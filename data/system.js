// system.js — ゲーム全体の設定
G.defineSystem({
  title: '夕方の空き教室',
  subtitle: '（システムとデザインの試作）',
  // タイトル画面の下に出す表示（素材の著作権表示など）
  credits: ['タイル素材：ドット絵世界'],
  // 画面の配置（画面は816×624）。map：地図の枠、message：文章の枠、portrait：立ち絵の枠、gauge：右端のゲージ
  // layout を消すと、地図が全画面で文章が下に重なる配置になる
  layout: {
    map: { x: 14, y: 14, w: 518, h: 432 },
    message: { x: 14, y: 456, w: 518, h: 156 },
    portrait: { x: 440, y: 0, w: 330, h: 624, default: 'ぼたん' },  // 会話中は話している人、それ以外（地の文も）は default の人（主人公）
    gauge: { x: 787, y: 12, h: 604, var: 'affection', max: 100 },  // var の変数の値だけ満ちる
  },
  // 立ち絵。img に画像（下そろえで枠の高さに合わせる）を書く。img がないと仮の人影
  portraits: {
    'ぼたん': { color: '#d99da6', img: 'img/portraits/botan.png', crop: [128, 0, 395, 746] },
    'かなで': { color: '#8a7a95', img: 'img/portraits/kanade.png', crop: [62, 0, 402, 760] },  // crop：腰から上を拡大して見せる。ドット絵の立ち絵なら pixel: true
  },
  // 最初にいる場所
  start: { map: 'escape', x: 7, y: 6, dir: 'right' },
  // 主人公
  player: { name: 'ぼたん', char: { sprite: 'img/chars/botan_chibi.png' } },
  // セーブ（ブラウザに保存）
  saveKey: 'game-test',
  saveSlots: 3,
  // メニューに並べる項目（{ label, common } でコモンイベントを呼ぶ項目も足せる）
  menu: ['items', 'log', 'save', 'load', 'title'],
  // Qキー（スマホは★）で呼ぶコモンイベント
  specialKey: 'hint',
  // 近くの調べられるものを「！」で知らせる（false で無効）
  sensor: { always: true },  // always：距離に関係なく出す（distance: 2 なら2マス以内だけ）
  // 全マップ共通のマス記号。tile: [素材ID, 列, 行]（列を配列にすると横に並べたとき順に使い分ける）
  legend: {
    '#': { solid: true, color: '#2b2733' },                       // 外側（暗い所）
    // 窓のある壁（上・中・下の3段）
    '1': { solid: true, tile: ['school_in', [0, 1, 2, 3, 4, 5], 5] },
    '2': { solid: true, tile: ['school_in', [0, 1, 2, 3, 4, 5], 6] },
    '3': { solid: true, tile: ['school_in', [0, 1, 2, 3, 4, 5], 7] },
    // 窓のない壁（上・中・下の3段）
    '4': { solid: true, tile: ['school_in', 0, 2] },
    '5': { solid: true, tile: ['school_in', 0, 3] },
    '6': { solid: true, tile: ['school_in', 0, 4] },
    // 引き戸（上・中・下の3段。いちばん下にイベントを置く）
    '7': { solid: true, tile: ['school_in', 6, 5] },
    '8': { solid: true, tile: ['school_in', 6, 6] },
    '9': { solid: true, tile: ['school_in', 6, 7] },
    // 床
    '.': { tile: ['school_in', [0, 1], 0] },  // 木の床
    ',': { tile: ['school_in', [4, 5], 0] },  // 緑の床（廊下）
    ':': { tile: ['school_in', [3, 4], 1] },  // 寄せ木の床
    ';': { tile: ['school_in', [5, 6], 1] },  // 灰色のじゅうたん
    '^': { tile: ['own', 0, 0] },              // 階段
    // 自作の床タイル（data/tilesets/floor.js）
    'A': { tile: ['floor', 0, 0] },   // 市松のタイル
    'B': { tile: ['floor', 1, 0] },   // 石の床
    'C': { tile: ['floor', 2, 0] },   // レンガ
    'D': { tile: ['floor', 3, 0] },   // 大理石風のタイル
    'E': { tile: ['floor', 4, 0] },   // 赤いじゅうたん
    'F': { tile: ['floor', 5, 0] },   // 人工芝
    'G': { tile: ['floor', 6, 0] },   // 体育館の床
    'H': { tile: ['floor', 7, 0] },   // コンクリート
    'I': { tile: ['floor', 0, 1] },   // 縞鋼板（金属）
    'J': { tile: ['floor', 1, 1] },   // グレーチング（側溝のふた）
    'K': { tile: ['floor', 2, 1] },  // 点字ブロック（線）
    'L': { tile: ['floor', 3, 1] },  // 点字ブロック（点）
    'M': { tile: ['floor', 4, 1] },  // 濃い木の床
    'N': { tile: ['floor', 5, 1] },  // 青いじゅうたん
    'O': { tile: ['floor', 6, 1] },  // 土・砂
    'P': { tile: ['floor', 7, 1] },  // ゴムマット
  },
});
