// hall.js — 廊下
G.defineMap('hall', {
  name: '廊下',
  tiles: [
    '#################',
    '#################',
    '#######D#########',
    '#...............#',
    '#...............#',
    '#...............#',
    '#...............#',
    '########D########',
    '                 ',
    '                 ',
    '                 ',
    '                 ',
    '                 ',
  ],
  legend: {
    '.': { color: '#c9b79a' },
  },
  events: [
    {
      id: 'toRoom', x: 8, y: 7,
      pages: [
        { trigger: 'touch', list: [['se', 'door'], ['transfer', 'room1', 8, 11, 'up']] },
      ],
    },
    {
      // 図書室の扉：鍵がないと開かない
      id: 'libDoor', x: 7, y: 2,
      pages: [
        { char: { shape: 'box', color: '#5b3a22' }, trigger: 'touch', list: [
          ['if', { item: 'key' }, [
            ['se', 'door'],
            ['transfer', 'library', 8, 11, 'up'],
          ], [
            ['se', 'buzzer'],
            ['text', '', '鍵がかかっている。'],
          ]],
        ] },
      ],
    },
    {
      id: 'yui', x: 12, y: 4, dir: 'left',
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
      id: 'card2', x: 2, y: 6,
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
      id: 'window', x: 13, y: 2,
      pages: [{ list: [['text', '', '窓の外はよく晴れている。']] }],
    },
  ],
});
