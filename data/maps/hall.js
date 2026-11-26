// hall.js — 廊下
G.defineMap('hall', {
  name: '廊下',
  tiles: [
    '#111711111117111#',
    '#222822222228222#',
    '#333933333339333#',
    '#,,,,,,,,,,,,,,,#',
    '#,,,,,,,,,,,,,,,#',
    '#,,,,,,,,,,,,,,,#',
    '#,,,,,,,,,,,,,,,#',
    '#,,,,,,,,,,,,,,,#',
    '#################',
    '#################',
    '#################',
    '#################',
    '#################',
  ],
  objects: [
    { tile: ['school_in', 6, 20, 1, 2], x: 7, y: 2, solid: 'bottom' },  // ロッカー
    { tile: ['school_in', 6, 20, 1, 2], x: 8, y: 2, solid: 'bottom' },  // ロッカー
    { tile: ['school_in', 7, 20, 1, 2], x: 9, y: 2, solid: 'bottom' },  // ロッカー（灰）
    { tile: ['school_in', 7, 34, 1, 2], x: 1, y: 2, solid: 'bottom' },  // 観葉植物
    { tile: ['school_in', 7, 34, 1, 2], x: 15, y: 2, solid: 'bottom' }, // 観葉植物
  ],
  events: [
    {
      id: 'toRoom', x: 4, y: 2,
      pages: [
        { trigger: 'touch', priority: 'same', list: [['se', 'door'], ['transfer', 'room1', 12, 3, 'down']] },
      ],
    },
    {
      // 図書室の扉：鍵がないと開かない
      id: 'libDoor', x: 12, y: 2,
      pages: [
        { trigger: 'touch', priority: 'same', list: [
          ['if', { item: 'key' }, [
            ['se', 'door'],
            ['transfer', 'library', 8, 3, 'down'],
          ], [
            ['se', 'buzzer'],
            ['text', '', '図書室の扉には鍵がかかっている。'],
          ]],
        ] },
      ],
    },
    {
      id: 'yui', x: 10, y: 5, dir: 'left',
      pages: [
        { char: { shape: 'person', color: '#d0587a', hair: '#7a3b1e' }, autoMove: ['wait:90', 'face:down', 'wait:90', 'face:left'], list: [
          ['text', 'ユイ', 'おはよう、ハル。カード探し、手伝ってくれるの？'],
          ['choice', ['もちろん', 'あとでね'], [
            [
              ['text', 'ユイ', 'ありがとう！　これ、図書室の鍵。'],
              ['getItem', 'key'],
              ['text', 'ユイ', 'カードは全部で3枚。見つけたら見せてね。'],
              ['self', 'A', true],
            ],
            [
              ['balloon', 'this', '…'],
              ['text', 'ユイ', 'そっか……気が向いたら声をかけてね。'],
            ],
          ]],
        ] },
        { cond: { self: 'A' }, char: { shape: 'person', color: '#d0587a', hair: '#7a3b1e' }, list: [
          ['text', 'ユイ', 'いま {v:cards} 枚だね。あと少し！'],
        ] },
        // カードが3枚そろったら（後ろのページほど優先）
        { cond: [{ self: 'A' }, { var: ['cards', '>=', 3] }], char: { shape: 'person', color: '#d0587a', hair: '#7a3b1e' }, list: [
          ['balloon', 'this', '♪'],
          ['text', 'ユイ', 'すごい、3枚そろったんだ！'],
          ['flash', [255, 240, 200], 40],
          ['pic', 1, { text: '朝　風　夜', color: '#2d2a4a', w: 420, h: 160, fontSize: 40, opacity: 0, scale: 0.6 }],
          ['picMove', 1, { opacity: 1, scale: 1 }, 30],
          ['text', 'ユイ', 'カードを並べると……ほら、一日がひとめぐりする。'],
          ['picMove', 1, { opacity: 0 }, 30],
          ['picErase', 1],
          ['text', '', '（ここまでが動作確認用のお話です）'],
          ['title'],
        ] },
      ],
    },
    {
      id: 'card2', x: 2, y: 7,
      pages: [
        { char: { shape: 'card', color: '#3bb39a' }, list: [
          ['getItem', 'card2'],
          ['self', 'A', true],
          ['common', 'getCard'],
        ] },
        { cond: { self: 'A' }, list: [] },
      ],
    },
    {
      // 調べるだけのもの（見えないイベント）
      id: 'window', x: 14, y: 2,
      pages: [{ list: [['text', '', '窓の外はよく晴れている。']] }],
    },
  ],
});
