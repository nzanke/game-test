// world.js — 部屋（マップ）、キャラクター、イベントの起動、条件、演出、描画
'use strict';
(function () {
  const G = window.G;
  const T = G.T;
  const DIRS = (G.DIRS = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] });

  // マスの記号の既定値（マップや system.js の legend で上書き・追加できる）
  const DEFAULT_LEGEND = {
    '#': { solid: true, color: '#4a4658' },
    '.': { color: '#d9cfbc' },
    ' ': { solid: true, color: '#000000' },
    'D': { color: '#7a5232' },
  };

  function cmp(a, op, b) {
    switch (op) {
      case '==': case '=': return a === b;
      case '!=': return a !== b;
      case '>=': return a >= b;
      case '<=': return a <= b;
      case '>': return a > b;
      case '<': return a < b;
    }
    console.warn('未知の比較', op);
    return false;
  }

  // ---------------- キャラクター ----------------
  class Char {
    constructor(x, y, dir) {
      this.setPos(x, y);
      this.dir = dir || 'down';
      this.speed = 4;
      this.through = false;
      this.route = null;     // 今の移動ルート
      this.baseRoute = null; // 自律移動（autoMove）
      this.balloon = null;
      this.opacity = 1;
      this.stepAnim = 0;
      this.locked = false;
      this.look = null;
    }
    setPos(x, y) { this.x = x; this.y = y; this.rx = x * T; this.ry = y * T; }
    get moving() { return this.rx !== this.x * T || this.ry !== this.y * T; }
    tryMove(d) {
      this.dir = d;
      const [dx, dy] = DIRS[d];
      const nx = this.x + dx, ny = this.y + dy;
      if (this.through || W.passable(nx, ny, this)) { this.x = nx; this.y = ny; return true; }
      // イベントの側からプレイヤーにぶつかったとき（接触で起動）
      if (this !== W.player && !W.interp && W.player.x === nx && W.player.y === ny) {
        const e = W.events.find((v) => v.char === this);
        if (e && e.page && e.page.trigger === 'touch') W.start(e);
      }
      return false;
    }
    facePlayer() {
      const p = W.player, dx = p.x - this.x, dy = p.y - this.y;
      if (!dx && !dy) return;
      this.dir = Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 'right' : 'left') : dy > 0 ? 'down' : 'up';
    }
    update() {
      const tx = this.x * T, ty = this.y * T, s = this.speed;
      if (this.rx < tx) this.rx = Math.min(tx, this.rx + s); else if (this.rx > tx) this.rx = Math.max(tx, this.rx - s);
      if (this.ry < ty) this.ry = Math.min(ty, this.ry + s); else if (this.ry > ty) this.ry = Math.max(ty, this.ry - s);
      if (this.moving) this.stepAnim++;
      if (this.balloon && ++this.balloon.t >= this.balloon.dur) this.balloon = null;
      if (this.route && !this.moving && !(this.locked && this.route.loop)) this.stepRoute();
    }
    stepRoute() {
      const r = this.route;
      if (r.wait > 0) { r.wait--; return; }
      if (r.i >= r.steps.length) {
        if (r.loop) r.i = 0;
        else { this.route = this.baseRoute ? Object.assign({}, this.baseRoute, { i: 0, wait: 0 }) : null; return; }
      }
      const st = String(r.steps[r.i]);
      const [cmd, arg] = st.split(':');
      if (DIRS[cmd]) {
        if (this.tryMove(cmd)) { r.i++; r.block = 0; }
        else if (r.skip || ++r.block > 30) { r.i++; r.block = 0; }
        return;
      }
      r.i++;
      switch (cmd) {
        case 'face': this.dir = arg; break;
        case 'wait': r.wait = +arg; break;
        case 'speed': this.speed = +arg; break;
        case 'through': this.through = arg === 'on'; break;
        case 'hide': this.opacity = 0; break;
        case 'show': this.opacity = 1; break;
        case 'facePlayer': this.facePlayer(); break;
        case 'random': this.tryMove(Object.keys(DIRS)[Math.floor(Math.random() * 4)]); break;
        case 'toward': {
          const p = W.player, dx = p.x - this.x, dy = p.y - this.y;
          this.tryMove(Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 'right' : 'left') : dy > 0 ? 'down' : 'up');
          break;
        }
        default: console.warn('未知の移動命令', st);
      }
    }
  }
  G.Char = Char;

  const freshFx = () => ({ fade: 0, flash: null, shake: null, tintAnim: null });

  // ---------------- 世界 ----------------
  const W = (G.world = {
    S: null, map: null, events: [], player: null, interp: null, fx: freshFx(), legend: {}, mapCanvas: null,

    newGame() {
      const st = G.data.system.start;
      this.S = { map: null, x: st.x, y: st.y, dir: st.dir || 'down', switches: {}, vars: {}, self: {}, items: {}, log: [], pics: {}, tint: [0, 0, 0, 0], bgm: null };
      this.interp = null;
      this.fx = freshFx();
      this.loadMap(st.map, st.x, st.y, st.dir || 'down');
    },
    loadSave(state) {
      this.S = state;
      this.interp = null;
      this.fx = freshFx();
      this.loadMap(state.map, state.x, state.y, state.dir);
      G.audio.bgm(state.bgm);
    },
    snapshot() {
      const p = this.player;
      Object.assign(this.S, { x: p.x, y: p.y, dir: p.dir });
      return JSON.parse(JSON.stringify(this.S));
    },

    loadMap(id, x, y, dir) {
      const m = G.data.maps[id];
      if (!m) { console.error('マップがありません: ' + id); G.popup.show('マップがありません: ' + id); return; }
      this.map = m;
      this.S.map = id;
      this.legend = Object.assign({}, DEFAULT_LEGEND, G.data.system.legend || {}, m.legend || {});
      this.mh = m.tiles.length;
      this.mw = Math.max(...m.tiles.map((r) => r.length));
      this.player = new Char(x, y, dir);
      this.player.look = (G.data.system.player || {}).char || { shape: 'person', color: '#4a7bd0' };
      const extra = ((G.data.extraEvents || {})[id] || []).map((ev) => {
        if (!ev.at) return ev;
        const d = (G.data.doors || {})[ev.at];
        if (!d) { console.warn('扉がありません: ' + ev.at); return ev; }
        return Object.assign({}, ev, { x: d.x + (ev.dx || 0), y: d.y + (ev.dy || 0) });
      });
      this.events = [...(m.events || []), ...extra].map((def) => ({
        def, id: def.id, char: new Char(def.x, def.y, def.dir), page: null, pageIndex: -1, erased: false, interp: null,
      }));
      this.solidCells = new Set();
      for (const o of m.objects || []) {
        if (o.solid === false) continue;
        const [, , , w = 1, h = 1] = o.tile;
        const rows = o.solid === 'bottom' ? [h - 1] : [...Array(h).keys()];
        for (let i = 0; i < w; i++) for (const j of rows) this.solidCells.add((o.x + i) + ',' + (o.y + j));
      }
      this.buildMapCanvas();
      this.refresh();
      if (m.bgm !== undefined) { G.audio.bgm(m.bgm); this.S.bgm = m.bgm; }
    },
    buildMapCanvas() {
      const c = document.createElement('canvas');
      c.width = this.mw * T; c.height = this.mh * T;
      const ctx = c.getContext('2d');
      ctx.fillStyle = this.map.bgColor || '#000';
      ctx.fillRect(0, 0, c.width, c.height);
      for (let y = 0; y < this.mh; y++) {
        for (let x = 0; x < this.mw; x++) {
          const lg = this.legend[this.tileAt(x, y)];
          if (!lg) continue;
          ctx.fillStyle = lg.color || '#000';
          ctx.fillRect(x * T, y * T, T, T);
          const base = lg.base && this.legend[lg.base];
          if (base && base.tile) G.drawTile(ctx, base.tile, x * T, y * T, x);
          if (lg.tile && G.drawTile(ctx, lg.tile, x * T, y * T, x)) continue;
          if (lg.solid && lg.color !== '#000000') {
            ctx.fillStyle = 'rgba(0,0,0,0.25)';
            ctx.fillRect(x * T, y * T + T - 6, T, 6); // 下に影をつけて立体っぽく
            ctx.fillStyle = 'rgba(255,255,255,0.08)';
            ctx.fillRect(x * T, y * T, T, 4);
          } else if (!lg.solid) {
            ctx.strokeStyle = 'rgba(0,0,0,0.06)';
            ctx.strokeRect(x * T + 0.5, y * T + 0.5, T - 1, T - 1);
          }
          if (lg.mark) G.text(ctx, lg.mark, x * T + T / 2, y * T + 12, 22, 'rgba(0,0,0,0.45)', 'center');
        }
      }
      for (const o of this.map.objects || []) if (!o.above) G.drawTile(ctx, o.tile, o.x * T, o.y * T, o.x);
      // 名札（扉の上の部屋名など）
      for (const s of this.map.signs || []) {
        ctx.font = G.font(14, true);
        const w = Math.max(40, ctx.measureText(s.text).width + 14), cx = s.x * T + T / 2, y = s.y * T + 6;
        G.roundRect(ctx, cx - w / 2, y, w, 22, 4);
        ctx.fillStyle = '#fbfaf3'; ctx.fill();
        ctx.lineWidth = 2; ctx.strokeStyle = '#5a4a3a'; ctx.stroke();
        G.text(ctx, s.text, cx, y + 4, 14, '#2a2420', 'center', true);
      }
      this.mapCanvas = c;
    },

    eventById(id) { return this.events.find((e) => e.id === id); },
    tileAt(x, y) { const row = this.map.tiles[y]; return row === undefined ? undefined : row[x]; },
    tilePassable(x, y) {
      const lg = this.legend[this.tileAt(x, y)];
      return !!lg && !lg.solid && !this.solidCells.has(x + ',' + y);
    },
    passable(x, y, mover) {
      if (x < 0 || y < 0 || x >= this.mw || y >= this.mh) return false;
      if (!this.tilePassable(x, y)) return false;
      for (const e of this.events) {
        if (e.char === mover || e.erased || !e.page) continue;
        if (e.char.x === x && e.char.y === y && e.page.priority === 'same' && !e.page.through) return false;
      }
      if (mover !== this.player && this.player.x === x && this.player.y === y) return false;
      return true;
    },

    // ---- イベントのページ選び（条件を満たすページのうち、いちばん後ろのもの） ----
    pageFor(e) {
      const pages = e.def.pages || [];
      for (let i = pages.length - 1; i >= 0; i--) if (this.check(pages[i].cond, e)) return i;
      return -1;
    },
    refresh() {
      for (const e of this.events) {
        const i = this.pageFor(e);
        if (i === e.pageIndex) continue;
        e.pageIndex = i;
        e.page = i >= 0 ? e.def.pages[i] : null;
        e.interp = null;
        const pg = e.page || {}, c = e.char;
        if (e.page && !pg.priority) pg.priority = pg.char && pg.char.shape !== 'none' ? 'same' : 'below';
        c.look = pg.char || null;
        c.through = !!pg.through;
        if (pg.dir) c.dir = pg.dir;
        c.baseRoute = pg.autoMove ? { steps: pg.autoMove, i: 0, wait: 0, loop: true, block: 0, skip: true } : null;
        c.route = c.baseRoute ? Object.assign({}, c.baseRoute) : null;
      }
    },

    // ---- 条件 ----
    selfKey(e, letter) { return this.S.map + ':' + (e ? e.id : '-') + ':' + letter; },
    check(c, e) {
      if (!c) return true;
      if (Array.isArray(c)) return c.every((x) => this.check(x, e));
      const S = this.S, want = c.is === undefined ? true : c.is;
      if (c.all) return c.all.every((x) => this.check(x, e));
      if (c.any) return c.any.some((x) => this.check(x, e));
      if (c.not) return !this.check(c.not, e);
      if (c.switch !== undefined) return !!S.switches[c.switch] === want;
      if (c.self !== undefined) return !!S.self[this.selfKey(e, c.self)] === want;
      if (c.var) {
        const [n, op, v] = c.var;
        const rhs = typeof v === 'string' && v[0] === '$' ? S.vars[v.slice(1)] || 0 : v;
        return cmp(S.vars[n] || 0, op, rhs) === want;
      }
      if (c.item !== undefined) return ((S.items[c.item] || 0) >= (c.count || 1)) === want;
      if (c.dir) return (this.player.dir === c.dir) === want;
      if (c.script) return !!c.script(G, S, e) === want;
      console.warn('未知の条件', c);
      return false;
    },

    // ---- 起動 ----
    start(e) {
      if (this.interp || !e.page || !e.page.list || !e.page.list.length) return false;
      this.interp = new G.Interp(e.page.list, e);
      if (e.page.char && !e.page.fixDir && e.page.trigger !== 'auto') e.char.facePlayer();
      return true;
    },
    runCommon(name) {
      const l = G.data.commons[name];
      if (!l) { console.warn('コモンイベントがありません: ' + name); return; }
      if (!this.interp) this.interp = new G.Interp(l, null);
    },
    live(e) { return !e.erased && e.page; },
    checkAction() {
      const p = this.player, [dx, dy] = DIRS[p.dir], fx = p.x + dx, fy = p.y + dy;
      const here = this.events.filter((e) => this.live(e) && e.char.x === p.x && e.char.y === p.y && e.page.priority !== 'same');
      const front = this.events.filter((e) => this.live(e) && e.char.x === fx && e.char.y === fy && !(e.page.priority === 'below' && this.tilePassable(fx, fy)));
      const cands = [...here, ...front];
      for (const tr of ['action', 'touch']) {
        for (const e of cands) if ((e.page.trigger || 'action') === tr && this.start(e)) return true;
      }
      return false;
    },
    checkTouchHere() {
      const p = this.player;
      for (const e of this.events) {
        if (this.live(e) && e.char.x === p.x && e.char.y === p.y && e.page.priority !== 'same' && e.page.trigger === 'touch' && this.start(e)) return true;
      }
      return false;
    },
    checkTouchFront(d) {
      const p = this.player, [dx, dy] = DIRS[d];
      for (const e of this.events) {
        if (this.live(e) && e.char.x === p.x + dx && e.char.y === p.y + dy && e.page.priority === 'same' && e.page.trigger === 'touch' && this.start(e)) return true;
      }
      return false;
    },

    // ---- 毎フレームの更新 ----
    update() {
      this.refresh();
      for (const e of this.events) {
        if (!this.live(e) || e.page.trigger !== 'parallel') continue;
        if (!e.interp || e.interp.done) e.interp = new G.Interp(e.page.list || [], e, true);
        e.interp.update();
      }
      let busy = false;
      if (this.interp) {
        busy = true;
        this.interp.update();
        if (this.interp && this.interp.done) this.interp = null;
      } else if (!G.msg.active) {
        for (const e of this.events) {
          if (this.live(e) && e.page.trigger === 'auto' && this.start(e)) { busy = true; break; }
        }
      }
      if (!busy && !G.msg.active && G.scene === G.mapScene) this.updatePlayer();
      const was = this.player.moving;
      this.player.update();
      for (const e of this.events) {
        e.char.locked = !!(this.interp && this.interp.ev === e);
        e.char.update();
      }
      if (was && !this.player.moving && !this.interp) this.checkTouchHere();
      this.updateFx();
    },
    updatePlayer() {
      const p = this.player, inp = G.input;
      if (p.moving) return;
      if (inp.trigger('cancel')) { inp.consume('cancel'); G.menu.open(); return; }
      if (inp.trigger('log')) { G.logView.open(); return; }
      if (inp.trigger('special') && G.data.system.specialKey) { this.runCommon(G.data.system.specialKey); return; }
      if (inp.trigger('ok')) { inp.consume('ok'); if (this.checkAction()) return; }
      const d = inp.dir4();
      if (d) {
        p.speed = inp.isDown('dash') ? 8 : 4;
        if (!p.tryMove(d)) this.checkTouchFront(d);
      }
    },
    updateFx() {
      const f = this.fx;
      if (f.flash && ++f.flash.t >= f.flash.dur) f.flash = null;
      if (f.shake && ++f.shake.t >= f.shake.dur) f.shake = null;
      if (f.tintAnim) {
        const a = f.tintAnim, k = ++a.t / a.dur;
        this.S.tint = a.from.map((v, i) => v + (a.to[i] - v) * k);
        if (a.t >= a.dur) { this.S.tint = a.to.slice(); f.tintAnim = null; }
      }
      for (const id in this.S.pics) {
        const p = this.S.pics[id];
        if (p.anim) {
          const a = p.anim, k = ++a.t / a.dur;
          for (const key in a.to) p[key] = a.from[key] + (a.to[key] - a.from[key]) * k;
          if (a.t >= a.dur) delete p.anim;
        }
        if (p.shake && ++p.shake.t >= p.shake.dur) delete p.shake;
      }
    },

    // ---------------- 描画 ----------------
    // 画面の左上が、マップのどこにあたるか（小さいマップは中央に置く）
    camera() {
      const p = this.player, mw = this.mw * T, mh = this.mh * T;
      const cx = mw <= G.W ? -(G.W - mw) / 2 : Math.max(0, Math.min(mw - G.W, p.rx + T / 2 - G.W / 2));
      const cy = mh <= G.H ? -(G.H - mh) / 2 : Math.max(0, Math.min(mh - G.H, p.ry + T / 2 - G.H / 2));
      return [Math.round(cx), Math.round(cy)];
    },
    draw(ctx) {
      const sh = this.fx.shake;
      const ox = sh ? Math.round(Math.sin(sh.t * 1.8) * sh.power * (1 - sh.t / sh.dur)) : 0;
      const [cx, cy] = this.camera();
      ctx.fillStyle = '#000';
      ctx.fillRect(0, 0, G.W, G.H);
      ctx.save();
      ctx.translate(ox - cx, -cy);
      ctx.drawImage(this.mapCanvas, 0, 0);
      const bg = G.img(this.map.bg);
      if (bg) ctx.drawImage(bg, 0, 0, G.W, G.H);
      const order = { below: 0, same: 1, above: 2 };
      const list = this.events.filter((e) => this.live(e) && e.char.look).map((e) => ({ c: e.char, pri: e.page.priority }));
      list.push({ c: this.player, pri: 'same' });
      list.sort((a, b) => order[a.pri] - order[b.pri] || a.c.ry - b.c.ry);
      for (const o of list) drawChar(ctx, o.c, o.c.look);
      for (const o of this.map.objects || []) if (o.above) G.drawTile(ctx, o.tile, o.x * T, o.y * T, o.x);
      this.drawSensor(ctx);
      for (const o of list) if (o.c.balloon) drawBalloon(ctx, o.c);
      ctx.restore();
      ctx.save();
      ctx.translate(ox, 0);
      this.drawPics(ctx);
      ctx.restore();
      const t = this.S.tint;
      if (t[3] > 0) { ctx.fillStyle = `rgba(${t[0] | 0},${t[1] | 0},${t[2] | 0},${t[3]})`; ctx.fillRect(0, 0, G.W, G.H); }
      const fl = this.fx.flash;
      if (fl) {
        const [r, g, b, a = 1] = fl.color;
        ctx.fillStyle = `rgba(${r},${g},${b},${a * (1 - fl.t / fl.dur)})`;
        ctx.fillRect(0, 0, G.W, G.H);
      }
      if (this.fx.fade > 0) { ctx.fillStyle = `rgba(0,0,0,${this.fx.fade})`; ctx.fillRect(0, 0, G.W, G.H); }
    },
    // 近くに調べられるものがあると「！」で知らせる
    drawSensor(ctx) {
      const cfg = G.data.system.sensor;
      if (cfg === false || this.interp) return;
      const dist = (cfg && cfg.distance) || 2, p = this.player;
      for (const e of this.events) {
        if (!this.live(e) || e.def.sensor === false || e.page.sensor === false) continue;
        const tr = e.page.trigger || 'action';
        if ((tr !== 'action' && tr !== 'touch') || !e.page.list || !e.page.list.length) continue;
        if (Math.abs(e.char.x - p.x) + Math.abs(e.char.y - p.y) > dist) continue;
        const x = e.char.rx + T / 2, y = e.char.ry - 6 + Math.sin(G.frame / 8) * 3;
        ctx.globalAlpha = 0.65 + 0.35 * Math.sin(G.frame / 10);
        ctx.beginPath(); ctx.arc(x, y, 11, 0, Math.PI * 2);
        ctx.fillStyle = '#ffd34d'; ctx.fill();
        G.text(ctx, '!', x, y - 9, 18, '#5a3b00', 'center', true);
        ctx.globalAlpha = 1;
      }
    },
    drawPics(ctx) {
      const ids = Object.keys(this.S.pics).map(Number).sort((a, b) => a - b);
      for (const id of ids) {
        const p = this.S.pics[id];
        ctx.save();
        ctx.globalAlpha = Math.max(0, Math.min(1, p.opacity));
        const sx = p.shake ? Math.sin(p.shake.t * 1.8) * p.shake.power * (1 - p.shake.t / p.shake.dur) : 0;
        ctx.translate(p.x + sx, p.y);
        ctx.scale(p.scale, p.scale);
        const im = G.img(p.src);
        const w = im ? im.width : p.w, h = im ? im.height : p.h;
        const x0 = p.origin === 'topleft' ? 0 : -w / 2, y0 = p.origin === 'topleft' ? 0 : -h / 2;
        if (im) ctx.drawImage(im, x0, y0);
        else {
          if (p.color) {
            G.roundRect(ctx, x0, y0, w, h, 16);
            ctx.fillStyle = p.color; ctx.fill();
            ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(255,255,255,0.6)'; ctx.stroke();
          }
          if (p.text) {
            const size = p.fontSize || 28;
            const lines = String(G.fmt(p.text)).split('\n');
            lines.forEach((ln, i) => G.text(ctx, ln, x0 + w / 2, y0 + h / 2 - (lines.length * size * 1.3) / 2 + i * size * 1.3, size, p.textColor || '#fff', 'center', true));
          }
        }
        ctx.restore();
      }
    },
  });

  // キャラクターの仮の絵
  function drawChar(ctx, c, look) {
    if (!look || look.shape === 'none' || c.opacity <= 0) return;
    const x = c.rx, y = c.ry;
    ctx.save();
    ctx.globalAlpha = c.opacity;
    const im = G.img(look.img);
    if (look.sprite) {
      // 歩行グラフィック：横3コマ（左足・立ち・右足）×縦4段（下・左・右・上）
      const sp = G.img(look.sprite);
      if (sp) {
        const fw = sp.width / 3, fh = sp.height / 4, k = look.scale || (fw >= 48 ? 1 : 1.5); // 48pxのコマは等倍
        const row = { down: 0, left: 1, right: 2, up: 3 }[c.dir] || 0;
        const col = c.moving ? [0, 1, 2, 1][Math.floor(c.stepAnim / 8) % 4] : 1;
        ctx.fillStyle = 'rgba(0,0,0,0.18)';
        ctx.beginPath(); ctx.ellipse(x + 24, y + 43, 14, 5, 0, 0, Math.PI * 2); ctx.fill();
        ctx.imageSmoothingEnabled = false;
        ctx.drawImage(sp, col * fw, row * fh, fw, fh, x + T / 2 - (fw * k) / 2, y + T - fh * k, fw * k, fh * k);
        ctx.imageSmoothingEnabled = true;
      }
    } else if (look.tile) {
      const h = look.tile[4] || 1;
      G.drawTile(ctx, look.tile, x, y - (h - 1) * T, c.x);
    } else if (im) {
      ctx.drawImage(im, x + T / 2 - im.width / 2, y + T - im.height);
    } else if (look.shape === 'person' || !look.shape) {
      const bob = c.moving ? Math.abs(Math.sin(c.stepAnim * 0.35)) * 3 : 0;
      ctx.fillStyle = 'rgba(0,0,0,0.2)';
      ctx.beginPath(); ctx.ellipse(x + 24, y + 44, 15, 5, 0, 0, Math.PI * 2); ctx.fill();
      G.roundRect(ctx, x + 11, y + 19 - bob, 26, 25, 8);
      ctx.fillStyle = look.color || '#888'; ctx.fill();
      ctx.beginPath(); ctx.arc(x + 24, y + 14 - bob, 11, 0, Math.PI * 2);
      ctx.fillStyle = look.skin || '#f3d6b8'; ctx.fill();
      ctx.beginPath(); ctx.arc(x + 24, y + 12 - bob, 11.5, Math.PI, 0);
      ctx.fillStyle = look.hair || '#3b2a20'; ctx.fill();
      ctx.fillStyle = '#222';
      const ey = y + 15 - bob;
      if (c.dir === 'down') { ctx.fillRect(x + 19, ey, 2.5, 3); ctx.fillRect(x + 27, ey, 2.5, 3); }
      else if (c.dir === 'left') ctx.fillRect(x + 16, ey, 2.5, 3);
      else if (c.dir === 'right') ctx.fillRect(x + 30, ey, 2.5, 3);
      else { ctx.beginPath(); ctx.arc(x + 24, y + 13 - bob, 11.5, 0, Math.PI * 2); ctx.fillStyle = look.hair || '#3b2a20'; ctx.fill(); }
    } else if (look.shape === 'box') {
      G.roundRect(ctx, x + 6, y + 6, 36, 36, 6);
      ctx.fillStyle = look.color || '#999'; ctx.fill();
      ctx.lineWidth = 2; ctx.strokeStyle = 'rgba(0,0,0,0.3)'; ctx.stroke();
    } else if (look.shape === 'card') {
      const bob = Math.sin(G.frame / 15 + c.x) * 3;
      G.roundRect(ctx, x + 12, y + 6 + bob, 24, 34, 4);
      ctx.fillStyle = look.color || '#5a6fd6'; ctx.fill();
      ctx.lineWidth = 2; ctx.strokeStyle = '#fff'; ctx.stroke();
      G.text(ctx, '★', x + 24, y + 14 + bob, 14, 'rgba(255,255,255,0.85)', 'center');
    } else if (look.shape === 'icon') {
      const bob = Math.sin(G.frame / 15 + c.x) * 3;
      G.text(ctx, look.icon || '?', x + 24, y + 8 + bob, 30, look.color || '#fff', 'center');
    }
    if (look.label) G.text(ctx, look.label, x + 24, y - 16, 14, '#fff', 'center', true);
    ctx.restore();
  }

  function drawBalloon(ctx, c) {
    const b = c.balloon, k = Math.min(1, b.t / 6);
    const x = c.rx + 24, y = c.ry - 22;
    ctx.save();
    ctx.translate(x, y);
    ctx.scale(k, k);
    G.roundRect(ctx, -20, -20, 40, 34, 10);
    ctx.fillStyle = '#fff'; ctx.fill();
    ctx.beginPath(); ctx.moveTo(-5, 14); ctx.lineTo(0, 22); ctx.lineTo(5, 14); ctx.fill();
    ctx.lineWidth = 2; ctx.strokeStyle = '#333'; G.roundRect(ctx, -20, -20, 40, 34, 10); ctx.stroke();
    G.text(ctx, b.kind, 0, -14, 22, '#c0392b', 'center', true);
    ctx.restore();
  }
})();
