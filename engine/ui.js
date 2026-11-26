// ui.js — 文章ウィンドウ、選択肢、ポップアップ、ログ、メニュー、セーブ、タイトル
'use strict';
(function () {
  const G = window.G;
  const W = () => G.world;
  // 画面の配置（system.js の layout。書いていない枠は全画面の配置になる）
  G.box = function (name) {
    const L = G.data.system.layout || {};
    const def = { map: { x: 0, y: 0, w: G.W, h: G.H }, message: { x: 8, y: G.H - 168, w: G.W - 16, h: 160 } };
    return L[name] || def[name] || null;
  };
  const LINE = 34, PAD = 20, PER_PAGE = 3;

  // ---------------- 文章 ----------------
  // 名前は枠の中の1行目。本文は3行ずつページを送る
  G.msg = {
    active: false, hidden: false, holdForChoice: false, lines: [], page: 0, shown: 0,
    show(name, text) {
      Object.assign(this, { active: true, hidden: false, holdForChoice: false, name, text, shown: 0, page: 0 });
      G.ctx.font = G.font(26);
      this.lines = G.wrap(G.ctx, text, G.box('message').w - PAD * 2);
      const log = W().S.log;
      log.push({ name, text });
      if (log.length > 300) log.shift();
    },
    pages() { return Math.max(1, Math.ceil(this.lines.length / PER_PAGE)); },
    pageLines() { return this.lines.slice(this.page * PER_PAGE, this.page * PER_PAGE + PER_PAGE); },
    pageTotal() { return this.pageLines().join('').length; },
    pageDone() { return this.shown >= this.pageTotal(); },
    typingDone() { return this.page >= this.pages() - 1 && this.pageDone(); },
    close() { this.active = false; this.holdForChoice = false; },
    update() {
      if (!this.active) return;
      const inp = G.input;
      if (this.hidden) {
        if (inp.trigger('ok') || inp.trigger('cancel') || inp.trigger('hide')) {
          this.hidden = false; inp.consume('ok'); inp.consume('cancel');
        }
        return;
      }
      if (inp.trigger('hide')) { this.hidden = true; return; }
      if (G.choice.active) return;
      if (inp.trigger('log')) { G.logView.open(); return; }
      if (!this.pageDone()) {
        if (inp.trigger('ok')) { this.shown = this.pageTotal(); inp.consume('ok'); }
        else this.shown = Math.min(this.pageTotal(), this.shown + (inp.isDown('dash') ? 4 : 1));
        return;
      }
      if (this.page < this.pages() - 1) {
        if (inp.trigger('ok')) { inp.consume('ok'); this.page++; this.shown = 0; }
        return;
      }
      if (this.holdForChoice) return;
      if (inp.trigger('ok') || inp.trigger('cancel')) { inp.consume('ok'); inp.consume('cancel'); this.close(); }
    },
    draw(ctx) {
      const B = G.box('message');
      G.drawFrame(ctx, B);
      if (!this.active || this.hidden) return;
      let y = B.y + 14;
      if (this.name) { G.text(ctx, '【' + this.name + '】', B.x + PAD - 6, y, 22, '#ffe9a8', 'left', true); }
      y += 32;
      let left = this.shown;
      this.pageLines().forEach((ln, i) => {
        if (left <= 0) return;
        G.text(ctx, ln.slice(0, left), B.x + PAD, y + i * LINE, 26);
        left -= ln.length;
      });
      if (this.pageDone() && !(this.holdForChoice && this.typingDone()) && G.frame % 40 < 28) {
        const x = B.x + B.w - 26, yy = B.y + B.h - 16;
        ctx.fillStyle = '#fff';
        ctx.beginPath(); ctx.moveTo(x - 8, yy - 6); ctx.lineTo(x + 8, yy - 6); ctx.lineTo(x, yy + 2); ctx.fill();
      }
    },
  };
  // 枠（黒地に白い縁）
  G.drawFrame = function (ctx, B, fill = 'rgba(0,0,0,0.92)') {
    G.roundRect(ctx, B.x, B.y, B.w, B.h, 10);
    ctx.fillStyle = fill; ctx.fill();
    ctx.lineWidth = 3; ctx.strokeStyle = '#fff'; ctx.stroke();
  };

  // ---------------- 選択肢 ----------------
  G.choice = {
    active: false, opts: [], index: 0, result: -1,
    open(opts, o = {}) {
      Object.assign(this, { active: true, opts, index: o.default || 0, result: -1, pos: o.pos || 'right' });
      this.cancel = o.cancel === 'last' ? opts.length - 1 : o.cancel === undefined ? -1 : o.cancel;
    },
    update() {
      if (!this.active || G.msg.hidden) return;
      const inp = G.input, n = this.opts.length;
      if (inp.repeat('down')) { this.index = (this.index + 1) % n; G.audio.se('cursor'); }
      if (inp.repeat('up')) { this.index = (this.index + n - 1) % n; G.audio.se('cursor'); }
      if (inp.trigger('ok')) { inp.consume('ok'); this.result = this.index; this.active = false; G.audio.se('ok'); }
      else if (inp.trigger('cancel') && this.cancel >= 0) { inp.consume('cancel'); this.result = this.cancel; this.active = false; G.audio.se('cancel'); }
    },
    draw(ctx) {
      if (!this.active || G.msg.hidden) return;
      const M = G.box('map'), B = G.box('message');
      ctx.font = G.font(24);
      const w = Math.max(160, ...this.opts.map((o) => ctx.measureText(o).width)) + 64;
      const h = this.opts.length * 44 + 20;
      const x = this.pos === 'center' ? M.x + (M.w - w) / 2 : this.pos === 'left' ? M.x + 8 : M.x + M.w - w - 8;
      const y = G.msg.active ? Math.min(B.y, M.y + M.h) - h - 8 : M.y + (M.h - h) / 2;
      G.drawWindow(ctx, x, y, w, h, 0.95);
      this.opts.forEach((o, i) => {
        if (i === this.index) {
          G.roundRect(ctx, x + 8, y + 10 + i * 44, w - 16, 42, 6);
          ctx.fillStyle = 'rgba(255,255,255,0.18)'; ctx.fill();
        }
        G.text(ctx, o, x + 32, y + 19 + i * 44, 24);
      });
    },
  };

  // ---------------- 立ち絵とゲージ ----------------
  G.hud = {
    // 立ち絵：話している人に立ち絵があればその人、なければ layout.portrait.default の人
    draw(ctx) {
      const P = G.box('portrait');
      if (P) {
        const ports = G.data.system.portraits || {};
        const who = (G.msg.active && ports[G.msg.name]) ? G.msg.name : P.default;
        const pt = ports[who];
        if (pt) this.drawPortrait(ctx, P, pt, who);
      }
      const g = G.box('gauge');
      if (g) this.drawGauge(ctx, g);
    },
    drawPortrait(ctx, P, pt, who) {
      const im = G.img(pt.img);
      if (im) { // 画像は枠の高さに合わせ、下そろえ・左右中央
        const k = Math.min(P.h / im.height, P.w / im.width);
        const w = im.width * k, h = im.height * k;
        ctx.save(); ctx.imageSmoothingEnabled = !pt.pixel; ctx.imageSmoothingQuality = 'high';  // pixel: true のドット絵の立ち絵だけ補正を切る
        ctx.drawImage(im, P.x + (P.w - w) / 2, P.y + P.h - h, w, h);
        ctx.restore();
        return;
      }
      // 仮の立ち絵（人影）
      const cx = P.x + P.w / 2, top = P.y + P.h * 0.08;
      ctx.save();
      ctx.globalAlpha = 0.9;
      ctx.fillStyle = pt.color || '#888';
      ctx.beginPath(); ctx.arc(cx, top + P.h * 0.12, P.h * 0.11, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath();
      ctx.moveTo(cx - P.w * 0.2, top + P.h * 0.26);
      ctx.lineTo(cx + P.w * 0.2, top + P.h * 0.26);
      ctx.lineTo(cx + P.w * 0.36, P.y + P.h);
      ctx.lineTo(cx - P.w * 0.36, P.y + P.h);
      ctx.closePath(); ctx.fill();
      ctx.globalAlpha = 1;
      G.text(ctx, '立ち絵（仮）', cx, top + P.h * 0.45, 20, '#fff', 'center', true);
      G.text(ctx, who, cx, top + P.h * 0.45 + 30, 26, '#fff', 'center', true);
      ctx.restore();
    },
    // 縦のゲージ：上にハート、下に丸。変数の値（0〜max）だけ下から満ちる
    drawGauge(ctx, g) {
      const S = W().S;
      const v = Math.max(0, Math.min(1, ((S && S.vars[g.var]) || 0) / (g.max || 100)));
      const cx = g.x, top = g.y + 34, bottom = g.y + g.h - 18, col = g.color || '#f07c8e';
      ctx.save();
      ctx.lineWidth = 3; ctx.strokeStyle = col;
      // 管
      G.roundRect(ctx, cx - 7, top, 14, bottom - top, 7);
      ctx.fillStyle = 'rgba(255,255,255,0.08)'; ctx.fill(); ctx.stroke();
      const fh = (bottom - top - 6) * v;
      if (fh > 0) { G.roundRect(ctx, cx - 4, bottom - 3 - fh, 8, fh, 4); ctx.fillStyle = col; ctx.fill(); }
      // 下の丸
      ctx.beginPath(); ctx.arc(cx, bottom + 2, 14, 0, Math.PI * 2);
      ctx.fillStyle = v > 0 ? col : '#000'; ctx.fill(); ctx.stroke();
      // 上のハート
      const hx = cx, hy = g.y + 16, r = 13;
      ctx.beginPath();
      ctx.moveTo(hx, hy + r * 1.3);
      ctx.bezierCurveTo(hx - r * 2, hy + r * 0.2, hx - r * 1.1, hy - r * 1.4, hx, hy - r * 0.3);
      ctx.bezierCurveTo(hx + r * 1.1, hy - r * 1.4, hx + r * 2, hy + r * 0.2, hx, hy + r * 1.3);
      ctx.fillStyle = v >= 1 ? col : '#000'; ctx.fill(); ctx.stroke();
      ctx.restore();
    },
  };

  // ---------------- ポップアップ ----------------
  G.popup = {
    queue: [], cur: null,
    show(text, frames = 150) { this.queue.push({ text, frames, t: 0 }); },
    update() {
      if (!this.cur && this.queue.length) this.cur = this.queue.shift();
      if (this.cur && ++this.cur.t >= this.cur.frames) this.cur = null;
    },
    draw(ctx) {
      const c = this.cur;
      if (!c) return;
      const a = Math.min(1, c.t / 10, (c.frames - c.t) / 15);
      ctx.save();
      ctx.globalAlpha = a;
      ctx.font = G.font(22);
      const w = ctx.measureText(c.text).width + 48, M = G.box('map');
      G.drawWindow(ctx, M.x + (M.w - w) / 2, M.y + 12, w, 48);
      G.text(ctx, c.text, M.x + M.w / 2, M.y + 25, 22, '#fff', 'center');
      ctx.restore();
    },
  };

  // ---------------- テキストログ ----------------
  G.logView = {
    active: false, rows: [], top: 0,
    open() {
      this.active = true;
      G.ctx.font = G.font(22);
      this.rows = [];
      for (const e of W().S.log) {
        if (e.name) this.rows.push({ s: '【' + e.name + '】', c: '#ffe9a8' });
        for (const ln of G.wrap(G.ctx, e.text, G.W - 120)) this.rows.push({ s: ln, c: '#fff' });
        this.rows.push({ s: '', c: '#fff' });
      }
      this.view = Math.floor((G.H - 110) / 32);
      this.top = Math.max(0, this.rows.length - this.view);
      G.audio.se('ok');
    },
    update() {
      const inp = G.input;
      if (inp.repeat('up')) this.top = Math.max(0, this.top - 1);
      if (inp.repeat('down')) this.top = Math.min(Math.max(0, this.rows.length - this.view), this.top + 1);
      if (inp.repeat('left')) this.top = Math.max(0, this.top - this.view);
      if (inp.repeat('right')) this.top = Math.min(Math.max(0, this.rows.length - this.view), this.top + this.view);
      if (inp.trigger('cancel') || inp.trigger('log') || inp.trigger('ok')) {
        inp.consume('ok'); inp.consume('cancel');
        this.active = false;
        G.audio.se('cancel');
      }
    },
    draw(ctx) {
      ctx.fillStyle = 'rgba(0,0,0,0.6)';
      ctx.fillRect(0, 0, G.W, G.H);
      G.drawWindow(ctx, 24, 24, G.W - 48, G.H - 48, 0.95);
      G.text(ctx, 'ログ（↑↓で送る／決定・戻るで閉じる）', 48, 40, 20, '#aab');
      this.rows.slice(this.top, this.top + this.view).forEach((r, i) => G.text(ctx, r.s, 56, 76 + i * 32, 22, r.c));
      if (!this.rows.length) G.text(ctx, 'まだ何もありません', G.W / 2, G.H / 2, 22, '#aab', 'center');
    },
  };

  // ---------------- セーブ ----------------
  G.save = {
    slots() { return G.data.system.saveSlots || 3; },
    key(i) { return (G.data.system.saveKey || 'rpg') + ':slot' + i; },
    read(i) { try { const s = localStorage.getItem(this.key(i)); return s ? JSON.parse(s) : null; } catch (e) { return null; } },
    write(i) {
      try {
        const W_ = W();
        localStorage.setItem(this.key(i), JSON.stringify({ time: Date.now(), mapName: W_.map.name || W_.S.map, state: W_.snapshot() }));
        return true;
      } catch (e) { return false; }
    },
    load(i) {
      const d = this.read(i);
      if (!d) return false;
      G.goMap();
      W().loadSave(d.state);
      return true;
    },
    any() { for (let i = 1; i <= this.slots(); i++) if (this.read(i)) return true; return false; },
  };

  // ---------------- メニュー ----------------
  const LABELS = { items: 'アイテム', cards: 'カード', log: 'ログ', save: 'セーブ', load: 'ロード', title: 'タイトルへ' };
  G.menu = {
    active: false, mode: 'main', index: 0,
    entries() {
      return (G.data.system.menu || ['items', 'cards', 'log', 'save', 'load', 'title']).map((e) =>
        typeof e === 'string' ? { key: e, label: LABELS[e] || e } : { key: 'common', label: e.label, common: e.common });
    },
    open(mode, fromTitle) {
      Object.assign(this, { active: true, mode: 'main', index: 0, sub: 0, fromTitle: !!fromTitle, direct: !!mode, list: this.entries() });
      G.audio.se('ok');
      if (mode) this.enter({ key: mode });
    },
    close() { this.active = false; },
    back() { G.audio.se('cancel'); if (this.fromTitle || this.direct) this.close(); else this.mode = 'main'; },
    ownedItems() { const S = W().S; return Object.keys(S.items).filter((id) => G.data.items[id] && G.data.items[id].type !== 'card' && !G.data.items[id].hidden); },
    cardIds() { return Object.keys(G.data.items).filter((id) => G.data.items[id].type === 'card'); },
    enter(e) {
      this.sub = 0;
      switch (e.key) {
        case 'items': this.mode = 'items'; break;
        case 'cards': this.mode = 'cards'; break;
        case 'log': this.close(); G.logView.open(); break;
        case 'save': case 'load': this.mode = e.key; break;
        case 'title': this.mode = 'confirm'; break;
        case 'common': this.close(); W().runCommon(e.common); break;
      }
    },
    update() {
      const inp = G.input;
      const ok = inp.trigger('ok'), cancel = inp.trigger('cancel');
      if (ok) inp.consume('ok');
      if (cancel) inp.consume('cancel');
      const nav = (n, cols = 1) => {
        if (!n) return;
        let i = this.sub;
        if (inp.repeat('down')) i += cols;
        if (inp.repeat('up')) i -= cols;
        if (cols > 1 && inp.repeat('right')) i += 1;
        if (cols > 1 && inp.repeat('left')) i -= 1;
        i = (i + n) % n;
        if (i !== this.sub) { this.sub = i; G.audio.se('cursor'); }
      };
      switch (this.mode) {
        case 'main': {
          const n = this.list.length;
          if (inp.repeat('down')) { this.index = (this.index + 1) % n; G.audio.se('cursor'); }
          if (inp.repeat('up')) { this.index = (this.index + n - 1) % n; G.audio.se('cursor'); }
          if (ok) { G.audio.se('ok'); this.enter(this.list[this.index]); }
          else if (cancel || inp.trigger('special')) { G.audio.se('cancel'); this.close(); }
          break;
        }
        case 'items': {
          const ids = this.ownedItems();
          nav(ids.length);
          if (ok && ids.length) {
            const it = G.data.items[ids[this.sub]];
            if (it.common) { G.audio.se('ok'); this.close(); W().runCommon(it.common); }
            else G.audio.se('buzzer');
          } else if (cancel) this.back();
          break;
        }
        case 'cards': nav(this.cardIds().length, 5); if (cancel || ok) this.back(); break;
        case 'save': case 'load': {
          nav(G.save.slots());
          if (ok) {
            const i = this.sub + 1;
            if (this.mode === 'save') {
              if (G.save.write(i)) { G.audio.se('ok'); G.popup.show('セーブしました'); this.close(); }
              else { G.audio.se('buzzer'); G.popup.show('セーブできませんでした'); }
            } else if (G.save.read(i)) { G.audio.se('ok'); this.close(); G.save.load(i); }
            else G.audio.se('buzzer');
          } else if (cancel) this.back();
          break;
        }
        case 'confirm': {
          nav(2);
          if (ok) { if (this.sub === 0) { G.audio.se('ok'); G.audio.bgm(null); G.goTitle(); } else this.back(); }
          else if (cancel) this.back();
          break;
        }
      }
    },
    draw(ctx) {
      ctx.fillStyle = 'rgba(0,0,0,0.45)';
      ctx.fillRect(0, 0, G.W, G.H);
      if (!this.fromTitle) {
        const list = this.list, h = list.length * 46 + 24;
        G.drawWindow(ctx, 16, 16, 200, h, 0.92);
        list.forEach((e, i) => {
          if (i === this.index) { G.roundRect(ctx, 24, 26 + i * 46, 184, 42, 6); ctx.fillStyle = this.mode === 'main' ? 'rgba(255,255,255,0.2)' : 'rgba(255,255,255,0.08)'; ctx.fill(); }
          G.text(ctx, e.label, 44, 35 + i * 46, 24);
        });
      }
      const X = this.fromTitle ? 120 : 232, Y = 16, Wd = G.W - X - (this.fromTitle ? 120 : 16), Hd = G.H - 32;
      const sel = (x, y, w, h, on) => { if (on) { G.roundRect(ctx, x, y, w, h, 6); ctx.fillStyle = 'rgba(255,255,255,0.2)'; ctx.fill(); } };
      switch (this.mode) {
        case 'items': {
          G.drawWindow(ctx, X, Y, Wd, Hd, 0.92);
          const ids = this.ownedItems(), S = W().S;
          if (!ids.length) G.text(ctx, '何も持っていない', X + 24, Y + 24, 22, '#aab');
          ids.forEach((id, i) => {
            sel(X + 8, Y + 12 + i * 44, Wd - 16, 42, i === this.sub);
            G.text(ctx, G.data.items[id].name, X + 24, Y + 21 + i * 44, 24);
            G.text(ctx, '×' + S.items[id], X + Wd - 24, Y + 21 + i * 44, 24, '#fff', 'right');
          });
          const it = G.data.items[ids[this.sub]];
          if (it) this.drawDesc(ctx, X, Wd, it.desc);
          break;
        }
        case 'cards': {
          G.drawWindow(ctx, X, Y, Wd, Hd, 0.92);
          const ids = this.cardIds(), S = W().S, cw = 98, ch = 132, gap = 12;
          const got = ids.filter((id) => S.items[id]).length;
          G.text(ctx, `カード ${got} / ${ids.length}`, X + 24, Y + 18, 22, '#ffe9a8', 'left', true);
          ids.forEach((id, i) => {
            const cx = X + 24 + (i % 5) * (cw + gap), cy = Y + 56 + Math.floor(i / 5) * (ch + gap);
            const it = G.data.items[id], has = !!S.items[id];
            G.roundRect(ctx, cx, cy, cw, ch, 8);
            ctx.fillStyle = has ? it.color || '#5a6fd6' : '#2a2c40'; ctx.fill();
            ctx.lineWidth = i === this.sub ? 4 : 2;
            ctx.strokeStyle = i === this.sub ? '#ffe9a8' : 'rgba(255,255,255,0.4)'; ctx.stroke();
            const im = has && G.img(it.img);
            if (im) ctx.drawImage(im, cx + 4, cy + 4, cw - 8, ch - 8);
            else G.text(ctx, has ? it.name : '？', cx + cw / 2, cy + ch / 2 - 12, has ? 16 : 30, '#fff', 'center', true);
          });
          const it = G.data.items[ids[this.sub]];
          if (it) this.drawDesc(ctx, X, Wd, S.items[ids[this.sub]] ? it.name + '：' + (it.desc || '') : 'まだ見つけていない');
          break;
        }
        case 'save': case 'load': {
          G.drawWindow(ctx, X, Y, Wd, Hd, 0.92);
          G.text(ctx, this.mode === 'save' ? 'どこにセーブしますか' : 'どれをロードしますか', X + 24, Y + 18, 22, '#ffe9a8', 'left', true);
          for (let i = 0; i < G.save.slots(); i++) {
            const d = G.save.read(i + 1), y = Y + 60 + i * 96;
            sel(X + 12, y, Wd - 24, 88, i === this.sub);
            G.text(ctx, 'ファイル ' + (i + 1), X + 32, y + 12, 24, '#fff', 'left', true);
            if (d) {
              const t = new Date(d.time);
              const ts = `${t.getFullYear()}/${t.getMonth() + 1}/${t.getDate()} ${String(t.getHours()).padStart(2, '0')}:${String(t.getMinutes()).padStart(2, '0')}`;
              G.text(ctx, d.mapName, X + 32, y + 50, 20, '#ccd');
              G.text(ctx, ts, X + Wd - 32, y + 50, 20, '#ccd', 'right');
            } else G.text(ctx, '（空き）', X + 32, y + 50, 20, '#889');
          }
          break;
        }
        case 'confirm': {
          const w = 360, h = 160, x = (G.W - w) / 2, y = (G.H - h) / 2;
          G.drawWindow(ctx, x, y, w, h, 0.95);
          G.text(ctx, 'タイトルに戻りますか？', x + w / 2, y + 22, 22, '#fff', 'center');
          ['はい', 'いいえ'].forEach((s, i) => { sel(x + 90, y + 64 + i * 44, w - 180, 40, i === this.sub); G.text(ctx, s, x + w / 2, y + 72 + i * 44, 22, '#fff', 'center'); });
          break;
        }
      }
    },
    drawDesc(ctx, X, Wd, desc) {
      if (!desc) return;
      const y = G.H - 16 - 110;
      G.drawWindow(ctx, X, y, Wd, 110, 0.95);
      ctx.font = G.font(20);
      G.wrap(ctx, desc, Wd - 48).slice(0, 3).forEach((ln, i) => G.text(ctx, ln, X + 24, y + 16 + i * 28, 20));
    },
  };

  // ---------------- 場面 ----------------
  G.titleScene = {
    start() { this.index = 0; this.hasSave = G.save.any(); this.t = 0; },
    update() {
      if (G.menu.active) { G.menu.update(); if (!G.menu.active) this.hasSave = G.save.any(); return; }
      this.t++;
      const inp = G.input;
      if (inp.repeat('down') || inp.repeat('up')) { this.index ^= 1; G.audio.se('cursor'); }
      if (inp.trigger('ok')) {
        inp.consume('ok');
        if (this.index === 0) { G.audio.se('ok'); G.goMap(); G.world.newGame(); }
        else if (this.hasSave) G.menu.open('load', true);
        else G.audio.se('buzzer');
      }
    },
    draw(ctx) {
      const sys = G.data.system;
      const im = G.img(sys.titleImage);
      if (im) ctx.drawImage(im, 0, 0, G.W, G.H);
      else {
        const g = ctx.createLinearGradient(0, 0, 0, G.H);
        g.addColorStop(0, '#1d2350'); g.addColorStop(1, '#5a3f6e');
        ctx.fillStyle = g; ctx.fillRect(0, 0, G.W, G.H);
      }
      G.text(ctx, sys.title || 'タイトル', G.W / 2, 170, 52, '#fff', 'center', true);
      if (sys.subtitle) G.text(ctx, sys.subtitle, G.W / 2, 240, 22, '#dde', 'center');
      ['はじめから', 'つづきから'].forEach((s, i) => {
        const y = 380 + i * 56;
        if (i === this.index) { G.roundRect(ctx, G.W / 2 - 130, y - 8, 260, 46, 8); ctx.fillStyle = 'rgba(255,255,255,0.2)'; ctx.fill(); }
        G.text(ctx, s, G.W / 2, y, 26, i === 1 && !this.hasSave ? '#889' : '#fff', 'center');
      });
      G.text(ctx, '移動：矢印キー　決定：Z／Enter　メニュー：X／Esc', G.W / 2, G.H - 64, 16, '#bbc', 'center');
      (sys.credits || []).forEach((c, i, a) => G.text(ctx, c, G.W / 2, G.H - 32 - (a.length - 1 - i) * 22, 16, '#dde', 'center'));
      if (this.t < 20) { ctx.fillStyle = `rgba(0,0,0,${1 - this.t / 20})`; ctx.fillRect(0, 0, G.W, G.H); }
      if (G.menu.active) G.menu.draw(ctx);
    },
  };

  G.mapScene = {
    update() {
      if (G.logView.active) { G.logView.update(); return; }
      if (G.menu.active) { G.menu.update(); G.popup.update(); return; }
      G.msg.update();
      G.choice.update();
      W().update();
      G.popup.update();
    },
    draw(ctx) {
      W().draw(ctx);
      G.hud.draw(ctx);
      G.msg.draw(ctx);
      G.choice.draw(ctx);
      if (G.menu.active) G.menu.draw(ctx);
      G.popup.draw(ctx);
      if (G.logView.active) G.logView.draw(ctx);
    },
  };

  const resetUI = () => { G.menu.active = false; G.msg.close(); G.choice.active = false; G.logView.active = false; };
  G.goTitle = () => { resetUI(); G.scene = G.titleScene; G.titleScene.start(); };
  G.goMap = () => { resetUI(); G.scene = G.mapScene; };
})();
