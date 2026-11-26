// データの書き間違いを探す：node tools/check.js
// マップの大きさ、マス記号、イベント命令の名前、参照先（マップ・アイテム・コモン・イベント）を調べる。
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');
const fctx = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(root, 'files.js'), 'utf8'), fctx);
const scripts = fctx.window.FILES.scripts.filter((s) => !s.endsWith('main.js'));

const ctx = vm.createContext({ console, Math, JSON });
ctx.window = ctx;
for (const s of scripts) vm.runInContext(fs.readFileSync(path.join(root, s), 'utf8'), ctx, { filename: s });
const G = ctx.G, D = G.data;
const errors = [], warns = [];
const err = (where, msg) => errors.push(`${where}: ${msg}`);

// files.js に入っていないマップファイル
for (const f of fs.readdirSync(path.join(root, 'data/maps'))) {
  if (f.endsWith('.js') && !scripts.includes('data/maps/' + f)) err('files.js', `data/maps/${f} が読み込まれていません`);
}

const DEFAULT_LEGEND = ['#', '.', ' ', 'D'];
const TRIGGERS = ['action', 'touch', 'auto', 'parallel'];
const COND_KEYS = ['switch', 'self', 'var', 'item', 'dir', 'script', 'all', 'any', 'not', 'is', 'count'];
const MOVES = ['up', 'down', 'left', 'right', 'face', 'wait', 'speed', 'through', 'hide', 'show', 'facePlayer', 'random', 'toward'];
const legendOf = (m) => new Set([...DEFAULT_LEGEND, ...Object.keys(D.system.legend || {}), ...Object.keys(m.legend || {})]);
const TS = D.tilesets || {};
function checkTile(ref, where, needSize) {
  if (!Array.isArray(ref) || ref.length < 3) return err(where, 'tile は [素材ID, 列, 行(, 幅, 高さ)] の形で');
  const [id, c, r, w = 1, h = 1] = ref, t = TS[id];
  if (!t) return err(where, `素材「${id}」がありません（data/tilesets と files.js を確認）`);
  for (const col of [].concat(c)) if (!(col >= 0 && col + w <= t.cols)) err(where, `素材「${id}」の列 ${col}（幅${w}）が範囲外です（0〜${t.cols - 1}）`);
  if (!(r >= 0 && r + h <= t.rows)) err(where, `素材「${id}」の行 ${r}（高さ${h}）が範囲外です（0〜${t.rows - 1}）`);
}
for (const [ch, lg] of Object.entries(D.system.legend || {})) if (lg.tile) checkTile(lg.tile, `system.js の記号「${ch}」`);
function objectSolids(m) {
  const set = new Set();
  for (const o of m.objects || []) {
    if (o.solid === false) continue;
    const [, , , w = 1, h = 1] = o.tile || [];
    const rows = o.solid === 'bottom' ? [h - 1] : [...Array(h).keys()];
    for (let i = 0; i < w; i++) for (const j of rows) set.add((o.x + i) + ',' + (o.y + j));
  }
  return set;
}
const solidOf = (m) => Object.assign({ '#': { solid: true }, ' ': { solid: true } }, D.system.legend || {}, m.legend || {});

function checkCond(c, where) {
  if (!c) return;
  if (Array.isArray(c)) return c.forEach((x) => checkCond(x, where));
  for (const k of Object.keys(c)) if (!COND_KEYS.includes(k)) err(where, `未知の条件「${k}」`);
  if (c.all) checkCond(c.all, where);
  if (c.any) checkCond(c.any, where);
  if (c.not) checkCond(c.not, where);
  if (c.item !== undefined && !D.items[c.item]) err(where, `アイテム「${c.item}」がありません`);
  if (c.var && (!Array.isArray(c.var) || c.var.length !== 3)) err(where, 'var は [変数名, 比較, 値] の形で');
}
function checkSteps(steps, where) {
  for (const s of [].concat(steps)) if (!MOVES.includes(String(s).split(':')[0])) err(where, `未知の移動命令「${s}」`);
}
function checkList(list, where, map) {
  if (!Array.isArray(list)) return err(where, '命令の並びが配列になっていません');
  list.forEach((c, i) => {
    const w = `${where} の${i + 1}番目`;
    if (!Array.isArray(c) || typeof c[0] !== 'string') return err(w, '命令は [\'命令名\', ...] の形で');
    const [name, ...a] = c;
    if (!G.commands[name]) return err(w, `未知の命令「${name}」`);
    switch (name) {
      case 'choice':
        if (!Array.isArray(a[0])) err(w, '選択肢の文が配列になっていません');
        (a[1] || []).forEach((b, j) => checkList(b, `${w}（選択肢${j + 1}）`, map));
        break;
      case 'if': checkCond(a[0], w); if (a[1]) checkList(a[1], w + '（成り立つとき）', map); if (a[2]) checkList(a[2], w + '（成り立たないとき）', map); break;
      case 'loop': checkList(a[0], w + '（くり返し）', map); break;
      case 'common': if (!D.commons[a[0]]) err(w, `コモンイベント「${a[0]}」がありません`); break;
      case 'item': case 'getItem': if (!D.items[a[0]]) err(w, `アイテム「${a[0]}」がありません`); break;
      case 'enter':
      case 'transfer': {
        const m = D.maps[a[0]];
        if (!m) { err(w, `マップ「${a[0]}」がありません`); break; }
        const ch = (m.tiles[a[2]] || '')[a[1]], sol = solidOf(m)[ch];
        if (ch === undefined) err(w, `移動先 (${a[1]},${a[2]}) がマップの外です`);
        else if ((sol && sol.solid) || objectSolids(m).has(a[1] + ',' + a[2])) err(w, `移動先 (${a[1]},${a[2]}) は通れないマスです`);
        break;
      }
      case 'move': checkSteps(a[1], w); // fallthrough
      case 'balloon':
        if (map && a[0] !== 'player' && a[0] !== 'this' && !(map.events || []).some((e) => e.id === a[0])) err(w, `イベント「${a[0]}」がこのマップにありません`);
        break;
      case 'openMenu': if (a[0] && !['items', 'cards', 'log', 'save', 'load', 'title'].includes(a[0])) err(w, `メニュー「${a[0]}」はありません`); break;
    }
  });
}

// システム
const st = D.system.start;
if (!st || !D.maps[st.map]) err('system.js', '開始マップ（start.map）がありません');
for (const [n, l] of Object.entries(D.commons)) checkList(l, `コモン「${n}」`, null);
if (D.system.specialKey && !D.commons[D.system.specialKey]) err('system.js', `specialKey のコモン「${D.system.specialKey}」がありません`);
for (const [id, it] of Object.entries(D.items)) {
  if (!it.name) err(`アイテム「${id}」`, 'name がありません');
  if (it.common && !D.commons[it.common]) err(`アイテム「${id}」`, `コモン「${it.common}」がありません`);
}

// マップ
for (const [id, m] of Object.entries(D.maps)) {
  const where = `マップ「${id}」`, lg = legendOf(m);
  if (!Array.isArray(m.tiles) || !m.tiles.length) { err(where, 'tiles がありません'); continue; }
  const MW = [...m.tiles[0]].length, MH = m.tiles.length;
  if (MW < G.COLS || MH < 1) err(where, `横は${G.COLS}マス以上にしてください`);
  m.tiles.forEach((row, y) => {
    if ([...row].length !== MW) err(where, `${y + 1}行目が${[...row].length}文字です（1行目と同じ${MW}文字にする）`);
    for (const ch of row) if (!lg.has(ch)) err(where, `${y + 1}行目の記号「${ch}」が legend にありません`);
  });
  for (const [ch, lg] of Object.entries(m.legend || {})) if (lg.tile) checkTile(lg.tile, `${where} の記号「${ch}」`);
  (m.objects || []).forEach((o, i) => {
    const ow = `${where} の objects ${i + 1}番目`;
    checkTile(o.tile, ow);
    const [, , , w = 1, h = 1] = o.tile || [];
    if (!(o.x >= 0 && o.y >= 0 && o.x + w <= MW && o.y + h <= MH)) err(ow, `位置 (${o.x},${o.y}) がマップからはみ出しています`);
  });
  if (m.exit && m.exit.door && !(D.doors || {})[m.exit.door]) err(where, `exit の扉「${m.exit.door}」がありません`);
  for (const s of m.signs || []) if (!(s.x >= 0 && s.x < MW && s.y >= 0 && s.y < MH)) err(where, `名札「${s.text}」がマップの外です`);
  const extra = ((D.extraEvents || {})[id] || []).map((ev) => {
    if (!ev.at) return ev;
    const d = (D.doors || {})[ev.at];
    if (!d) { err(`${where}（story）`, `扉「${ev.at}」がありません`); return ev; }
    if (d.map !== id) err(`${where}（story）`, `扉「${ev.at}」は ${d.map} にあります`);
    return Object.assign({}, ev, { x: d.x + (ev.dx || 0), y: d.y + (ev.dy || 0) });
  });
  const ids = new Set();
  for (const e of [...(m.events || []), ...extra]) {
    const ew = `${where} のイベント「${e.id}」`;
    if (!e.id) err(where, 'id のないイベントがあります');
    if (ids.has(e.id)) err(ew, 'id が重複しています');
    ids.add(e.id);
    if (!(e.x >= 0 && e.x < MW && e.y >= 0 && e.y < MH)) err(ew, `位置 (${e.x},${e.y}) がマップの外です`);
    (e.pages || []).forEach((p, i) => {
      const pw = `${ew} の${i + 1}ページ目`;
      if (p.trigger && !TRIGGERS.includes(p.trigger)) err(pw, `trigger「${p.trigger}」は ${TRIGGERS.join('/')} のどれか`);
      if (p.priority && !['below', 'same', 'above'].includes(p.priority)) err(pw, `priority「${p.priority}」は below/same/above のどれか`);
      checkCond(p.cond, pw);
      if (p.autoMove) checkSteps(p.autoMove, pw);
      if (p.char && p.char.tile) checkTile(p.char.tile, pw);
      checkList(p.list || [], pw, m);
    });
  }
}
if (st && D.maps[st.map]) {
  const ch = D.maps[st.map].tiles[st.y][st.x];
  if ((solidOf(D.maps[st.map])[ch] || {}).solid || objectSolids(D.maps[st.map]).has(st.x + ',' + st.y)) err('system.js', '開始位置が通れないマスです');
}

console.log(`マップ ${Object.keys(D.maps).length}　アイテム ${Object.keys(D.items).length}　コモン ${Object.keys(D.commons).length}`);
warns.forEach((w) => console.log('注意: ' + w));
if (errors.length) { errors.forEach((e) => console.log('×  ' + e)); process.exit(1); }
console.log('問題は見つかりませんでした');
