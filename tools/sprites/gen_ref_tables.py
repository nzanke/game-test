"""手本（RPGツクールMVの標準キャラの男女）の全12コマを、役割ごとの記号の表に書き起こす。
手本の画像そのものはリポジトリに入れない。使うときに場所を渡す。

使い方: python3 -I tools/sprites/gen_ref_tables.py 手本.png tools/sprites/ref_tables.py

記号：_ 透明／# 濃い輪郭／H L M D E 髪（光→影）／1 2 3 4 肌（明→濃い影）／h 肌の茶色の輪郭・まぶた／
      w 白目／g 灰色の白目／i I K 瞳（濃→明）／T U V 服（明→暗）／Q q p P ズボン・スカート（明→暗）／
      S s d o 靴（明→暗）
手本の中心の列（x −1）を、うちの中心で3列に広げて左右の幅をそろえる（左の端は手本と同じ、右は左右対称）。
"""
import sys
from PIL import Image

SKIN = {'fbdcc8': '1', 'f9c19d': '2', 'ea9777': '3', 'b36739': '4', '964b1f': 'h'}


def boy(hx, y):
    if hx == '000000':
        return '#'
    if hx in SKIN:
        return SKIN[hx]
    hair = {'e3c182': 'H', 'd7a355': 'L', 'b1802c': 'M', '815627': 'D', '553926': 'E'}
    if hx in hair:
        return hair[hx]
    if y < 32:  # 顔：目
        eye = {'ffffff': 'w', 'afa992': 'g', '143443': 'i', '266dae': 'I', '2365a0': 'I', '77afe1': 'K', '4692d7': 'K'}
        if hx in eye:
            return eye[hx]
    top = {'c84322': 'T', '9a2810': 'U', '551c0b': 'V', 'c4bfac': 'T', '978f71': 'U', 'ffffff': 'T', 'f29d00': 'T', '6f5f48': 'V'}
    if hx in top:
        return top[hx]
    low = {'77afe1': 'Q', '4692d7': 'q', '2365a0': 'p', '266dae': 'p', '143443': 'P'}
    if hx in low:
        return low[hx]
    shoe = {'a25f28': 'S', '864f22': 's', '623a1a': 'd', '422b1c': 'o'}
    return shoe.get(hx, '?')


def girl(hx, y):
    if hx == '000000':
        return '#'
    if hx in SKIN:
        return SKIN[hx]
    yel = ['ffee9b', 'ffbf17', 'd58c06', '8c5604', '603906']
    hair = ['dab5df', 'c58cce', 'a752b6', '833880', '4e214b']
    dress = {'9164c8': 0, '6c44a8': 1, '573685': 1, '442c6b': 2, '3d255c': 2}
    if y >= 46:  # 足元：脚と靴
        if hx in yel:
            return '23344'[yel.index(hx)]
        if hx in hair:
            return 'SSsdo'[hair.index(hx)]
        if hx in dress:
            return 'sdo'[dress[hx]]
    if y < 32:  # 顔：目
        eye = {'ffffff': 'w', 'afa992': 'g', '3f1f4e': 'i', '7a3c80': 'I', 'ae61bc': 'K'}
        if hx in eye:
            return eye[hx]
    if hx in hair:
        return 'HLMDE'[hair.index(hx)]
    if hx in yel:  # 頭の上はカチューシャ（キャラごとの差分で扱う。ここでは髪として残し、記号 Y で印をつける）
        return 'Y' if y < 20 else 'TTUVV'[yel.index(hx)]
    if hx in dress:
        return ('TUV' if y <= 39 else 'qpP')[dress[hx]]
    frill = {'ffffff': 'Q', 'afa992': 'Q', '948b6b': 'p', '6f5f48': 'P'}
    return frill.get(hx, '?')


def table(px, base, d, st, fn):
    out = []
    for y in range(48):
        row = ''
        for X in range(48):
            x = X - 24
            rx = x if x <= -1 else -1 if x == 0 else x - 2
            if not -24 <= rx < 24:
                row += '_'
                continue
            p = px[base + st * 48 + 24 + rx, d * 48 + y]
            row += '_' if p[3] < 128 else fn('%02x%02x%02x' % p[:3], y)
        out.append(row)
    return out


def main():
    px = Image.open(sys.argv[1]).convert('RGBA').load()
    lines = ['"""手本の全12コマを役割ごとの記号に書き起こした表（gen_ref_tables.py が作る）。記号の意味は gen_ref_tables.py に。"""', '']
    for name, base, fn in (('BOY', 0, boy), ('GIRL', 144, girl)):
        lines.append(f'{name} = {{')
        for d, dn in enumerate(('down', 'left', 'right', 'up')):
            for st in range(3):
                lines.append(f"    ('{dn}', {st}): [")
                lines += [f"        '{r}'," for r in table(px, base, d, st, fn)]
                lines.append('    ],')
        lines.append('}')
        lines.append('')
    text = '\n'.join(lines)
    open(sys.argv[2], 'w', encoding='utf-8').write(text)
    print('分類できなかった点の数:', text.count('?'))


if __name__ == '__main__':
    main()
