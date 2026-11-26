// 読み込むファイルの一覧と版の番号。index.html が開くたびに毎回新しく読む。
// マップなどを足したら scripts に1行足す（順番どおりに読み込む。main.js は最後）。
// 版の番号 v は tools/stamp.py が書き換える。
window.FILES = {
  v: '20261127064756',
  scripts: [
    'engine/core.js',
    'engine/world.js',
    'engine/interpreter.js',
    'engine/ui.js',
    'data/tilesets/school_in.js',
    'data/tilesets/school_out.js',
    'data/tilesets/own.js',
    'data/system.js',
    'data/items.js',
    'data/commons.js',
    'data/maps/escape.js',
    // 学校の地図とお話は data/archive/school/ に残してある（いまは読み込まない）
    'engine/main.js',
  ],
};
