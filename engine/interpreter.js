// interpreter.js — イベント命令の実行
// 命令は ['命令名', 引数1, 引数2, ...] の配列。一覧は DATA_FORMAT.md を参照。
'use strict';
(function () {
  const G = window.G;
  const W = () => G.world;

  // 文中の {v:変数名} {item:アイテムID} {player} を置き換える
  G.fmt = function (s) {
    const S = W().S;
    return String(s)
      .replace(/\{v:([^}]+)\}/g, (_, n) => (S ? S.vars[n] || 0 : 0))
      .replace(/\{item:([^}]+)\}/g, (_, n) => (G.data.items[n] || {}).name || n)
      .replace(/\{player\}/g, (G.data.system.player || {}).name || '');
  };

  function* waitWhile(fn) { while (fn()) yield; }
  function* fadeTo(v, frames) {
    const fx = W().fx, s = fx.fade, n = Math.max(1, frames);
    for (let i = 1; i <= n; i++) { fx.fade = s + (v - s) * (i / n); yield; }
  }
  function resolve(it, target) {
    if (target === 'player') return W().player;
    if (target === 'this' || target === undefined) return it.ev ? it.ev.char : null;
    const e = W().eventById(target);
    if (!e) console.warn('イベントがありません: ' + target);
    return e ? e.char : null;
  }

  // ---------------- 命令 ----------------
  const CMD = (G.commands = {
    // 文章
    *text(name, body) {
      G.msg.show(G.fmt(name || ''), G.fmt(body));
      if (this.next && this.next[0] === 'choice') { G.msg.holdForChoice = true; return; }
      yield* waitWhile(() => G.msg.active);
    },
    *choice(options, branches, opt = {}) {
      yield* waitWhile(() => G.msg.active && !G.msg.typingDone());
      G.choice.open(options.map(G.fmt), opt);
      yield* waitWhile(() => G.choice.active);
      const r = G.choice.result;
      if (G.msg.active) G.msg.close();
      if (r >= 0 && branches && branches[r]) yield* this.run(branches[r]);
    },
    popup(text, frames = 150) { G.popup.show(G.fmt(text), frames); },

    // 流れ
    *if(cond, thenList, elseList) {
      if (W().check(cond, this.ev)) { if (thenList) yield* this.run(thenList); }
      else if (elseList) yield* this.run(elseList);
    },
    *loop(list) {
      while (!this.stopped) {
        yield* this.run(list);
        if (this.breaking) { this.breaking = false; break; }
        yield; // 1周ごとに1フレーム進める（固まり防止）
      }
    },
    break() { this.breaking = true; },
    end() { this.stopped = true; },
    *wait(frames) { for (let i = 0; i < frames; i++) yield; },
    *common(name) {
      const l = G.data.commons[name];
      if (!l) { console.warn('コモンイベントがありません: ' + name); return; }
      yield* this.run(l);
    },
    script(fn) { fn(G, W().S, this.ev); },

    // スイッチ・変数・アイテム
    switch(name, val = true) { for (const n of [].concat(name)) W().S.switches[n] = !!val; },
    var(name, op, v) {
      const S = W().S;
      let val = typeof v === 'string' && v[0] === '$' ? S.vars[v.slice(1)] || 0 : v;
      if (op === 'rand') { val = v[0] + Math.floor(Math.random() * (v[1] - v[0] + 1)); op = '='; }
      const cur = S.vars[name] || 0;
      S.vars[name] =
        op === '=' ? val : op === '+' ? cur + val : op === '-' ? cur - val :
        op === '*' ? cur * val : op === '/' ? Math.floor(cur / val) : op === '%' ? cur % val : cur;
    },
    self(letter, val = true, eventId) {
      const e = eventId ? W().eventById(eventId) : this.ev;
      if (e) W().S.self[W().selfKey(e, letter)] = !!val;
    },
    item(id, n = 1) {
      const S = W().S, v = Math.max(0, (S.items[id] || 0) + n);
      if (v) S.items[id] = v; else delete S.items[id];
    },
    getItem(id, n = 1) {
      CMD.item.call(this, id, n);
      G.audio.se('item');
      const it = G.data.items[id] || { name: id };
      G.popup.show(`${it.name} を手に入れた${n > 1 ? `（×${n}）` : ''}`);
    },

    // 移動
    *transfer(map, x, y, dir, opt = {}) {
      const fade = opt.fade !== false;
      if (fade) yield* fadeTo(1, 15);
      W().loadMap(map, x, y, dir || W().player.dir);
      if (fade) yield* fadeTo(0, 15);
    },
    // 部屋に入る：いまの場所を覚えてから移動し、部屋名を出す（出るときは back）
    *enter(map, x, y, dir, label) {
      const p = W().player, S = W().S;
      (S.back = S.back || []).push({ map: S.map, x: p.x, y: p.y, dir: 'down' });
      if (S.back.length > 20) S.back.shift();
      yield* CMD.transfer.call(this, map, x, y, dir || 'down');
      if (label) G.popup.show(G.fmt(label), 100);
    },
    // 入ってきた場所へ戻る。覚えていなければマップの exit（{ door: '扉の名前' } か { map, x, y }）へ
    *back() {
      const S = W().S;
      let to = (S.back || []).pop();
      if (!to) {
        const ex = W().map.exit || {};
        const d = ex.door ? (G.data.doors || {})[ex.door] : ex;
        if (d && d.map) to = { map: d.map, x: d.x, y: d.y + (ex.door ? 1 : 0), dir: 'down' };
      }
      if (!to) { console.warn('戻り先がありません'); return; }
      yield* CMD.transfer.call(this, to.map, to.x, to.y, to.dir);
    },
    *move(target, steps, wait = true) {
      const c = resolve(this, target);
      if (!c) return;
      const r = { steps: [].concat(steps), i: 0, wait: 0, loop: false, block: 0, skip: false };
      c.route = r;
      if (wait) yield* waitWhile(() => c.route === r);
    },
    *balloon(target, kind = '!', wait = true) {
      const c = resolve(this, target);
      if (!c) return;
      const b = { kind, t: 0, dur: 60 };
      c.balloon = b;
      if (wait) yield* waitWhile(() => c.balloon === b);
    },
    erase() { if (this.ev) this.ev.erased = true; },

    // ピクチャ
    pic(id, opt = {}) {
      W().S.pics[id] = Object.assign({ x: G.W / 2, y: G.H / 2, w: 200, h: 200, opacity: 1, scale: 1, origin: 'center' }, opt);
    },
    *picMove(id, to, frames = 30, wait = true) {
      const p = W().S.pics[id];
      if (!p) return;
      const from = {};
      for (const k in to) from[k] = p[k] !== undefined ? p[k] : 0;
      p.anim = { from, to, t: 0, dur: Math.max(1, frames) };
      if (wait) yield* waitWhile(() => p.anim && W().S.pics[id] === p);
    },
    picErase(id) { delete W().S.pics[id]; },
    *picShake(id, power = 8, frames = 30, wait = false) {
      const p = W().S.pics[id];
      if (!p) return;
      p.shake = { power, t: 0, dur: frames };
      if (wait) yield* waitWhile(() => p.shake);
    },

    // 画面の演出
    *shake(power = 5, frames = 30, wait = false) {
      W().fx.shake = { power: power * 2, t: 0, dur: frames };
      if (wait) yield* waitWhile(() => W().fx.shake);
    },
    *flash(color = [255, 255, 255], frames = 30, wait = false) {
      W().fx.flash = { color, t: 0, dur: frames };
      if (wait) yield* waitWhile(() => W().fx.flash);
    },
    *tint(color = [0, 0, 0, 0], frames = 30, wait = true) {
      const to = color.length === 3 ? [...color, 0.3] : color.slice();
      W().fx.tintAnim = { from: W().S.tint.slice(), to, t: 0, dur: Math.max(1, frames) };
      if (wait) yield* waitWhile(() => W().fx.tintAnim);
    },
    *fadeout(frames = 30) { yield* fadeTo(1, frames); },
    *fadein(frames = 30) { yield* fadeTo(0, frames); },

    // 音
    se(name) { G.audio.se(name); },
    bgm(src, vol) { G.audio.bgm(src, vol); W().S.bgm = src || null; },

    // その他
    *openMenu(mode) { G.menu.open(mode); yield* waitWhile(() => G.menu.active); },
    *title() {
      yield* fadeTo(1, 30);
      G.audio.bgm(null);
      G.goTitle();
      this.stopped = true;
    },
  });

  // ---------------- 実行役 ----------------
  class Interp {
    constructor(list, ev, parallel) {
      this.ev = ev || null;
      this.parallel = !!parallel;
      this.done = false;
      this.stopped = false;
      this.breaking = false;
      this.ops = 0;
      this.gen = this.run(list);
    }
    update() {
      if (this.done) return;
      this.ops = 0;
      try {
        if (this.gen.next().done) this.done = true;
      } catch (err) {
        console.error('イベント実行エラー', err);
        G.popup.show('エラー: ' + err.message, 300);
        this.done = true;
      }
    }
    *run(list) {
      for (let i = 0; i < list.length; i++) {
        if (this.stopped || this.breaking) return;
        if (++this.ops > 5000) { this.ops = 0; yield; }
        const c = list[i];
        this.next = list[i + 1];
        const h = CMD[c[0]];
        if (!h) { console.warn('未知の命令', c); continue; }
        const r = h.apply(this, c.slice(1));
        if (r && typeof r.next === 'function') yield* r;
      }
    }
  }
  G.Interp = Interp;
})();
