# game-test

ブラウザで動く自作のアドベンチャー／RPGエンジンと、その中身。ビルドは不要で、`index.html` を開けば動く。GitHub Pages で公開している。

- 中身（部屋・会話・アイテム）は `data/` に書く。書式は `DATA_FORMAT.md` に全部ある
- エンジンは `engine/`（core 入力・音・ループ／world 部屋・キャラ・イベント起動・条件・描画／interpreter 命令／ui 文章・選択肢・メニュー・セーブ・タイトル）
- 新しい命令は `engine/interpreter.js` の `CMD` に足し、`DATA_FORMAT.md` にも書く。条件を足したら `tools/check.js` の `COND_KEYS` も直す
- データを変えたら必ず `node tools/check.js` を通す
- マップを足したら `index.html` に `<script>` を1行足す
- 参考にした市販ゲームのファイル（データ・画像・音・シナリオ）はこのリポジトリに入れない
- タイル素材（ドット絵世界）は二次配布禁止。元のPNGは入れず、`tools/encode_tileset.py` で変換した `data/tilesets/*.js` だけを入れる。タイトル画面の著作権表示（system.js の credits）は消さない
- キャラの歩行グラフィックは `tools/sprites/make_chars.py` で一から描いている（1コマ48px・等倍。顔・髪・目・胴などの部品を図形で描き、輪郭は自動。色はパレット）。男子は目を描かない、女子は大きな目、という描き分けが好み。直したらこれを動かして `img/chars/*.png` を作り直す。参考素材は写さない
- 字体：半角英数は BIZ UDGothic、日本語は BIZ UDPGothic（`G.font()` が両方を指定する）
- 公開は gh-pages ブランチから。更新したら `git push origin main main:gh-pages` で両方に送る（Pages 設定のAPIは作業環境から使えない）
- やりとりと説明は日本語で
