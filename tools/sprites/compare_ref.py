"""手本（RPGツクールMVの標準キャラ）と、make_chibi.py で作ったキャラを1ドット単位で比べる道具。
手本の画像はリポジトリに入れない。使うときに場所を渡す。

使い方:
  python3 -I tools/sprites/compare_ref.py 手本.png 向き コマ [行の始め 行の終わり 列の始め 列の終わり]
    向き: down / left / right / up   コマ: 0 1 2
  出力:
    1) 行ごとの左右の端の列（透明でない最も外側の点。肌だけでなく髪や輪郭も含む）を
       手本の男子・ハル・手本の女子・ユイで並べ、手本と違う行に ← をつける
    2) 範囲を指定したときは、その範囲を色ごとの記号で1ドットずつ書き出す（色と記号の対応も出す）
    3) /tmp/compare_<向き><コマ>.png に4人を並べた拡大画像
"""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DIRS = {'down': 0, 'left': 1, 'right': 2, 'up': 3}


def load(ref_path):
    r = Image.open(ref_path).convert('RGBA')
    h = Image.open(ROOT / 'img/chars/haru_chibi.png').convert('RGBA')
    y = Image.open(ROOT / 'img/chars/yui_chibi.png').convert('RGBA')
    return r, h, y


def frames(ref_path, d, st):
    r, h, y = load(ref_path)
    row = DIRS[d] * 48
    return [('手本男', r, st * 48, row), ('ハル', h, st * 48, row),
            ('手本女', r, 144 + st * 48, row), ('ユイ', y, st * 48, row)]


def extents(im, ox, oy):
    px = im.load()
    out = []
    for yy in range(48):
        xs = [x for x in range(-24, 24) if px[ox + 24 + x, oy + yy][3] > 128]
        out.append((min(xs), max(xs)) if xs else None)
    return out


def main():
    ref, d, st = sys.argv[1], sys.argv[2], int(sys.argv[3])
    fs = frames(ref, d, st)
    ex = [extents(im, ox, oy) for _, im, ox, oy in fs]
    fmt = lambda e: '   --  ' if e is None else f'{e[0]:+3d}..{e[1]:+d}'.ljust(8)
    print('行  ' + ''.join(n.ljust(11) for n, *_ in fs))
    for yy in range(48):
        if not any(e[yy] for e in ex):
            continue
        mark = ''
        if ex[1][yy] != ex[0][yy]:
            mark += ' ←ハル'
        if ex[3][yy] != ex[2][yy]:
            mark += ' ←ユイ'
        print(f'{yy:2d}  ' + ''.join(fmt(e[yy]).ljust(11) for e in ex) + mark)
    if len(sys.argv) >= 8:
        y0, y1, x0, x1 = map(int, sys.argv[4:8])
        for n, im, ox, oy in fs:
            px = im.load(); m = {}
            print(f'{n}（列 {x0:+d}..{x1:+d}）')
            print('    ' + ''.join(str(abs(x) % 10) for x in range(x0, x1 + 1)))
            for yy in range(y0, y1 + 1):
                row = ''
                for x in range(x0, x1 + 1):
                    p = px[ox + 24 + x, oy + yy]
                    if p[3] < 128:
                        row += ' '
                        continue
                    hx = '%02x%02x%02x' % p[:3]
                    if hx not in m:
                        m[hx] = chr(ord('a') + len(m)) if len(m) < 26 else chr(ord('A') + len(m) - 26)
                    row += m[hx]
                print(f'{yy:2d}  ' + row)
            print('   ', ' '.join(f'{v}={k}' for k, v in m.items()))
    c = Image.new('RGBA', (48 * 4 + 18, 48), (206, 206, 198, 255))
    for i, (_, im, ox, oy) in enumerate(fs):
        k = im.crop((ox, oy, ox + 48, oy + 48))
        c.paste(k, (i * 54, 0), k)
    c.resize((c.width * 5, c.height * 5), Image.NEAREST).save(f'/tmp/compare_{d}{st}.png')


if __name__ == '__main__':
    main()
