// main.js — 起動（字体を読み込んでからタイトルへ）。files.js の一覧の最後に読み込まれる
'use strict';
(async () => {
  const G = window.G;
  document.title = G.data.system.title || document.title;
  try {
    await Promise.race([
      Promise.all([document.fonts.load(G.font(26), 'あA1'), document.fonts.load(G.font(26, true), 'あA1')]),
      new Promise((r) => setTimeout(r, 5000)),
    ]);
  } catch (e) { /* 字体が読めなくても動かす */ }
  await G.loadTilesets();
  G.start();
  G.goTitle();
})();
