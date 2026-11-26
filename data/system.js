// system.js — ゲーム全体の設定
G.defineSystem({
  title: 'ゲームテスト',
  subtitle: '自作エンジンの動作確認用',
  // 最初にいる場所
  start: { map: 'room1', x: 8, y: 8, dir: 'up' },
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
  // 全マップ共通のマス記号（各マップの legend で上書きできる）
  legend: {
    'r': { color: '#b8574e' },               // じゅうたん
    's': { solid: true, color: '#6b4a2e' },  // 本棚
  },
});
