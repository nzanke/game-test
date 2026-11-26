"""公開の前に動かす：python3 tools/stamp.py

files.js の版の番号 v を書き換える。index.html は開くたびに files.js を新しく読み、
この番号をつけて各ファイルを読み込むので、ブラウザが古いファイルを使い回さない（画像も engine/core.js の G.img で同じ番号をつける）。
"""
import re
import time
from pathlib import Path

p = Path(__file__).resolve().parent.parent / 'files.js'
v = time.strftime('%Y%m%d%H%M%S')
s = p.read_text(encoding='utf-8')
s = re.sub(r"v: '[^']*'", f"v: '{v}'", s, count=1)
p.write_text(s, encoding='utf-8')
print('版の番号', v)
