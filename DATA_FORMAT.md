# データの書き方

ゲームの中身は `data/` のファイルにすべて書く。エンジン（`engine/`）は触らなくてよい。
書いたら `node tools/check.js` で書き間違いを調べる。

## ファイルの分かれ方

| ファイル | 中身 |
|---|---|
| `data/system.js` | タイトル、開始位置、主人公、メニュー、共通のマス記号 |
| `data/items.js` | アイテムとカード |
| `data/commons.js` | コモンイベント（どこからでも呼べる命令のまとまり） |
| `data/maps/*.js` | 部屋（マップ）1つにつき1ファイル |

マップを足したら、`index.html` の「データ」の所に `<script src="data/maps/○○.js"></script>` を1行足す。

## マップ

```js
G.defineMap('room1', {
  name: '自室',            // セーブ画面に出る名前
  tiles: [                 // 17文字×13行。1文字が1マス（48px）
    '#################',
    ...
  ],
  legend: {                // このマップだけのマス記号
    'B': { solid: true, color: '#8fa6c9' },  // solid: true で通れない
  },
  bg: 'img/rooms/room1.png',  // （任意）一枚絵の背景。816×624。マス記号は通れるかどうかだけに使われる
  bgm: 'audio/bgm/xxx.ogg',   // （任意）この部屋のBGM。null で止める
  events: [ ... ],
});
```

既定のマス記号：`#` 壁、`.` 床、` `（空白）黒い通れない所、`D` 扉の床。
`system.js` の `legend` に書いた記号は全マップで使える。

## イベント

```js
{
  id: 'yui', x: 12, y: 4, dir: 'left',
  pages: [
    { cond: ..., trigger: 'action', char: {...}, list: [ 命令, 命令, ... ] },
    { cond: ..., ... },
  ],
}
```

- **ページは「条件を満たすもののうち、いちばん後ろ」が選ばれる。** どれも満たさなければ、そのイベントは無いのと同じ
- `trigger`：`action`（決定キーで調べる。省略時）／`touch`（触れたら）／`auto`（自動で1回ずつ。終わるまで操作できない）／`parallel`（並列。くり返し動き続ける）
- `char`：見た目。`{ shape: 'person', color, hair }` 人／`'box'` 箱／`'card'` カード／`'icon', icon: '★'` 文字／`img: 'img/chars/x.png'` 画像。省略すると見えないイベント
- `priority`：`below`（下。上を歩ける）／`same`（通れない）／`above`（上）。省略時は、見た目があれば `same`、なければ `below`
- `through: true`：すり抜け　`fixDir: true`：話しかけても振り向かない　`sensor: false`：近づいても「！」を出さない
- `autoMove: ['left', 'wait:60', 'right']`：自律移動（くり返し）

調べ方のきまり：正面のマスのイベントを調べる。見えない「below」のイベントは、その上に乗ると調べられる（ただし壁など通れないマスにある場合は正面から調べられる）。

## 条件（cond）

```js
{ switch: '名前' }                 // スイッチがON
{ switch: '名前', is: false }      // OFF（is: false はどの条件にも付けられる）
{ self: 'A' }                      // このイベントのセルフスイッチA
{ var: ['cards', '>=', 3] }        // 変数（== != >= <= > <）。値に '$名前' で別の変数
{ item: 'key' }                    // アイテムを持っている（count: 2 で2個以上）
{ dir: 'up' }                      // 主人公の向き
[ 条件, 条件 ]                     // すべて満たす
{ any: [ 条件, 条件 ] }            // どれかを満たす
{ not: 条件 }
```

## 命令（list の中身）

1つの命令は `['命令名', 引数, ...]`。フレームは1/60秒。

**文章**

| 命令 | 例 |
|---|---|
| 文章（名前、本文） | `['text', 'ユイ', 'おはよう。\n2行目']` |
| 選択肢（直前の文章と一緒に出る） | `['choice', ['はい', 'いいえ'], [[はいの命令...], [いいえの命令...]], { cancel: 1, pos: 'right' }]` |
| 画面上の短い知らせ | `['popup', 'セーブしました']` |

文中の `{v:変数名}` は変数の値、`{item:ID}` はアイテム名、`{player}` は主人公の名前になる。
`cancel` は戻るキーで選ばれる番号（0から。`'last'` で最後）、`pos` は `right`／`center`／`left`。

**流れ**

| 命令 | 例 |
|---|---|
| 条件分岐 | `['if', { item: 'key' }, [成り立つとき...], [成り立たないとき...]]` |
| くり返し／抜ける | `['loop', [ ... ['break'] ... ]]` |
| ウェイト | `['wait', 60]` |
| コモンイベントを呼ぶ | `['common', 'getCard']` |
| イベントを終える | `['end']` |
| このイベントを一時消去 | `['erase']`（部屋を出入りすると戻る） |
| タイトルへ戻る | `['title']` |
| メニューの画面を開く | `['openMenu', 'save']` |
| JavaScriptを直接書く | `['script', (G, S, ev) => { S.vars.x = 1; }]` |

**スイッチ・変数・アイテム**

| 命令 | 例 |
|---|---|
| スイッチ | `['switch', 'gotKey', true]`（名前を配列にすると一度に複数） |
| 変数 | `['var', 'cards', '+', 1]`（演算は = + - * / %。`['var', 'r', 'rand', [1, 6]]` で乱数） |
| セルフスイッチ | `['self', 'A', true]`（3つ目の引数に別イベントのidも書ける） |
| アイテムを増減（黙って） | `['item', 'key', -1]` |
| アイテムを手に入れる（音と知らせつき） | `['getItem', 'card1']` |

**移動・キャラクター**（対象は `'player'`／`'this'`（このイベント）／イベントのid）

| 命令 | 例 |
|---|---|
| 場所移動 | `['transfer', 'hall', 8, 6, 'up']`（5つ目に `{ fade: false }` で暗転なし） |
| 移動ルート | `['move', 'this', ['left', 'left', 'face:down', 'wait:30'], true]` |
| フキダシ | `['balloon', 'player', '!']`（中の文字は自由） |

移動ルートで使えるもの：`up` `down` `left` `right` `face:向き` `wait:フレーム` `speed:数`（4が普通、8が速い） `through:on/off` `hide` `show` `facePlayer` `random` `toward`（主人公に近づく）

**ピクチャ**（番号が大きいほど手前）

| 命令 | 例 |
|---|---|
| 表示 | `['pic', 1, { src: 'img/pictures/a.png', x: 408, y: 300 }]` |
| 仮の絵（色の板と文字） | `['pic', 1, { text: '立ち絵', color: '#7c5aa6', w: 280, h: 440 }]` |
| 文字だけ | `['pic', 2, { text: '第一章', fontSize: 48 }]` |
| 移動・変化 | `['picMove', 1, { x: 300, opacity: 0, scale: 1.2 }, 30, true]`（フレーム数、終わるまで待つか） |
| 揺らす | `['picShake', 1, 12, 30]` |
| 消す | `['picErase', 1]` |

ピクチャの項目：`x` `y`（既定は画面中央） `origin`（`center` 既定／`topleft`） `opacity`（0〜1） `scale` `w` `h` `color` `text` `fontSize` `textColor`

**画面の演出**

| 命令 | 例 |
|---|---|
| 画面を揺らす | `['shake', 5, 30]` |
| フラッシュ | `['flash', [255, 255, 255], 30]` |
| 色調（かぶせる色と濃さ） | `['tint', [0, 0, 40, 0.4], 30]`（戻すときは `[0, 0, 0, 0]`） |
| フェードアウト／イン | `['fadeout', 30]` `['fadein', 30]` |

**音**

| 命令 | 例 |
|---|---|
| 効果音 | `['se', 'item']`（仮の電子音：cursor ok cancel buzzer item door shock talk magic。ファイル名も可） |
| BGM | `['bgm', 'audio/bgm/xxx.ogg']`（`null` で止める） |

## アイテム（data/items.js）

```js
key:   { name: '図書室の鍵', desc: '説明文' },
memo:  { name: 'メモ', desc: '...', common: 'readMemo' },   // メニューで使うとコモンが動く
card1: { type: 'card', name: '朝のカード', color: '#e3a33b', img: 'img/cards/1.png', desc: '...' },
```

`type: 'card'` はカード画面に並ぶ（定義した順）。`hidden: true` はアイテム画面に出さない。

## 操作

| 操作 | キーボード | スマホ |
|---|---|---|
| 移動 | 矢印／WASD（Shiftで速く） | 十字ボタン |
| 決定 | Z／Enter／Space | 決定・画面タップ |
| 戻る・メニュー | X／Esc | 戻る |
| コモン呼び出し（system.js の specialKey） | Q | ★ |
| ログ | L | ログ |
| 文章ウィンドウを隠す | H | － |
