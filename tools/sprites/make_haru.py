"""ハル（主人公）の歩行グラフィックを描いて img/chars/haru.png に書き出す。

使い方：python3 tools/sprites/make_haru.py
ユイ（make_trial.py）と同じ「イラストをドットに落とし込んだ」描き方：6倍の大きさでイラストとして描き、64×96pxに縮める。
約4頭身、やや上から見下ろす角度。短めの黒髪、細めの目、白い半袖シャツに紺のズボン。
描画の道具（Art）は make_trial.py のものを使う。座標は 64×96 のコマの中の位置（x は体の中心からのずれ）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_trial import Art, FW, FH, rgb  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

C = {k: rgb(v) for k, v in {
    'hair1': '#3c3f4c', 'hair2': '#16171d', 'hairL': '#8f96b0', 'hairLine': '#0d0d12',
    'skin1': '#fdeee2', 'skin2': '#f1c9b1', 'skinS': '#d69a83', 'skinLine': '#9e6252',
    'eyeW': '#ffffff', 'iris1': '#1e1614', 'iris2': '#6b4c3a', 'lash': '#16100f', 'mouth': '#b86a62',
    'shirt1': '#ffffff', 'shirt2': '#d6dbe6', 'shirtLine': '#7d8496',
    'pants1': '#3d4360', 'pants2': '#1b1e2c', 'belt': '#2a2420',
    'shoe1': '#4a4446', 'shoe2': '#101012', 'line': '#22202a',
}.items()}

LIFT = {0: (1.6, 0), 1: (0, 0), 2: (0, 1.6)}


def legs(a, step, side):
    la, ra = LIFT[step]
    if side == 'left':
        if step == 1:
            a.part([('p', [(-3, 52), (3, 52), (2.4, 88), (-2.6, 88)])], C['pants1'], C['pants2'], shade=C['pants2'], line=C['line'])
            a.part([('e', -6, 86.5, 3, 93)], C['shoe1'], C['shoe2'], light=(150, 150, 160), line=C['line'])
        else:
            a.part([('p', [(-0.5, 52), (3.5, 52), (7, 87), (3.5, 88)])], C['pants2'], C['pants2'], line=C['line'])
            a.part([('e', 3, 85.5, 10.5, 91.5)], C['shoe1'], C['shoe2'], line=C['line'])
            a.part([('p', [(-3.5, 52), (0.5, 52), (-3.6, 88), (-7.2, 87)])], C['pants1'], C['pants2'], shade=C['pants2'], line=C['line'])
            a.part([('e', -11, 86.5, -3, 92.5)], C['shoe1'], C['shoe2'], light=(150, 150, 160), line=C['line'])
        return
    for x0, x1, lift in ((-5.4, -0.4, la), (0.4, 5.4, ra)):
        m = a.part([('p', [(x0, 52), (x1, 52), (x1 - 0.3, 88 - lift), (x0 + 0.3, 88 - lift)])], C['pants1'], C['pants2'], shade=C['pants2'], line=C['line'])
        a.clip(m, [('r', (x0 + x1) / 2 - 0.2, 56, (x0 + x1) / 2 + 0.2, 87)], (90, 98, 130), 0.5, blur=0.3)  # 折り目
        a.part([('e', x0 - 1.2, 86 - lift, x1 + 1.2, 93 - lift)], C['shoe1'], C['shoe2'], light=(160, 160, 170), line=C['line'], la=0.7)


def torso_front(a, back, bob):
    b = bob
    a.part([('r', -2.4, 29.5 + b, 2.4, 35 + b)], C['skin2'], C['skinS'], line=C['skinLine'])  # 首
    for s in (-1, 1):  # 腕（半袖から出る腕と手）
        a.part([('p', [(s * 9.6, 41 + b), (s * 11.6, 41 + b), (s * 12, 54 + b), (s * 9.8, 54.4 + b)])], C['skin1'], C['skin2'], shade=C['skinS'], line=C['skinLine'], lw=0.6)
        a.part([('e', s * 10.9 - 1.8, 53 + b, s * 10.9 + 1.8, 57.6 + b)], C['skin1'], C['skin2'], shade=C['skinS'], line=C['skinLine'], lw=0.6)
    m = a.part([('p', [(-10.4, 33.5 + b), (10.4, 33.5 + b), (9, 52.5 + b), (-9, 52.5 + b)])], C['shirt1'], C['shirt2'],
               shade=C['shirt2'], light=(255, 255, 255), line=C['shirtLine'])
    for s in (-1, 1):  # 半袖
        a.part([('p', [(s * 8.6, 33.8 + b), (s * 11.2, 34.8 + b), (s * 12.4, 42 + b), (s * 9.4, 42.6 + b)])], C['shirt1'], C['shirt2'], shade=C['shirt2'], line=C['shirtLine'])
        a.stroke([(s * 8.8, 33.8 + b), (s * 10.8, 34.6 + b)], (255, 255, 255), 0.7, 0.9)
    if not back:
        a.part([('p', [(-3.4, 33 + b), (0, 37.4 + b), (3.4, 33 + b), (2.4, 34 + b), (0, 36.2 + b), (-2.4, 34 + b)])], C['shirt1'], C['shirt2'], line=C['shirtLine'], lw=0.5)  # 開いた襟
        a.clip(m, [('p', [(-2, 33.5 + b), (2, 33.5 + b), (0, 37 + b)])], C['skin2'], 1.0)
        a.clip(m, [('r', -0.25, 37 + b, 0.25, 51 + b)], C['shirtLine'], 0.7)  # 前立て
        for y in (40, 44.5, 49):
            a.blob(-0.9 + 0.6, y + b, 0.9 - 0.2, y + 0.9 + b, C['shirtLine'], 0.8, 0)
        a.clip(m, [('e', -8, 44 + b, -3, 52 + b), ('e', 3, 44 + b, 8, 52 + b)], C['shirt2'], 0.5, blur=1.0)  # しわ
    else:
        a.clip(m, [('r', -6, 36 + b, 6, 37 + b)], C['shirt2'], 0.6, blur=0.4)
    a.part([('r', -9.2, 51 + b, 9.2, 53.6 + b)], C['belt'], C['belt'], line=C['line'], lw=0.5)  # ベルト
    if not back:
        a.part([('r', -1, 51.4 + b, 1, 53.2 + b)], (170, 160, 140), (120, 110, 90))


def torso_side(a, step, bob):
    b = bob
    sw = {0: -2.6, 1: 0, 2: 2.6}[step]
    a.part([('r', -2, 29.5 + b, 1.6, 35 + b)], C['skin2'], C['skinS'], line=C['skinLine'])
    a.part([('p', [(-6.8, 33.5 + b), (6.4, 33.5 + b), (5.6, 52.5 + b), (-5.8, 52.5 + b)])], C['shirt1'], C['shirt2'], shade=C['shirt2'], light=(255, 255, 255), line=C['shirtLine'])
    a.part([('p', [(-7, 33.4 + b), (-3.6, 33.4 + b), (-5, 37 + b)])], C['skin2'], C['skin2'], line=C['shirtLine'], lw=0.4)
    a.part([('r', -6, 51 + b, 5.8, 53.6 + b)], C['belt'], C['belt'], line=C['line'], lw=0.5)
    a.part([('p', [(-2.2, 34.4 + b), (2.4, 34.4 + b), (2.6 + sw * 0.4, 42 + b), (-2.4 + sw * 0.4, 42 + b)])], C['shirt1'], C['shirt2'], shade=C['shirt2'], line=C['shirtLine'])
    a.part([('p', [(-1.6 + sw * 0.4, 42 + b), (1.8 + sw * 0.4, 42 + b), (1.8 + sw, 53.5 + b), (-1.6 + sw, 53.5 + b)])], C['skin1'], C['skin2'], line=C['skinLine'], lw=0.6)
    a.part([('e', -1.9 + sw, 52.5 + b, 1.9 + sw, 57.2 + b)], C['skin1'], C['skin2'], line=C['skinLine'], lw=0.6)


def eye(a, cx, cy, flip=False, side=False):
    """男子の目：細め、暗い茶色の瞳、光は1つ、まつげの跳ねなし"""
    s = -1 if flip else 1
    w, h = (3.4, 3.2) if not side else (2.4, 3.2)
    a.part([('e', cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)], C['eyeW'], (232, 232, 238))
    a.part([('e', cx - w / 2 + 0.4, cy - h / 2 + 0.1, cx + w / 2 - 0.4, cy + h / 2)], C['iris1'], C['iris2'])
    a.blob(cx - s * 0.9 - 0.45, cy - 1.0, cx - s * 0.9 + 0.45, cy - 0.1, (255, 255, 255), 0.95, 0)
    a.stroke([(cx - w / 2 - 0.3, cy - h / 2 + 0.3), (cx, cy - h / 2 - 0.1), (cx + w / 2 + 0.3, cy - h / 2 + 0.3)], C['lash'], 0.75)
    a.stroke([(cx - 2.2, cy - h / 2 - 1.6), (cx + 2.2, cy - h / 2 - 1.9)], C['hair2'], 0.55)  # 眉（前髪の間から）


def tufts(a, b, pts_list):
    """頭のてっぺんの毛先（少しだけ散らす）"""
    a.part([('p', [(x, y + b) for x, y in pts]) for pts in pts_list], C['hair1'], C['hair2'], shade=C['hair2'], line=C['hairLine'], lw=0.7)


def head_front(a, bob):
    b = bob
    top = [[(-9, 11), (-11.4, 8.4), (-5, 9.4)], [(-4, 9), (-2.4, 6.6), (1.4, 8.8)], [(2, 9), (6, 7), (6.4, 10.4)], [(7.6, 10.6), (11.2, 10), (9.6, 13.6)]]
    tufts(a, b, top)
    hm = a.part([('e', -10.4, 7.6 + b, 10.4, 29 + b)], C['hair1'], C['hair2'], shade=C['hair2'], line=C['hairLine'])
    face = [('e', -7.8, 14.6 + b, 7.8, 29.4 + b), ('p', [(-7.8, 22 + b), (7.8, 22 + b), (6.6, 27.6 + b), (2.8, 30.8 + b), (0, 31.4 + b), (-2.8, 30.8 + b), (-6.6, 27.6 + b)])]
    fm = a.part(face, C['skin1'], C['skin2'], shade=C['skinS'], sh=(1.2, 1.4), sb=1.0, line=C['skinLine'], lw=0.6)
    a.clip(fm, [('r', -9, 14 + b, 9, 19.6 + b)], C['skinS'], 0.55, blur=0.9)
    bang = [('r', -9.6, 10.4 + b, 9.6, 16.6 + b)]
    for x0, x1, y in [(-9.6, -5.6, 22.4), (-6.4, -2.2, 20.6), (-3, 1.2, 21.8), (0.4, 4.6, 20.2), (3.8, 7.8, 22), (7, 10, 21)]:
        bang.append(('p', [(x0, 16 + b), (x1, 16 + b), ((x0 + x1) / 2 - 0.8, y + b)]))
    bm = a.part(bang, C['hair1'], C['hair2'], shade=C['hair2'], line=C['hairLine'], lw=0.7)
    for s in (-1, 1):  # もみあげ（短め）
        a.part([('p', [(s * 10.4, 15 + b), (s * 7.8, 15 + b), (s * 7.6, 26 + b), (s * 9.2, 27.6 + b), (s * 10.6, 22 + b)])], C['hair1'] if s < 0 else C['hair2'], C['hair2'], line=C['hairLine'], lw=0.7)
    a.clip(hm, [('e', -7.5, 10.8 + b, 1, 12.8 + b)], C['hairL'], 0.35, blur=0.6)
    a.clip(bm, [('e', -7.5, 10.8 + b, 1, 12.8 + b)], C['hairL'], 0.25, blur=0.6)
    eye(a, -3.9, 23.8 + b)
    eye(a, 3.9, 23.8 + b, flip=True)
    a.blob(-0.35, 26.6 + b, 0.35, 27.5 + b, C['skinS'], 0.6, 0.2)
    a.stroke([(-1, 29.1 + b), (1, 29.1 + b)], C['mouth'], 0.45)


def head_side(a, bob):
    b = bob
    tufts(a, b, [[(-6, 9.4), (-5.6, 7), (-1, 8.8)], [(0, 8.8), (4.6, 6.6), (4.8, 10)], [(6, 10), (11, 9.6), (9.6, 13.4)], [(9, 15), (12.4, 16), (9.6, 19)]])
    hm = a.part([('e', -9.4, 7.6 + b, 10.4, 29 + b)], C['hair1'], C['hair2'], shade=C['hair2'], line=C['hairLine'])
    fm = a.part([('e', -10.6, 14.6 + b, 2.8, 29.4 + b), ('p', [(-10.6, 22 + b), (1.6, 22 + b), (0.2, 28 + b), (-3.2, 31 + b), (-6.2, 31.4 + b), (-10, 28 + b)])],
                C['skin1'], C['skin2'], shade=C['skinS'], line=C['skinLine'], lw=0.6)
    a.clip(fm, [('r', -11, 14 + b, 3, 19.6 + b)], C['skinS'], 0.55, blur=0.9)
    bang = [('r', -10, 10.4 + b, 2.4, 16.6 + b)]
    for x0, x1, y in [(-10.6, -6.6, 22), (-7.4, -3.4, 20.6), (-4.2, -0.2, 21.4), (-1, 2.8, 19.8)]:
        bang.append(('p', [(x0, 16 + b), (x1, 16 + b), ((x0 + x1) / 2 - 0.8, y + b)]))
    a.part(bang, C['hair1'], C['hair2'], shade=C['hair2'], line=C['hairLine'], lw=0.7)
    a.part([('p', [(0.6, 12.6 + b), (10, 12.6 + b), (9.4, 26 + b), (5, 29.4 + b), (1.4, 24 + b)])], C['hair1'], C['hair2'], shade=C['hair2'], line=C['hairLine'], lw=0.7)
    a.clip(hm, [('e', -5, 10.8 + b, 4, 12.8 + b)], C['hairL'], 0.35, blur=0.6)
    eye(a, -7.4, 23.8 + b, side=True)
    a.stroke([(-10.2, 29.1 + b), (-9.2, 29.2 + b)], C['mouth'], 0.45)


def head_back(a, bob):
    b = bob
    tufts(a, b, [[(-9, 11), (-11.4, 8.4), (-5, 9.4)], [(-4, 9), (-2.4, 6.6), (1.4, 8.8)], [(2, 9), (6, 7), (6.4, 10.4)], [(7.6, 10.6), (11.2, 10), (9.6, 13.6)]])
    hm = a.part([('e', -10.4, 7.6 + b, 10.4, 29.6 + b)] + [('p', [(x - 2.2, 27 + b), (x + 2.2, 27 + b), (x, 31.4 + b)]) for x in (-6.4, -2.2, 2.2, 6.4)],
                C['hair1'], C['hair2'], shade=C['hair2'], line=C['hairLine'])
    a.clip(hm, [('e', -7.5, 10.8 + b, 1, 12.8 + b)], C['hairL'], 0.35, blur=0.6)


def frame(d, step):
    side = 'left' if d in ('left', 'right') else d
    bob = 0 if step == 1 else 0.6
    a = Art()
    legs(a, step, side)
    if side == 'left':
        torso_side(a, step, bob); head_side(a, bob)
    elif side == 'up':
        torso_front(a, True, bob); head_back(a, bob)
    else:
        torso_front(a, False, bob); head_front(a, bob)
    im = a.shrink()
    return im.transpose(Image.FLIP_LEFT_RIGHT) if d == 'right' else im


if __name__ == '__main__':
    sheet = Image.new('RGBA', (FW * 3, FH * 4), (0, 0, 0, 0))
    for r, d in enumerate(['down', 'left', 'right', 'up']):
        for s in range(3):
            sheet.paste(frame(d, s), (s * FW, r * FH))
    out = ROOT / 'img' / 'chars' / 'haru.png'
    sheet.save(out)
    print(out.relative_to(ROOT))
