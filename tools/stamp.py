"""公開の前に動かす：python3 tools/stamp.py

index.html の自前のファイル（js・css）の後ろに ?v=版の番号 をつけ直す。
ブラウザが古いファイルを使い回すのを防ぐため。画像もこの番号で読み直される（engine/core.js の G.img）。
"""
import re
import time
from pathlib import Path

p = Path(__file__).resolve().parent.parent / 'index.html'
v = time.strftime('%Y%m%d%H%M%S')
s = p.read_text(encoding='utf-8')
s = re.sub(r'((?:src|href)="(?!https?:)[^"?]+\.(?:js|css))(\?v=[^"]*)?"', lambda m: f'{m.group(1)}?v={v}"', s)
p.write_text(s, encoding='utf-8')
print('版の番号', v)
