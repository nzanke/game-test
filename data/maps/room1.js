// room1.js — 自室（ゲームの始まり）
G.defineMap('room1', {
  name: '自室',
  // 17列×13行。記号の意味は legend（なければ system.js と既定値）
  tiles: [
    '#################',
    '#################',
    '#BB.........KKK.#',
    '#BB.............#',
    '#BB.............#',
    '#...............#',
    '#.......rr......#',
    '#.......rr......#',
    '#...............#',
    '#...............#',
    '#ss.............#',
    '#ss.............#',
    '########D########',
  ],
  legend: {
    'B': { solid: true, color: '#8fa6c9' }, // ベッド
    'K': { solid: true, color: '#9a6b42' }, // 机
  },
  events: [
    {
      id: 'intro', x: 0, y: 0,
      pages: [
        { trigger: 'auto', list: [
          ['fadeout', 1],
          ['fadein', 40],
          ['text', '', '……朝だ。'],
          ['balloon', 'player', '!'],
          ['text', 'ハル', '今日は図書室でカードを探す約束だった。\nまずは机の上を見てみよう。'],
          ['self', 'A', true],
        ] },
        { cond: { self: 'A' }, list: [] },
      ],
    },
    {
      id: 'desk', x: 13, y: 2,
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
      id: 'bed', x: 2, y: 4,
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
      id: 'card1', x: 5, y: 9,
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
      id: 'door', x: 8, y: 12,
      pages: [
        { trigger: 'touch', list: [
          ['se', 'door'],
          ['transfer', 'hall', 8, 6, 'up'],
        ] },
      ],
    },
  ],
});
