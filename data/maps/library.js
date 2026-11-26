// library.js — 図書室（ピクチャ演出・並列イベント・自律移動の見本）
G.defineMap('library', {
  name: '図書室',
  tiles: [
    '#################',
    '#################',
    '#sssss.....sssss#',
    '#...............#',
    '#sssss.....sssss#',
    '#...............#',
    '#...............#',
    '#.....ttttt.....#',
    '#.....ttttt.....#',
    '#...............#',
    '#...............#',
    '#...............#',
    '########D########',
  ],
  legend: {
    '.': { color: '#bfc7a8' },
    't': { solid: true, color: '#a7804f' }, // 机
  },
  events: [
    {
      id: 'toHall', x: 8, y: 12,
      pages: [{ trigger: 'touch', list: [['se', 'door'], ['transfer', 'hall', 7, 3, 'down']] }],
    },
    {
      id: 'oldBook', x: 3, y: 4,
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
      id: 'card3', x: 14, y: 3,
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
      id: 'cat', x: 4, y: 10,
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
