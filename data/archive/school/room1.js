// room1.js — 保健室（ゲームの始まり）
G.defineMap('room1', {
  name: '保健室',
  exit: { door: '保健室' },  // back で戻る先（入ってきた記録がないとき）
  // 17列×13行。記号の意味は system.js の legend（このマップだけの記号は legend に足す）
  tiles: [
    '#111111111117111#',
    '#222222222228222#',
    '#333333333339333#',
    '#;;;;;;;;;;;;;;;#',
    '#;;;;;;;;;;;;;;;#',
    '#;;;;;;;;;;;;;;;#',
    '#;;;;;;;;;;;;;;;#',
    '#;;;;;;;;;;;;;;;#',
    '#;;;;;;;;;;;;;;;#',
    '#;;;;;;;;;;;;;;;#',
    '#;;;;;;;;;;;;;;;#',
    '#;;;;;;;;;;;;;;;#',
    '#################',
  ],
  // 複数マスの家具など。tile: [素材ID, 列, 行, 幅, 高さ]、x・y は左上のマス
  // solid: 'bottom' はいちばん下の段だけ通れない（壁ぎわの家具）、false は通れる
  objects: [
    { tile: ['school_in', 5, 14, 2, 2], x: 1, y: 4 },                   // ベッド
    { tile: ['school_in', 5, 14, 2, 2], x: 1, y: 8 },                   // ベッド
    { tile: ['school_in', 0, 11, 1, 3], x: 3, y: 3 },                   // カーテン
    { tile: ['school_in', 0, 11, 1, 3], x: 3, y: 7 },                   // カーテン
    { tile: ['school_in', 2, 20, 3, 2], x: 8, y: 2, solid: 'bottom' },  // 机
    { tile: ['school_in', 6, 9, 1, 2], x: 14, y: 2, solid: 'bottom' },  // 薬の棚
    { tile: ['school_in', 7, 9, 1, 2], x: 15, y: 2, solid: 'bottom' },  // 本棚
    { tile: ['school_in', 5, 19], x: 5, y: 1, solid: false },           // 時計
    { tile: ['school_in', 7, 34, 1, 2], x: 15, y: 10 },                 // 観葉植物
  ],
  events: [
    {
      id: 'intro', x: 0, y: 0,
      pages: [
        { trigger: 'auto', list: [
          ['fadeout', 1],
          ['fadein', 40],
          ['text', '', '……気がつくと、保健室にいた。'],
          ['balloon', 'player', '!'],
          ['text', 'ハル', '今日は図書室でカードを探す約束だった。\nまずは机の上を見てみよう。'],
          ['self', 'A', true],
        ] },
        { cond: { self: 'A' }, list: [] },
      ],
    },
    {
      id: 'desk', x: 9, y: 3,
      pages: [
        { list: [
          ['text', '', '机の上にメモがある。'],
          ['getItem', 'memo'],
          ['text', '', '（メニューの「アイテム」から読める。\n　Qキー／★ボタンで、集めたカードの枚数がわかる）'],
          ['self', 'A', true],
        ] },
        { cond: { self: 'A' }, list: [
          ['text', '', '机の上はもう片づいている。'],
        ] },
      ],
    },
    {
      id: 'bed', x: 2, y: 5,
      pages: [
        { list: [
          ['text', 'ハル', 'もう少し寝ていたい……'],
          ['choice', ['寝る', 'やめておく'], [
            [['fadeout', 30], ['wait', 40], ['fadein', 30], ['text', 'ハル', '……よし、目が覚めた。']],
            [],
          ], { cancel: 1 }],
        ] },
      ],
    },
    {
      id: 'card1', x: 11, y: 9,
      pages: [
        { char: { shape: 'card', color: '#e3a33b' }, list: [
          ['getItem', 'card1'],
          ['self', 'A', true],
          ['common', 'getCard'],
        ] },
        { cond: { self: 'A' }, list: [] },
      ],
    },
    {
      // 扉：ぶつかると廊下へ戻る
      id: 'door', x: 12, y: 2,
      pages: [
        { trigger: 'touch', priority: 'same', list: [
          ['se', 'door'],
          ['back'],
        ] },
      ],
    },
  ],
});
