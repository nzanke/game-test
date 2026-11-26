"""手本の書き起こし（ref_tables.py）を土台に、キャラごとの色と差分で全12コマを描く。

使い方: python3 -I tools/sprites/make_from_ref.py [出力の名前の後ろにつける文字（例 _ref）]
キャラを足すときは CHARS に、土台（BOY/GIRL）・色・差分を書くだけでよい。
差分は関数で、描いた1コマ（Image）・向き・コマ・色を受け取って上書きする。
"""
import sys
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ref_tables as rt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DIRS = ['down', 'left', 'right', 'up']


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def mix(a, b, t):
    return tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))


def palette(c):
    """キャラの色の指定（髪5段・肌4段・瞳3段・服3段・ズボン2段・靴2段・輪郭）から記号ごとの色を作る"""
    p = {'#': rgb(c['line']), 'w': (255, 255, 255), 'g': (196, 190, 200)}
    for k, v in zip('HLMDE', c['hair']):
        p[k] = rgb(v)
    for k, v in zip('1234', c['skin']):
        p[k] = rgb(v)
    p['h'] = rgb(c['skin'][3])
    for k, v in zip('iIK', c['iris']):
        p[k] = rgb(v)
    for k, v in zip('TUV', c['top']):
        p[k] = rgb(v)
    l1, l2 = rgb(c['low'][0]), rgb(c['low'][1])
    p.update({'Q': mix(l1, (255, 255, 255), 0.3), 'q': l1, 'p': l2, 'P': mix(l2, (0, 0, 0), 0.3)})
    s1, s2 = rgb(c['shoe'][0]), rgb(c['shoe'][1])
    p.update({'S': s1, 's': mix(s1, s2, 0.5), 'd': s2, 'o': mix(s2, (0, 0, 0), 0.35)})
    p['Y'] = p['L']
    return p


def draw(rows, pal, fix=None):
    im = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '_':
                col = fix(ch, x, y) if fix else None
                im.putpixel((x, y), (col or pal[ch]) + (255,))
    return im


# ---- 差分
def long_pants(c):
    """手本の男子は素足。長ズボンにする：44行より下の肌（と茶色の輪郭）をズボンの色に"""
    pal = palette(c)
    return lambda ch, x, y: (pal['q'] if ch in '123' else pal['p']) if y >= 44 and ch in '1234h' else None


def no_headband(im, rows, d, st, pal):
    """手本の女子のカチューシャ（Y）を消す：Y は髪の色にし、頭の上に出っ張る部分（大きなリボンや飾り）は
    男子の同じコマの頭の形（12行より上）で削って、上の縁を暗い髪色で縁取る"""
    px = im.load()
    boy = rt.BOY[(d, st)]
    for y in range(12):
        for x in range(48):
            if rows[y][x] != '_' and boy[y][x] == '_':
                px[x, y] = (0, 0, 0, 0)
    for x in range(48):
        for y in range(14):
            if px[x, y][3] > 128:
                if rows[y][x] in 'YHLMDE':
                    px[x, y] = pal['E'] + (255,)
                break
    return im


CHARS = {
    'haru': dict(base='BOY', line='#2a1e2a',
                 hair=['#7d8396', '#626778', '#3c3f4c', '#2a2c36', '#16171d'],
                 skin=['#fbdcc8', '#f6bf9c', '#e2916f', '#97502c'],
                 iris=['#5a3a28', '#8a6040', '#c09a78'],
                 top=['#ffffff', '#d6dbe6', '#363a4a'], low=['#4d6290', '#2e3c62'], shoe=['#7a6a66', '#463c40'],
                 diffs=['long_pants']),
    'yui': dict(base='GIRL', line='#2a1e2a',
                hair=['#a3aee6', '#6873b0', '#454d84', '#30365e', '#1e2240'],
                skin=['#fbdcc8', '#f6bf9c', '#e2916f', '#97502c'],
                iris=['#5a3aa0', '#8a5ad8', '#d8c2ff'],
                top=['#f7ecd4', '#cdb88f', '#4a3826'], low=['#8e93a6', '#4f5366'], shoe=['#7a5a4c', '#2e201c'],
                diffs=['no_headband']),
}


def make(name, c):
    base = getattr(rt, c['base'])
    pal = palette(c)
    fix = long_pants(c) if 'long_pants' in c['diffs'] else None
    sheet = Image.new('RGBA', (144, 192), (0, 0, 0, 0))
    for r, d in enumerate(DIRS):
        for st in range(3):
            rows = base[(d, st)]
            im = draw(rows, pal, fix)
            if 'no_headband' in c['diffs']:
                im = no_headband(im, rows, d, st, pal)
            sheet.paste(im, (st * 48, r * 48))
    return sheet


if __name__ == '__main__':
    suffix = sys.argv[1] if len(sys.argv) > 1 else '_ref'
    for name, c in CHARS.items():
        out = ROOT / 'img' / 'chars' / f'{name}{suffix}.png'
        make(name, c).save(out)
        print(out.relative_to(ROOT))
