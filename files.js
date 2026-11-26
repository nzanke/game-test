// 読み込むファイルの一覧と版の番号。index.html が開くたびに毎回新しく読む。
// マップなどを足したら scripts に1行足す（順番どおりに読み込む。main.js は最後）。
// 版の番号 v は tools/stamp.py が書き換える。
window.FILES = {
  v: '20261127062615',
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
    'data/maps/room1.js',
    'data/maps/library.js',
    'data/maps/school_main1f.js',
    'data/maps/school_main2f.js',
    'data/maps/school_main3f.js',
    'data/maps/school_main4f.js',
    'data/maps/school_annex1f.js',
    'data/maps/school_annex2f.js',
    'data/maps/school_annex3f.js',
    'data/maps/school_annex4f.js',
    'data/maps/school_rooms.js',
    'data/maps/school_doors.js',
    'data/story.js',
    'engine/main.js',
  ],
};
