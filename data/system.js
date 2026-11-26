// system.js — ゲーム全体の設定
G.defineSystem({
  title: 'ゲームテスト',
  subtitle: '自作エンジンの動作確認用',
  // タイトル画面の下に出す表示（素材の著作権表示など）
  credits: ['タイル素材：ドット絵世界'],
  // 最初にいる場所
  start: { map: 'room1', x: 2, y: 6, dir: 'up' },
  // 主人公
  player: { name: 'ハル', char: { shape: 'person', color: '#4a7bd0', hair: '#2b2018' } },
  // セーブ（ブラウザに保存）
  saveKey: 'game-test',
  saveSlots: 3,
  // メニューに並べる項目（{ label, common } でコモンイベントを呼ぶ項目も足せる）
  menu: ['items', 'cards', 'log', 'save', 'load', 'title'],
  // Qキー（スマホは★）で呼ぶコモンイベント
  specialKey: 'hint',
  // 近くの調べられるものを「！」で知らせる（false で無効）
  sensor: { distance: 2 },
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
  },
});
