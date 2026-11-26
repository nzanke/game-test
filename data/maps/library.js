// library.js — 図書室（ピクチャ演出・並列イベント・自律移動の見本）
G.defineMap('library', {
  name: '図書室',
  exit: { door: '図書室' },
  tiles: [
    '#444444474444444#',
    '#555555585555555#',
    '#666666696666666#',
    '#:::::::::::::::#',
    '#:::::::::::::::#',
    '#:::::::::::::::#',
    '#:::::::::::::::#',
    '#:::::::::::::::#',
    '#:::::::::::::::#',
    '#:::::::::::::::#',
    '#:::::::::::::::#',
    '#:::::::::::::::#',
    '#################',
  ],
  objects: [
    { tile: ['school_in', 7, 9, 1, 2], x: 1, y: 2, solid: 'bottom' },   // 本棚（壁ぎわ）
    { tile: ['school_in', 7, 9, 1, 2], x: 2, y: 2, solid: 'bottom' },
    { tile: ['school_in', 7, 9, 1, 2], x: 3, y: 2, solid: 'bottom' },
    { tile: ['school_in', 0, 39, 3, 2], x: 11, y: 2, solid: 'bottom' }, // 司書の机
    { tile: ['school_in', 5, 38], x: 15, y: 3 },                        // 地球儀
    { tile: ['school_in', 2, 18, 3, 2], x: 1, y: 5 },                   // 低い本棚
    { tile: ['school_in', 2, 18, 3, 2], x: 5, y: 5 },
    { tile: ['school_in', 2, 18, 3, 2], x: 9, y: 5 },
    { tile: ['school_in', 2, 18, 3, 2], x: 13, y: 5 },
    { tile: ['school_in', 0, 42, 3, 2], x: 6, y: 9 },                   // 閲覧机
    { tile: ['school_in', 0, 42, 3, 2], x: 10, y: 9 },
    { tile: ['school_in', 5, 19], x: 5, y: 0, solid: false },           // 時計
  ],
  events: [
    {
      id: 'toHall', x: 8, y: 2,
      pages: [{ trigger: 'touch', priority: 'same', list: [['se', 'door'], ['back']] }],
    },
    {
      id: 'oldBook', x: 2, y: 6,
      pages: [
        { list: [
          ['text', '', '古い本が一冊だけ、逆さまに差してある。'],
          ['choice', ['開いてみる', 'やめておく'], [
            [
              ['se', 'magic'],
              ['flash', [255, 255, 210], 30],
              ['pic', 1, { text: '立ち絵（仮）', color: '#7c5aa6', w: 280, h: 440, x: 408, y: 300, opacity: 0 }],
              ['picMove', 1, { opacity: 1, y: 280 }, 30],
              ['text', '謎の声', '……やっと開いてくれたね。'],
              ['se', 'shock'],
              ['picShake', 1, 12, 30],
              ['shake', 6, 30],
              ['text', '謎の声', '本の間にカードを隠しておいたよ。\n3枚そろえて、ユイに見せてあげて。'],
              ['picMove', 1, { opacity: 0, y: 300 }, 30],
              ['picErase', 1],
              ['self', 'A', true],
              ['switch', 'bookOpened', true],
            ],
            [],
          ]],
        ] },
        { cond: { self: 'A' }, list: [['text', '', 'もう何も起こらない。']] },
      ],
    },
    {
      // 本を開くまでカードは出てこない（ページの条件がどれも合わないと、イベントは無いのと同じ）
      id: 'card3', x: 14, y: 8,
      pages: [
        { cond: { switch: 'bookOpened' }, char: { shape: 'card', color: '#5a5fd6' }, list: [
          ['getItem', 'card3'],
          ['self', 'A', true],
          ['common', 'getCard'],
        ] },
        { cond: { self: 'A' }, list: [] },
      ],
    },
    {
      // 自律移動する猫
      id: 'cat', x: 3, y: 11,
      pages: [
        { char: { shape: 'box', color: '#444', label: '猫' }, autoMove: ['right', 'wait:40', 'right', 'wait:60', 'left', 'wait:40', 'left', 'wait:60'], list: [
          ['balloon', 'this', '♪'],
          ['text', '猫', 'にゃあ。'],
        ] },
      ],
    },
    {
      // 並列イベント：ときどき明かりがまたたく
      id: 'lights', x: 0, y: 0,
      pages: [
        { trigger: 'parallel', list: [
          ['wait', 300],
          ['tint', [0, 0, 30, 0.25], 20],
          ['tint', [0, 0, 0, 0], 20],
        ] },
      ],
    },
  ],
});
