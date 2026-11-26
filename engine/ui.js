// ui.js — 文章ウィンドウ、選択肢、ポップアップ、ログ、メニュー、セーブ、タイトル
'use strict';
(function () {
  const G = window.G;
  const W = () => G.world;
  const MSG_Y = G.H - 168, MSG_H = 160, LINE = 38, PAD = 24;

  // ---------------- 文章 ----------------
  G.msg = {
    active: false, hidden: false, holdForChoice: false, lines: [], shown: 0, total: 0,
    show(name, text) {
      Object.assign(this, { active: true, hidden: false, holdForChoice: false, name, text, shown: 0 });
      G.ctx.font = G.font(26);
      this.lines = G.wrap(G.ctx, text, G.W - 16 - PAD * 2);
      this.total = this.lines.join('').length;
      const log = W().S.log;
      log.push({ name, text });
      if (log.length > 300) log.shift();
    },
    typingDone() { return this.shown >= this.total; },
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
      if (!this.typingDone()) {
        if (inp.trigger('ok')) { this.shown = this.total; inp.consume('ok'); }
        else this.shown = Math.min(this.total, this.shown + (inp.isDown('dash') ? 4 : 1));
        return;
      }
      if (this.holdForChoice) return;
      if (inp.trigger('ok') || inp.trigger('cancel')) { inp.consume('ok'); inp.consume('cancel'); this.close(); }
    },
    draw(ctx) {
      if (!this.active || this.hidden) return;
      G.drawWindow(ctx, 8, MSG_Y, G.W - 16, MSG_H);
      if (this.name) {
        ctx.font = G.font(24, true);
        const w = ctx.measureText(this.name).width + 40;
        G.drawWindow(ctx, 8, MSG_Y - 52, w, 46);
        G.text(ctx, this.name, 28, MSG_Y - 41, 24, '#ffe9a8', 'left', true);
      }
      let left = this.shown;
      this.lines.slice(0, 3).forEach((ln, i) => {
        if (left <= 0) return;
        G.text(ctx, ln.slice(0, left), 8 + PAD, MSG_Y + 20 + i * LINE, 26);
        left -= ln.length;
      });
      if (this.typingDone() && !this.holdForChoice && G.frame % 40 < 28) {
        const x = G.W / 2, y = MSG_Y + MSG_H - 18;
        ctx.fillStyle = '#fff';
        ctx.beginPath(); ctx.moveTo(x - 8, y - 6); ctx.lineTo(x + 8, y - 6); ctx.lineTo(x, y + 2); ctx.fill();
      }
    },
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
      ctx.font = G.font(24);
      const w = Math.max(160, ...this.opts.map((o) => ctx.measureText(o).width)) + 64;
      const h = this.opts.length * 44 + 20;
      let x = this.pos === 'center' ? (G.W - w) / 2 : this.pos === 'left' ? 8 : G.W - w - 8;
      let y = G.msg.active ? MSG_Y - h - 8 : (G.H - h) / 2;
      if (this.pos === 'center' && !G.msg.active) y = (G.H - h) / 2;
      G.drawWindow(ctx, x, y, w, h);
      this.opts.forEach((o, i) => {
        if (i === this.index) {
          G.roundRect(ctx, x + 8, y + 10 + i * 44, w - 16, 42, 6);
          ctx.fillStyle = 'rgba(255,255,255,0.18)'; ctx.fill();
        }
        G.text(ctx, o, x + 32, y + 19 + i * 44, 24);
      });
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
      const w = ctx.measureText(c.text).width + 48;
      G.drawWindow(ctx, (G.W - w) / 2, 16, w, 48);
      G.text(ctx, c.text, G.W / 2, 29, 22, '#fff', 'center');
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
