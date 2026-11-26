// escape.js — 大学の夕方の空き教室（ひと部屋。いまはシステムとデザインの土台づくり用で、謎解きは入れていない）
// 会話は data/CHARACTERS.md の設定と口調に合わせる
// 床は横11×縦7マス（x 3〜13、y 4〜10）。上の3段が壁、扉は右上（x 13）
const I = 'school_in';

G.defineMap('escape', {
  name: '夕方の空き教室',
  tiles: [  // 17×13マスの地図のまん中に、床が横11×縦7マスの部屋（まわりは暗い外側）
    '#################',
    '###UUUUUUUUUU7###',
    '###VVVVVVVVVV8###',
    '###WWWWWWWWWW9###',
    '###QQQQQQQQQQP###',  // 床は灰色のPタイル（記号 Q）、扉の前にゴムマット（記号 P）
    '###QQQQQQQQQQQ###',
    '###QQQQQQQQQQQ###',
    '###QQQQQQQQQQQ###',
    '###QQQQQQQQQQQ###',
    '###QQQQQQQQQQQ###',
    '###QQQQQQQQQQQ###',
    '#################',
    '#################',
  ],
  objects: [
    // 壁は自作のタイル（記号 U・V・W）。黒板は壁の2段目に置くと目の高さになる
    { tile: ['objects', 0, 6, 3, 2], x: 4, y: 2, solid: false },       // 黒板
    { tile: ['objects', 0, 6, 3, 2], x: 7, y: 2, solid: false },       // 黒板
    { tile: ['objects', 7, 0, 1, 1], x: 11, y: 2, solid: false },      // 掛け時計
    { tile: ['objects', 3, 6, 1, 1], x: 13, y: 10 },                   // 観葉植物
    // 自作の家具・小物（data/tilesets/objects.js。スチール製）
    { tile: ['objects', 4, 0, 1, 2], x: 3, y: 3, solid: 'bottom' },    // スチール書庫
    { tile: ['objects', 3, 0, 1, 2], x: 4, y: 3, solid: 'bottom' },    // ロッカー
    { tile: ['objects', 0, 0, 1, 2], x: 10, y: 3, solid: 'bottom' },   // 自販機（赤）
    { tile: ['objects', 7, 1, 1, 1], x: 11, y: 4 },                    // ごみ箱
    { tile: ['objects', 5, 2, 2, 1], x: 6, y: 5 },                     // 教卓
    // 長机（3人掛け）と椅子（後ろ向き）：左右2列×2段
    { tile: ['objects', 0, 2, 3, 1], x: 4, y: 7 }, { tile: ['objects', 0, 2, 3, 1], x: 9, y: 7 },
    { tile: ['objects', 0, 2, 3, 1], x: 4, y: 9 }, { tile: ['objects', 0, 2, 3, 1], x: 9, y: 9 },
    { tile: ['objects', 0, 3, 1, 1], x: 4, y: 8 }, { tile: ['objects', 0, 3, 1, 1], x: 5, y: 8 }, { tile: ['objects', 0, 3, 1, 1], x: 6, y: 8 },
    { tile: ['objects', 0, 3, 1, 1], x: 9, y: 8 }, { tile: ['objects', 0, 3, 1, 1], x: 10, y: 8 }, { tile: ['objects', 0, 3, 1, 1], x: 11, y: 8 },
    { tile: ['objects', 0, 3, 1, 1], x: 4, y: 10 }, { tile: ['objects', 0, 3, 1, 1], x: 5, y: 10 }, { tile: ['objects', 0, 3, 1, 1], x: 6, y: 10 },
    { tile: ['objects', 0, 3, 1, 1], x: 9, y: 10 }, { tile: ['objects', 0, 3, 1, 1], x: 10, y: 10 }, { tile: ['objects', 0, 3, 1, 1], x: 11, y: 10 },
  ],
  events: [
    {
      id: 'intro', x: 0, y: 0,
      pages: [
        { trigger: 'auto', list: [
          ['fadeout', 1],
          ['wait', 20],
          ['fadein', 40],
          ['text', '', '夕方の空き教室。\nゼミの片づけを手伝っていたら、すっかり日が暮れてしまった。'],
          ['text', 'かなで', 'ぼたんちゃん、まだ帰らないの？\n寮の夕飯、なくなっちゃうわよ。'],
          ['text', 'ぼたん', 'はい、もう少しだけ……。\n先輩こそ、論文のほうは大丈夫なんですかぁ？'],
          ['text', 'かなで', '……それは聞かないでほしいわね。'],
          ['self', 'A', true],
        ] },
        { cond: { self: 'A' }, list: [] },
      ],
    },
    {
      id: 'kanade', x: 9, y: 6,
      pages: [
        { char: { sprite: 'img/chars/kanade_chibi.png', dir: 'left' }, list: [
          ['move', 'this', ['facePlayer'], true],
          ['var', 'talk', 'rand', [1, 4]],
          ['if', { var: ['talk', '==', 1] }, [
            ['text', 'かなで', '一服したいところだけど、ここは禁煙だもの。\n我慢するわ。'],
          ]],
          ['if', { var: ['talk', '==', 2] }, [
            ['text', 'ぼたん', '先輩、帰りに一杯どうですかぁ？'],
            ['text', 'かなで', '一杯だけ、なんて言わないでね。\nわたし、すぐ酔っちゃうんだもの。'],
          ]],
          ['if', { var: ['talk', '==', 3] }, [
            ['text', 'かなで', 'ぼたんちゃん、上着ちゃんと持ってきた？\n夜は冷えるわよ。'],
            ['text', 'ぼたん', 'はい、持ってきましたよぉ。\n先輩はやさしいですねぇ。'],
          ]],
          ['if', { var: ['talk', '==', 4] }, [
            ['text', 'かなで', '……なに、じっと見て。\n顔に何かついてるかしら。'],
            ['text', 'ぼたん', 'いえ、先輩と一緒だと落ち着くなぁって。'],
            ['text', 'かなで', '……そういうこと、さらっと言うのね。'],
          ]],
        ] },
      ],
    },
    { id: 'board', x: 5, y: 3, pages: [{ list: [
      ['text', '', '黒板。消し忘れた板書が残っている。'],
      ['text', 'ぼたん', '先輩の専門の話ですかねぇ。\nわたしにはまだ難しいです。'],
    ] }] },
    { id: 'clock', x: 11, y: 3, pages: [{ list: [
      ['text', '', '壁の時計。もうすぐ18時だ。'],
      ['text', 'ぼたん', '寮の近くの居酒屋、今日は半額の日でしたねぇ……。'],
    ] }] },
    { id: 'shelf', x: 3, y: 4, pages: [{ list: [
      ['text', '', 'スチールの書庫。ガラス戸の奥に、分厚いファイルと専門書が並んでいる。'],
      ['text', 'ぼたん', '先輩、これ全部読んだんですかぁ？'],
    ] }] },
    { id: 'desk', x: 6, y: 5, pages: [{ list: [
      ['text', '', '教卓。ゼミの資料が積んである。'],
    ] }] },
    { id: 'seat', x: 5, y: 7, pages: [{ list: [
      ['text', '', '机。だれかの飲みかけの缶コーヒーが置きっぱなしだ。'],
      ['text', 'ぼたん', 'お酒だったらよかったのになぁ。'],
    ] }] },
    { id: 'plant', x: 13, y: 10, pages: [{ list: [
      ['text', '', '教室のすみの観葉植物。'],
      ['text', 'ぼたん', 'ちゃんとお水もらえてるんですかねぇ。'],
    ] }] },
    { id: 'vending', x: 10, y: 4, pages: [{ list: [
      ['text', '', '飲み物の自販機。'],
      ['text', 'ぼたん', 'お酒は……売ってないですよねぇ。'],
    ] }] },
    { id: 'locker', x: 4, y: 4, pages: [{ list: [
      ['text', '', 'スチールのロッカー。名札は空白のままだ。'],
    ] }] },
    { id: 'trash', x: 11, y: 4, pages: [{ list: [
      ['text', '', 'ごみ箱。丸めたレポート用紙が入っている。'],
      ['text', 'ぼたん', 'だれかの書きかけですかねぇ。'],
    ] }] },
    { id: 'door', x: 13, y: 3, pages: [{ list: [
      ['text', 'ぼたん', 'まだ先輩とお話ししていたいなぁ。'],
    ] }] },
  ],
});
