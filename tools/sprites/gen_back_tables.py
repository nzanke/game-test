# 手本の後ろ向きを、役割ごとの記号の表に書き起こす（手本の画像そのものはリポジトリに入れない）
# 使い方: python3 -I tools/sprites/gen_back_tables.py 手本.png tools/sprites/back_tables.py
import sys
from PIL import Image
ref = Image.open(sys.argv[1]).convert('RGBA'); px = ref.load()
BOY = {'e3c182':'H','d7a355':'L','b1802c':'M','815627':'D','553926':'E','000000':'#',
       'fbdcc8':'1','f9c19d':'2','ea9777':'3','b36739':'4','964b1f':'h',
       'c84322':'T','9a2810':'U','551c0b':'V','c4bfac':'T','978f71':'U','ffffff':'T',
       '77afe1':'Q','4692d7':'q','2365a0':'p','143443':'P',
       'a25f28':'S','864f22':'s','623a1a':'d','422b1c':'o'}
def girl(hx, y):
    if hx == '000000': return '#'
    skin = {'fbdcc8':'1','f9c19d':'2','ea9777':'3','b36739':'4','964b1f':'h'}
    if hx in skin: return skin[hx]
    yel = ['ffee9b','ffbf17','d58c06','8c5604','603906']
    hair = ['dab5df','c58cce','a752b6','833880','4e214b']
    dress = {'9164c8':0,'6c44a8':1,'573685':1,'3d255c':2}
    frill = {'ffffff':'Q','afa992':'Q','948b6b':'p','6f5f48':'P'}
    if y >= 46:   # 足元：脚と靴
        if hx in yel: return '23344'[yel.index(hx)]
        if hx in hair: return 'SSsdo'[hair.index(hx)]
        if hx in dress: return 'sdo'[dress[hx]]
    if hx in hair: return 'HLMDE'[hair.index(hx)]
    if hx in yel: return 'HLMDE'[yel.index(hx)] if y < 20 else 'TTUVV'[yel.index(hx)]
    if hx in dress: return ('TUV' if y <= 39 else 'qpP')[dress[hx]]
    if hx in frill: return frill[hx]
    return '?'
def table(base, st, is_girl):
    out = []
    for y in range(48):
        row = ''
        for X in range(48):
            x = X - 24
            rx = x if x <= -1 else -1 if x == 0 else x - 2   # 手本の中心の列（−1）をうちの中心で3列に広げる
            p = px[base + st * 48 + 24 + rx, 144 + y] if -24 <= rx < 24 else (0, 0, 0, 0)
            if p[3] < 128: row += '_'; continue
            hx = '%02x%02x%02x' % p[:3]
            row += girl(hx, y) if is_girl else BOY.get(hx, '?')
        out.append(row)
    while out and set(out[0]) == {'_'}: out.pop(0)
    top = 48 - len(out)
    return top, out
lines = ['"""後ろ向きの表（make_chibi.py が読む）。手本の後ろ向きを1ドットずつ、役割ごとの記号に書き起こしたもの。',
         '手本の中心の列を、うちの中心で3列に広げて左右の幅を正面とそろえてある。色はキャラごとに置き換える。',
         "_ 透明／# 濃い輪郭／H L M D E 髪（光→影）／1〜4 肌／h 肌の茶色の輪郭／T U V 服（明→暗）／",
         'Q q p P ズボン・スカート（明→暗）／S s d o 靴（明→暗）"""', '']
for name, base, g in (('BACK_BOY', 0, False), ('BACK_GIRL', 144, True)):
    lines.append(f'{name} = {{')
    for st in (0, 1, 2):
        top, rows = table(base, st, g)
        lines.append(f'    {st}: ({top}, [')
        lines += [f"        '{r}'," for r in rows]
        lines.append('    ]),')
    lines.append('}')
    lines.append('')
open(sys.argv[2], 'w', encoding='utf-8').write('\n'.join(lines))
print('?の数:', sum(l.count('?') for l in lines))
