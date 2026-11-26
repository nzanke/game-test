// story.js — お話のイベント（生成した校舎のマップに足す）
// at: '扉の名前' と書くと、その扉の位置を基準に置ける（dx・dy でずらす）。扉の名前は data/maps/school_doors.js

// 本館1階：ユイと2枚目のカード
G.addEvents('main1f', [
  {
    id: 'yui', at: '保健室', dx: -5, dy: 3, dir: 'left',
    pages: [
      { char: { sprite: 'img/chars/yui.png' }, autoMove: ['wait:90', 'face:down', 'wait:90', 'face:left'], list: [
        ['text', 'ユイ', 'おはよう、ハル。カード探し、手伝ってくれるの？'],
        ['choice', ['もちろん', 'あとでね'], [
          [
            ['text', 'ユイ', 'ありがとう！　これ、図書室の鍵。'],
            ['getItem', 'key'],
            ['text', 'ユイ', '図書室は特別教室棟の3階。\nこの廊下の渡り廊下から行けるよ。'],
            ['text', 'ユイ', 'カードは全部で3枚。見つけたら見せてね。'],
            ['self', 'A', true],
          ],
          [
            ['balloon', 'this', '…'],
            ['text', 'ユイ', 'そっか……気が向いたら声をかけてね。'],
          ],
        ]],
      ] },
      { cond: { self: 'A' }, char: { sprite: 'img/chars/yui.png' }, list: [
        ['text', 'ユイ', 'いま {v:cards} 枚だね。図書室は特別教室棟の3階だよ。'],
      ] },
      { cond: [{ self: 'A' }, { var: ['cards', '>=', 3] }], char: { sprite: 'img/chars/yui.png' }, list: [
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
    id: 'card2', at: '進路室', dx: 0, dy: 4,
    pages: [
      { char: { shape: 'card', color: '#3bb39a' }, list: [
        ['getItem', 'card2'],
        ['self', 'A', true],
        ['common', 'getCard'],
      ] },
      { cond: { self: 'A' }, list: [] },
    ],
  },
]);

// 特別教室棟3階：図書室の扉（鍵がないと開かない）
G.addEvents('annex3f', [
  {
    id: 'libDoor', at: '図書室',
    pages: [
      { trigger: 'touch', priority: 'same', sensor: false, list: [
        ['if', { item: 'key' }, [
          ['se', 'door'],
          ['enter', 'library', 8, 3, 'down', '図書室'],
        ], [
          ['se', 'buzzer'],
          ['text', '', '図書室の扉には鍵がかかっている。'],
        ]],
      ] },
    ],
  },
]);
