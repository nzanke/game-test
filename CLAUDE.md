# game-test

ブラウザで動く自作のアドベンチャー／RPGエンジンと、その中身。ビルドは不要で、`index.html` を開けば動く。GitHub Pages で公開している。

- 中身（部屋・会話・アイテム）は `data/` に書く。書式は `DATA_FORMAT.md` に全部ある
- エンジンは `engine/`（core 入力・音・ループ／world 部屋・キャラ・イベント起動・条件・描画／interpreter 命令／ui 文章・選択肢・メニュー・セーブ・タイトル）
- 新しい命令は `engine/interpreter.js` の `CMD` に足し、`DATA_FORMAT.md` にも書く。条件を足したら `tools/check.js` の `COND_KEYS` も直す
- データを変えたら必ず `node tools/check.js` を通す
- マップなどのファイルを足したら `files.js` の scripts に1行足す（index.html は固定で、開くたびに files.js を新しく読んでから各ファイルを読み込む）
- 校舎（廊下8枚と部屋の型）は `tools/gen_school.py` で生成する。生成した `data/maps/school_*.js` は直接直さず、スクリプトを直して作り直す。お話のイベントは `data/story.js` に `G.addEvents` で足す（`at: '扉の名前'` で位置を決められる）。見取り図の施設名のうち学校が特定されそうな名前は一般的な名前に変える
- 参考にした市販ゲームのファイル（データ・画像・音・シナリオ）はこのリポジトリに入れない
- タイル素材（ドット絵世界）は二次配布禁止。元のPNGは入れず、`tools/encode_tileset.py` で変換した `data/tilesets/*.js` だけを入れる。タイトル画面の著作権表示（system.js の credits）は消さない
- キャラの歩行グラフィックは「イラストをドットに落とし込んだ」描き方：6倍の大きさでグラデーション・柔らかい影と光・描き込んだアニメ風の目でイラストとして描き、64×96pxに縮める。約4頭身（デフォルメ控えめ）、やや上から見下ろす角度。ユイは `tools/sprites/make_trial.py`（`img/chars/trial.png`）、ハルは `tools/sprites/make_haru.py`（`img/chars/haru.png`。描画の道具は make_trial.py のものを使う）。新しいキャラも同じ道具で描く。参考が既存作品のキャラのときは写さない。直したらスクリプトを動かして画像を作り直す
- 字体：ゲームの文字は M+ 1m（`fonts/mplus-1m-regular.ttf`、M+ FONTS は自由に使用・配布できる）。`G.font()` と css/style.css で指定している。収録外の文字（♪など）は端末のフォントになる
- 公開は gh-pages ブランチから。更新したら、まず `python3 tools/stamp.py`（files.js の版の番号を新しくする。ブラウザが古いファイルを使い回して新旧が混ざるのを防ぐ）、コミットして `git push origin main main:gh-pages` で両方に送る。そのあと `gh api repos/nzanke/game-test/actions/runs` で「pages build and deployment」が新しいコミットで completed success になったのを確かめてから報告する。ビルドが走らないときは空のコミットを送り直す（Pages 設定のAPIは作業環境から使えない）
- やりとりと説明は日本語で
