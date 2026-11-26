// core.js — 土台：定数、データ登録、入力、音、画像、描画の小道具、メインループ
'use strict';
(function () {
  const G = (window.G = {
    W: 816, H: 624, T: 48, COLS: 17, ROWS: 13,
    data: { maps: {}, items: {}, commons: {}, system: {} },
    frame: 0,
    scene: null,
    defineMap(id, def) { def.id = id; this.data.maps[id] = def; },
    defineItems(o) { Object.assign(this.data.items, o); },
    defineCommons(o) { Object.assign(this.data.commons, o); },
    defineSystem(o) { Object.assign(this.data.system, o); },
    defineTileset(id, def) { this.data.tilesets = this.data.tilesets || {}; this.data.tilesets[id] = def; },
    // 扉の位置の一覧（名前 → { map, x, y }）。イベントの at: '名前' や back の戻り先に使う
    defineDoors(o) { this.data.doors = Object.assign(this.data.doors || {}, o); },
    // 生成したマップなどに、あとからイベントを足す
    addEvents(mapId, evs) { const e = (this.data.extraEvents = this.data.extraEvents || {}); (e[mapId] = e[mapId] || []).push(...evs); },
    // 半角英数は BIZ UDGothic（index.html で英数字だけ読み込む）、それ以外は BIZ UDPGothic
    font(size, bold) {
      return `${bold ? 'bold ' : ''}${size}px "BIZ UDGothic","BIZ UDPGothic",sans-serif`;
    },
  });

  // ---------------- 入力 ----------------
  const KEYMAP = {
    ArrowUp: 'up', KeyW: 'up', ArrowDown: 'down', KeyS: 'down',
    ArrowLeft: 'left', KeyA: 'left', ArrowRight: 'right', KeyD: 'right',
    KeyZ: 'ok', Enter: 'ok', Space: 'ok', NumpadEnter: 'ok',
    KeyX: 'cancel', Escape: 'cancel', Backspace: 'cancel',
    ShiftLeft: 'dash', ShiftRight: 'dash',
    KeyQ: 'special', KeyL: 'log', KeyH: 'hide',
  };
  const input = (G.input = {
    held: {}, pend: {}, time: {},
    press(k) { if (!this.held[k]) { this.held[k] = true; this.pend[k] = true; } },
    release(k) { this.held[k] = false; },
    update() {
      const keys = new Set([...Object.keys(this.held), ...Object.keys(this.pend)]);
      for (const k of keys) {
        if (this.pend[k]) { this.time[k] = 1; this.pend[k] = false; }
        else if (this.held[k]) this.time[k] = (this.time[k] || 0) + 1;
        else this.time[k] = -1;
      }
    },
    trigger(k) { return this.time[k] === 1; },
    repeat(k) { const t = this.time[k]; return t === 1 || (t > 24 && t % 6 === 1); },
    isDown(k) { return !!this.held[k] || this.time[k] === 1; },
    consume(k) { if (this.time[k] === 1) this.time[k] = 2; },
    dir4() {
      let best = null, bt = 1e9;
      for (const d of ['up', 'down', 'left', 'right']) {
        if (this.isDown(d) && this.time[d] < bt) { best = d; bt = this.time[d]; }
      }
      return best; // いちばん新しく押した方向
    },
    clear() { this.held = {}; this.pend = {}; this.time = {}; },
  });

  G.bindInput = function (canvas) {
    window.addEventListener('keydown', (e) => {
      const k = KEYMAP[e.code];
      if (!k) return;
      e.preventDefault();
      G.audio.ensure();
      if (!e.repeat) input.press(k);
    });
    window.addEventListener('keyup', (e) => { const k = KEYMAP[e.code]; if (k) input.release(k); });
    window.addEventListener('blur', () => input.clear());
    // 画面のタップ＝決定
    canvas.addEventListener('pointerdown', (e) => { e.preventDefault(); G.audio.ensure(); input.press('ok'); });
    canvas.addEventListener('pointerup', () => input.release('ok'));
    canvas.addEventListener('pointerleave', () => input.release('ok'));
    // スマホ用ボタン
    document.querySelectorAll('[data-key]').forEach((b) => {
      const k = b.dataset.key;
      const on = (e) => { e.preventDefault(); G.audio.ensure(); input.press(k); b.classList.add('on'); };
      const off = (e) => { e.preventDefault(); input.release(k); b.classList.remove('on'); };
      b.addEventListener('pointerdown', on);
      b.addEventListener('pointerup', off);
      b.addEventListener('pointerleave', off);
      b.addEventListener('pointercancel', off);
    });
  };

  // ---------------- 音 ----------------
  // 効果音は名前で呼ぶと電子音を鳴らす（仮の音）。ファイル名（.ogg など）を渡すとそれを鳴らす。
  G.audio = {
    ctx: null, bgmEl: null, bgmSrc: null,
    tones: {
      cursor: [[880, 0.04]],
      ok: [[660, 0.05], [990, 0.07]],
      cancel: [[500, 0.05], [330, 0.08]],
      buzzer: [[150, 0.18, 'square']],
      item: [[784, 0.08], [1047, 0.08], [1319, 0.16]],
      door: [[220, 0.08, 'triangle'], [160, 0.14, 'triangle']],
      shock: [[110, 0.3, 'sawtooth']],
      talk: [[520, 0.03]],
      magic: [[523, 0.07], [659, 0.07], [784, 0.07], [1047, 0.2]],
    },
    ensure() {
      try {
        if (!this.ctx) this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        if (this.ctx.state === 'suspended') this.ctx.resume();
      } catch (e) { this.ctx = null; }
      return this.ctx;
    },
    se(name) {
      if (!name) return;
      if (/\.(ogg|mp3|wav|m4a)$/i.test(name)) {
        try { const a = new Audio(name); a.volume = 0.8; a.play().catch(() => {}); } catch (e) {}
        return;
      }
      const seq = this.tones[name];
      const ctx = seq && this.ensure();
      if (!ctx) return;
      let t = ctx.currentTime;
      for (const [f, d, type] of seq) {
        const o = ctx.createOscillator(), g = ctx.createGain();
        o.type = type || 'sine';
        o.frequency.value = f;
        g.gain.setValueAtTime(0.12, t);
        g.gain.exponentialRampToValueAtTime(0.001, t + d);
        o.connect(g).connect(ctx.destination);
        o.start(t); o.stop(t + d + 0.02);
        t += d;
      }
    },
    bgm(src, vol = 0.6) {
      if ((src || null) === this.bgmSrc) return;
      if (this.bgmEl) { this.bgmEl.pause(); this.bgmEl = null; }
      this.bgmSrc = src || null;
      if (!src) return;
      try { const a = new Audio(src); a.loop = true; a.volume = vol; a.play().catch(() => {}); this.bgmEl = a; } catch (e) {}
    },
  };

  // ---------------- 画像 ----------------
  // 版の番号（index.html の ?v=…）。画像も古いものを使い回さないよう、この番号をつけて読む
  G.ver = ((typeof document !== 'undefined' && document.currentScript && document.currentScript.src.match(/[?&]v=([^&]+)/)) || [])[1] || '';
  G.url = (src) => (G.ver && !/^(https?:|data:|blob:)/.test(src) ? src + (src.includes('?') ? '&' : '?') + 'v=' + G.ver : src);
  G.images = {};
  G.img = function (src) {
    if (!src) return null;
    let i = G.images[src];
    if (!i) { i = new Image(); i.src = G.url(src); G.images[src] = i; }
    return i.complete && i.naturalWidth ? i : null;
  };

  // ---------------- タイル素材 ----------------
  // 素材は data/tilesets/*.js に、そのままでは画像として開けない形（XOR）で入っている。
  // 作り方：python3 tools/encode_tileset.py 元の画像.png ID
  const TILE_KEY = 'game-test-tileset';
  G.tilesets = {};
  G.loadTilesets = function () {
    const defs = G.data.tilesets || {};
    return Promise.all(Object.entries(defs).map(([id, d]) => new Promise((resolve) => {
      if (d.src) { // 自作のタイル（ふつうのPNG）
        const im = new Image();
        im.onload = () => { G.tilesets[id] = im; resolve(); };
        im.onerror = () => { console.error('素材を読めません: ' + id); resolve(); };
        im.src = G.url(d.src);
        return;
      }
      try {
        const bin = atob(d.data), bytes = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i) ^ TILE_KEY.charCodeAt(i % TILE_KEY.length);
        const im = new Image();
        im.onload = () => { G.tilesets[id] = im; resolve(); };
        im.onerror = () => { console.error('素材を読めません: ' + id); resolve(); };
        im.src = URL.createObjectURL(new Blob([bytes], { type: 'image/png' }));
      } catch (e) { console.error('素材を読めません: ' + id, e); resolve(); }
    })));
  };
  // ref = [素材ID, 列, 行, 幅, 高さ]。列を配列にすると、置く位置（x）で順に使い分ける
  G.drawTile = function (ctx, ref, dx, dy, mx = 0) {
    const [id, c, r, w = 1, h = 1] = ref;
    const im = G.tilesets[id], d = (G.data.tilesets || {})[id];
    if (!im || !d) return false;
    const col = Array.isArray(c) ? c[mx % c.length] : c, S = d.size || 32;
    const sm = ctx.imageSmoothingEnabled;
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(im, col * S, r * S, w * S, h * S, dx, dy, w * G.T, h * G.T);
    ctx.imageSmoothingEnabled = sm;
    return true;
  };

  // ---------------- 描画の小道具 ----------------
  G.roundRect = function (ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  };
  G.drawWindow = function (ctx, x, y, w, h, alpha = 0.86) {
    G.roundRect(ctx, x, y, w, h, 10);
    ctx.fillStyle = `rgba(12,14,32,${alpha})`;
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = 'rgba(255,255,255,0.75)';
    ctx.stroke();
  };
  // 幅に合わせて折り返す（\n は改行）
  G.wrap = function (ctx, text, maxW) {
    const out = [];
    for (const para of String(text).split('\n')) {
      let line = '';
      for (const ch of para) {
        if (line && ctx.measureText(line + ch).width > maxW) { out.push(line); line = ''; }
        line += ch;
      }
      out.push(line);
    }
    return out;
  };
  G.text = function (ctx, s, x, y, size = 24, color = '#fff', align = 'left', bold = false) {
    ctx.font = G.font(size, bold);
    ctx.textAlign = align;
    ctx.textBaseline = 'top';
    ctx.fillStyle = color;
    ctx.fillText(s, x, y);
  };

  // ---------------- メインループ（1秒60回） ----------------
  G.start = function () {
    const cv = document.getElementById('screen');
    cv.width = G.W;
    cv.height = G.H;
    G.ctx = cv.getContext('2d');
    G.bindInput(cv);
    const step = 1000 / 60;
    let last = performance.now(), acc = 0;
    function tick(now) {
      acc += Math.min(now - last, 250);
      last = now;
      let n = 0;
      while (acc >= step && n < 5) {
        input.update();
        G.frame++;
        if (G.scene) G.scene.update();
        acc -= step;
        n++;
      }
      if (n && G.scene) G.scene.draw(G.ctx);
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  };
})();
