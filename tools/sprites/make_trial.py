"""試作：美少女アニメ風・3頭身の歩行グラフィック（設定なしの自由制作）。img/chars/trial.png に書き出す。

使い方：python3 tools/sprites/make_trial.py
1コマ64×96px、横3コマ（左足・立ち・右足）×縦4段（下・左・右・上）、等倍。頭 y5〜36、全身 y5〜93。
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
FW, FH, CX = 64, 96, 32
OUT = (44, 30, 44, 255)

PAL = {
    'H': '#2a2d48', 'h': '#1a1b2e', 'L': '#5b6aa8', 'l': '#3c4675',   # 髪（黒に青いつや）
    'S': '#fbe3d2', 's': '#efc4ad', 't': '#dea48c', 'p': '#f6a6a6',   # 肌・影・赤み
    'E': '#2b1a2a', 'I': '#4b2a7a', 'J': '#7c4fc0', 'K': '#b691ee', 'e': '#ffffff',  # 目（まつげ・瞳3段・光）
    'm': '#d0706e', 'R': '#d8344a', 'r': '#9c1f33',                   # 口・リボン
    'W': '#fbfbf7', 'w': '#d9dbe4',                                   # ブラウス
    'C': '#efe2c6', 'c': '#d2bf98',                                   # カーディガン
    'G': '#7d8193', 'g': '#5c6072', 'x': '#b84a5a',                   # スカート（チェック）
    'T': '#2a2730', 'u': '#3f3b48', 'B': '#3a2a26', 'b': '#6b5248',   # タイツ・靴
}


class Pen:
    def __init__(self):
        self.pal = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) + (255,) for k, v in PAL.items()}
        self.im = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def ell(self, x0, y0, x1, y1, k):
        self.d.ellipse((CX + x0, y0, CX + x1, y1), fill=self.pal[k])

    def rect(self, x0, y0, x1, y1, k):
        self.d.rectangle((CX + x0, y0, CX + x1, y1), fill=self.pal[k])

    def poly(self, pts, k):
        self.d.polygon([(CX + x, y) for x, y in pts], fill=self.pal[k])

    def line(self, pts, k):
        self.d.line([(CX + x, y) for x, y in pts], fill=self.pal[k])

    def px(self, pts, k):
        for x, y in pts:
            self.d.point((CX + x, y), fill=self.pal[k])


LIFT = {0: (2, 0), 1: (0, 0), 2: (0, 2)}


# ---------------- 下半身 ----------------
def legs(p, step, side):
    la, ra = LIFT[step]
    if side == 'left':
        if step == 1:
            p.rect(-3, 74, 2, 88, 'T'); p.line([(1, 75), (1, 87)], 'u')
            p.rect(-6, 88, 2, 92, 'B'); p.line([(-5, 88), (0, 88)], 'b')
        else:
            p.poly([(0, 74), (4, 74), (7, 88), (3, 88)], 'u')
            p.rect(3, 87, 9, 91, 'B')
            p.poly([(-4, 74), (0, 74), (-4, 88), (-8, 88)], 'T')
            p.rect(-11, 88, -4, 92, 'B'); p.line([(-10, 88), (-6, 88)], 'b')
        return
    p.rect(-6, 74, -2, 88 - la, 'T'); p.line([(-3, 75), (-3, 87 - la)], 'u')
    p.rect(2, 74, 6, 88 - ra, 'T'); p.line([(5, 75), (5, 87 - ra)], 'u')
    p.rect(-7, 88 - la, -1, 92 - la, 'B'); p.line([(-6, 88 - la), (-3, 88 - la)], 'b')
    p.rect(1, 88 - ra, 7, 92 - ra, 'B'); p.line([(2, 88 - ra), (5, 88 - ra)], 'b')


def skirt(p, side):
    w0, w1 = (10, 14) if side != 'left' else (8, 11)
    p.poly([(-w0, 60), (w0, 60), (w1, 76), (-w1, 76)], 'g')
    p.poly([(-w0, 60), (w0 - 1, 60), (w1 - 1, 74), (-w1, 74)], 'G')
    for x in range(-w1 + 3, w1, 5):  # チェック（縦）
        p.line([(round(x * 0.75), 61), (x, 75)], 'g')
    p.line([(-w0 - 1, 66), (w0 + 1, 66)], 'g')  # チェック（横）
    p.line([(-w1 + 1, 71), (w1 - 1, 71)], 'x')


# ---------------- 上半身 ----------------
def torso_front(p, back):
    p.rect(-3, 36, 3, 41, 't')
    p.poly([(-11, 40), (11, 40), (10, 61), (-10, 61)], 'c')
    p.poly([(-11, 40), (10, 40), (9, 60), (-10, 60)], 'C')
    if not back:
        p.poly([(-3, 40), (3, 40), (2, 60), (-2, 60)], 'W')  # 前の開きからブラウス
        p.poly([(-5, 39), (0, 42), (5, 39), (4, 43), (0, 44), (-4, 43)], 'W')  # 襟
        p.poly([(-4, 42), (0, 44), (4, 42), (3, 46), (0, 45), (-3, 46)], 'R')  # リボン
        p.px([(0, 44)], 'r')
        p.px([(-3, 49), (-3, 54)], 'c')  # ボタン
        p.line([(-3, 41), (-3, 60)], 'c')
        p.line([(3, 41), (3, 60)], 'c')
    else:
        p.line([(0, 44), (0, 59)], 'c')
    for s in (-1, 1):  # 長袖の腕と手
        p.poly([(s * 10, 41), (s * 13, 42), (s * 15, 58), (s * 11, 59)], 'c')
        p.poly([(s * 10, 41), (s * 12, 42), (s * 14, 57), (s * 11, 58)], 'C')
        p.ell(s * 13 - 2, 57, s * 13 + 2, 62, 'S')
        p.px([(s * 13 + (1 if s > 0 else -1), 61)], 's')


def torso_side(p, step):
    swing = {0: -3, 1: 0, 2: 3}[step]
    p.rect(-2, 36, 2, 41, 't')
    p.poly([(-7, 40), (8, 40), (7, 61), (-7, 61)], 'c')
    p.poly([(-7, 40), (7, 40), (6, 60), (-6, 60)], 'C')
    p.poly([(-8, 40), (-4, 40), (-5, 46)], 'W')
    p.poly([(-8, 43), (-5, 44), (-7, 48)], 'R')
    p.poly([(-2, 41), (3, 41), (3 + swing, 57), (-2 + swing, 57)], 'c')
    p.poly([(-2, 41), (2, 41), (2 + swing, 56), (-2 + swing, 56)], 'C')
    p.ell(-2 + swing, 55, 2 + swing, 60, 'S')


# ---------------- 頭 ----------------
def eye(p, x, flip=False):
    """アニメ風の目（横5×縦7）：まつげ・瞳のグラデーション・瞳孔・光2つ"""
    f = (lambda dx: x - dx) if flip else (lambda dx: x + dx)
    p.line([(f(-1), 22), (f(5), 22)], 'E')          # 上まつげ
    p.px([(f(5), 23), (f(6), 21)], 'E')              # 目じりのはね
    for dx in range(0, 5):
        p.line([(f(dx), 23), (f(dx), 24)], 'I')
        p.line([(f(dx), 25), (f(dx), 26)], 'J')
        p.px([(f(dx), 27)], 'K')
    p.px([(f(0), 23), (f(0), 24), (f(0), 25), (f(0), 26), (f(0), 27)], 'E')  # 目がしら側の縁
    p.px([(f(2), 24), (f(3), 24), (f(2), 25), (f(3), 25)], 'E')            # 瞳孔
    p.px([(f(1), 23), (f(1), 24), (f(2), 23)], 'e')                         # 大きな光
    p.px([(f(4), 27)], 'e')                                                 # 小さな光
    p.line([(f(1), 28), (f(4), 28)], 't')                                   # 下まつげ（淡く）


def hair_back_long(p, side):
    if side == 'down':
        p.poly([(-17, 14), (17, 14), (19, 58), (15, 68), (8, 64), (0, 70), (-8, 64), (-15, 68), (-19, 58)], 'h')
        p.poly([(-16, 14), (16, 14), (17, 57), (14, 65), (8, 61), (0, 66), (-8, 61), (-14, 65), (-17, 57)], 'H')
    elif side == 'up':
        p.poly([(-18, 12), (18, 12), (20, 60), (16, 72), (8, 68), (0, 74), (-8, 68), (-16, 72), (-20, 60)], 'h')
        p.poly([(-17, 12), (17, 12), (18, 59), (15, 69), (8, 65), (0, 70), (-8, 65), (-15, 69), (-18, 59)], 'H')
        for x in (-11, -4, 4, 11):  # 毛の流れ
            p.line([(x, 30), (x + (1 if x > 0 else -1), 66)], 'l')
    else:
        p.poly([(-2, 12), (16, 12), (19, 56), (16, 70), (8, 66), (2, 52)], 'h')
        p.poly([(-1, 12), (15, 12), (17, 55), (15, 67), (8, 63), (3, 51)], 'H')
        p.line([(10, 24), (13, 62)], 'l')


def head_front(p):
    p.ell(-16, 4, 16, 34, 'h')                       # 髪のかたまり
    p.ell(-16, 4, 15, 32, 'H')
    # 顔：上は丸く、あごはとがる
    p.ell(-12, 12, 12, 34, 'S')
    p.poly([(-12, 24), (12, 24), (10, 31), (4, 36), (0, 37), (-4, 36), (-10, 31)], 'S')
    p.poly([(10, 26), (12, 24), (10, 31), (5, 36), (3, 36), (8, 31)], 's')  # 右の頬の影
    p.line([(-3, 37), (3, 37)], 's')
    # 前髪：束ごとに分かれて垂れる
    p.rect(-14, 9, 14, 15, 'H')
    for x0, x1, y in [(-14, -8, 22), (-9, -3, 20), (-4, 2, 23), (1, 7, 19), (6, 12, 21), (11, 15, 24)]:
        p.poly([(x0, 14), (x1, 14), ((x0 + x1) // 2 + 1, y)], 'H')
    for x, y in [(-6, 15), (4, 15)]:  # 束の間のかげ
        p.line([(x, y), (x + 1, y + 4)], 'h')
    # 顔の横の触角のような髪
    p.poly([(-16, 14), (-12, 14), (-11, 40), (-14, 44), (-16, 30)], 'H')
    p.poly([(16, 14), (12, 14), (11, 40), (14, 44), (16, 30)], 'h')
    p.line([(-14, 18), (-13, 38)], 'l')
    # つや（天使の輪）
    p.line([(-11, 9), (-5, 7)], 'L'); p.line([(-4, 7), (2, 7)], 'L'); p.line([(4, 8), (9, 9)], 'l')
    eye(p, -9)
    eye(p, 9, flip=True)
    p.line([(-11, 30), (-8, 30)], 'p'); p.line([(8, 30), (11, 30)], 'p')   # 頬の赤み
    p.px([(0, 29)], 't')                                                   # 鼻
    p.line([(-1, 33), (1, 33)], 'm')                                       # 口
    p.poly([(7, 11), (11, 9), (12, 11), (8, 13)], 'R')                     # ヘアピン


def head_side(p):
    p.ell(-15, 4, 16, 34, 'h')
    p.ell(-15, 4, 15, 32, 'H')
    p.ell(-16, 12, 4, 34, 'S')
    p.poly([(-16, 24), (2, 24), (0, 32), (-5, 36), (-9, 37), (-15, 31)], 'S')
    p.poly([(-1, 26), (2, 24), (0, 32), (-5, 36), (-6, 35), (-2, 31)], 's')
    p.rect(-15, 9, 3, 15, 'H')
    for x0, x1, y in [(-16, -10, 22), (-11, -5, 20), (-6, 0, 22), (-1, 4, 19)]:
        p.poly([(x0, 14), (x1, 14), ((x0 + x1) // 2, y)], 'H')
    p.poly([(1, 12), (15, 12), (14, 36), (6, 40), (2, 30)], 'H')
    p.line([(-8, 8), (-2, 7)], 'L'); p.line([(0, 7), (6, 8)], 'L')
    # 横向きの目（手前の1つ）
    p.line([(-15, 22), (-9, 22)], 'E'); p.px([(-9, 21)], 'E')
    for dx in range(4):
        x = -14 + dx
        p.line([(x, 23), (x, 24)], 'I'); p.line([(x, 25), (x, 26)], 'J'); p.px([(x, 27)], 'K')
    p.px([(-12, 24), (-12, 25), (-11, 24), (-11, 25)], 'E')
    p.px([(-13, 23), (-13, 24)], 'e')
    p.line([(-15, 30), (-12, 30)], 'p')
    p.px([(-16, 33)], 'm')
    p.poly([(8, 11), (12, 9), (13, 11), (9, 13)], 'R')


def head_back(p):
    p.ell(-16, 4, 16, 34, 'h')
    p.ell(-16, 4, 15, 32, 'H')
    p.line([(-11, 9), (-5, 7)], 'L'); p.line([(-4, 7), (2, 7)], 'L'); p.line([(4, 8), (9, 9)], 'l')
    p.poly([(-12, 11), (-8, 9), (-7, 11), (-11, 13)], 'R')


def outline(im):
    src, out = im.load(), im.copy()
    dst = out.load()
    for y in range(FH):
        for x in range(FW):
            if not src[x, y][3] and any(
                    0 <= x + dx < FW and 0 <= y + dy < FH and src[x + dx, y + dy][3]
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                dst[x, y] = OUT
    return out


def frame(d, step):
    side = 'left' if d in ('left', 'right') else d
    bob = 0 if step == 1 else 1
    back_l, low, up = Pen(), Pen(), Pen()
    if side != 'up':
        hair_back_long(back_l, side)
    legs(low, step, side)
    if side == 'left':
        skirt(up, 'left'); torso_side(up, step); head_side(up)
    elif side == 'up':
        skirt(up, 'down'); torso_front(up, True); hair_back_long(up, 'up'); head_back(up)
    else:
        skirt(up, 'down'); torso_front(up, False); head_front(up)
    im = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
    im.alpha_composite(back_l.im, (0, bob))
    im.alpha_composite(low.im, (0, 0))
    im.alpha_composite(up.im, (0, bob))
    im = outline(im)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if d == 'right' else im


if __name__ == '__main__':
    sheet = Image.new('RGBA', (FW * 3, FH * 4), (0, 0, 0, 0))
    for r, d in enumerate(['down', 'left', 'right', 'up']):
        for s in range(3):
            sheet.paste(frame(d, s), (s * FW, r * FH))
    out = ROOT / 'img' / 'chars' / 'trial.png'
    sheet.save(out)
    print(out.relative_to(ROOT))
