// items.js — アイテムとカード
// type: 'card' はカード画面に並ぶ。common を書くと、メニューで使ったときにそのコモンイベントが動く。
G.defineItems({
  key:  { name: '図書室の鍵', desc: '古びた真ちゅうの鍵。図書室の扉に合いそうだ。' },
  memo: { name: 'メモ', desc: '「カードは3枚。部屋・廊下・図書室に1枚ずつ」と書いてある。', common: 'readMemo' },

  card1: { type: 'card', name: '朝のカード', color: '#e3a33b', desc: '自室で見つけた。ほんのり温かい。' },
  card2: { type: 'card', name: '風のカード', color: '#3bb39a', desc: '廊下の隅に落ちていた。' },
  card3: { type: 'card', name: '夜のカード', color: '#5a5fd6', desc: '図書室の本の間に挟まっていた。' },
});
