"""試作：美少女アニメ風の歩行グラフィック（設定なしの自由制作）。img/chars/trial.png に書き出す。

使い方：python3 tools/sprites/make_trial.py
1コマ64×96px、横3コマ（左足・立ち・右足）×縦4段（下・左・右・上）、等倍。
版2：デフォルメを弱め、リアル寄りのバランスに（約4.2頭身：頭 y5〜26、全身 y5〜92）。
頭は「頭の座標」で描き、HS 倍に縮めて置く（目だけは縮めると潰れるので、別に小さな目を描く）。
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
FW, FH, CX = 64, 96, 32
HS, HOY = 0.62, 3   # 頭の縮め方と、頭の上端の位置
OUT = (44, 30, 44, 255)

PAL = {
    'H': '#2a2d48', 'h': '#1a1b2e', 'L': '#5b6aa8', 'l': '#3c4675',   # 髪（黒に青いつや）
    'S': '#fbe3d2', 's': '#efc4ad', 't': '#dea48c', 'p': '#f6a6a6',   # 肌・影・赤み
    'E': '#2b1a2a', 'I': '#4b2a7a', 'J': '#7c4fc0', 'K': '#b691ee', 'e': '#ffffff',  # 目
    'm': '#d0706e', 'R': '#d8344a', 'r': '#9c1f33',                   # 口・リボン
    'W': '#fbfbf7', 'w': '#d9dbe4',                                   # ブラウス
    'C': '#efe2c6', 'c': '#d2bf98',                                   # カーディガン
    'G': '#7d8193', 'g': '#5c6072', 'x': '#b84a5a',                   # スカート（チェック）
    'T': '#2a2730', 'u': '#3f3b48', 'B': '#3a2a26', 'b': '#6b5248',   # タイツ・靴
}


class Pen:
    """head=True のときは頭の座標（大きく描いた座標）を HS 倍に縮めて置く"""

    def __init__(self, head=False):
        self.head = head
        self.pal = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) + (255,) for k, v in PAL.items()}
        self.im = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def t(self, x, y):
        if self.head:
            return (round(CX + x * HS), round(HOY + y * HS))
        return (CX + x, y)

    def ell(self, x0, y0, x1, y1, k):
        self.d.ellipse(self.t(x0, y0) + self.t(x1, y1), fill=self.pal[k])

    def rect(self, x0, y0, x1, y1, k):
        self.d.rectangle(self.t(x0, y0) + self.t(x1, y1), fill=self.pal[k])

    def poly(self, pts, k):
        self.d.polygon([self.t(x, y) for x, y in pts], fill=self.pal[k])

    def line(self, pts, k):
        self.d.line([self.t(x, y) for x, y in pts], fill=self.pal[k])

    def px(self, pts, k):
        for x, y in pts:
            self.d.point(self.t(x, y), fill=self.pal[k])


LIFT = {0: (2, 0), 1: (0, 0), 2: (0, 2)}


# ---------------- 下半身（脚は長め） ----------------
def legs(p, step, side):
    la, ra = LIFT[step]
    if side == 'left':
        if step == 1:
            p.rect(-2, 62, 2, 88, 'T'); p.line([(1, 63), (1, 87)], 'u')
            p.rect(-5, 88, 2, 92, 'B'); p.line([(-4, 88), (0, 88)], 'b')
        else:
            p.poly([(0, 62), (3, 62), (7, 88), (4, 88)], 'u')
            p.rect(4, 87, 9, 91, 'B')
            p.poly([(-3, 62), (0, 62), (-4, 88), (-7, 88)], 'T')
            p.rect(-10, 88, -4, 92, 'B'); p.line([(-9, 88), (-6, 88)], 'b')
        return
    p.rect(-5, 62, -2, 88 - la, 'T'); p.line([(-3, 63), (-3, 87 - la)], 'u')
    p.rect(2, 62, 5, 88 - ra, 'T'); p.line([(4, 63), (4, 87 - ra)], 'u')
    p.rect(-6, 88 - la, -1, 92 - la, 'B'); p.line([(-5, 88 - la), (-3, 88 - la)], 'b')
    p.rect(1, 88 - ra, 6, 92 - ra, 'B'); p.line([(2, 88 - ra), (4, 88 - ra)], 'b')


def skirt(p, side):
    w0, w1 = (8, 11) if side != 'left' else (6, 9)
    p.poly([(-w0, 46), (w0, 46), (w1, 63), (-w1, 63)], 'g')
    p.poly([(-w0, 46), (w0 - 1, 46), (w1 - 1, 61), (-w1, 61)], 'G')
    for x in range(-w1 + 3, w1, 4):
        p.line([(round(x * 0.75), 47), (x, 62)], 'g')
    p.line([(-w0 - 1, 52), (w0 + 1, 52)], 'g')
    p.line([(-w1 + 1, 58), (w1 - 1, 58)], 'x')


# ---------------- 上半身（肩幅は控えめ、胴は長め） ----------------
def torso_front(p, back):
    p.rect(-2, 24, 2, 29, 's')
    p.line([(-2, 25), (2, 25)], 't')
    p.poly([(-9, 28), (9, 28), (8, 48), (-8, 48)], 'c')
    p.poly([(-9, 28), (8, 28), (7, 47), (-8, 47)], 'C')
    if not back:
        p.poly([(-2, 28), (2, 28), (2, 47), (-2, 47)], 'W')
        p.poly([(-4, 27), (0, 30), (4, 27), (3, 31), (0, 32), (-3, 31)], 'W')
        p.poly([(-3, 30), (0, 32), (3, 30), (2, 34), (0, 33), (-2, 34)], 'R')
        p.px([(0, 32)], 'r')
        p.line([(-2, 29), (-2, 47)], 'c'); p.line([(2, 29), (2, 47)], 'c')
        p.px([(-2, 37), (-2, 42)], 'c')
        p.line([(-6, 39), (-4, 40)], 'c'); p.line([(6, 39), (4, 40)], 'c')  # 胸のしわ
    else:
        p.line([(0, 31), (0, 46)], 'c')
    for s in (-1, 1):  # 長袖の腕（腰まで）と手
        p.poly([(s * 8, 29), (s * 11, 30), (s * 12, 49), (s * 9, 50)], 'c')
        p.poly([(s * 8, 29), (s * 10, 30), (s * 11, 48), (s * 9, 49)], 'C')
        p.ell(s * 11 - 2, 49, s * 11 + 1, 53, 'S')
        p.px([(s * 11, 53)], 's')


def torso_side(p, step):
    swing = {0: -3, 1: 0, 2: 3}[step]
    p.rect(-2, 24, 1, 29, 's')
    p.poly([(-6, 28), (6, 28), (5, 48), (-5, 48)], 'c')
    p.poly([(-6, 28), (5, 28), (4, 47), (-5, 47)], 'C')
    p.poly([(-6, 28), (-3, 28), (-4, 33)], 'W')
    p.poly([(-7, 30), (-4, 31), (-6, 34)], 'R')
    p.line([(-5, 37), (-3, 38)], 'c')
    p.poly([(-2, 29), (2, 29), (2 + swing, 48), (-2 + swing, 48)], 'c')
    p.poly([(-2, 29), (1, 29), (1 + swing, 47), (-2 + swing, 47)], 'C')
    p.ell(-2 + swing, 47, 1 + swing, 51, 'S')


# ---------------- 頭（頭の座標で描き、縮めて置く） ----------------
def hair_back_long(p, side):
    """背中の中ほどまでの長い髪（体の座標）"""
    if side == 'down':
        p.poly([(-11, 10), (11, 10), (12, 50), (9, 58), (4, 55), (0, 59), (-4, 55), (-9, 58), (-12, 50)], 'h')
        p.poly([(-10, 10), (10, 10), (11, 49), (8, 56), (4, 53), (0, 56), (-4, 53), (-8, 56), (-11, 49)], 'H')
    elif side == 'up':
        p.poly([(-12, 8), (12, 8), (13, 52), (10, 61), (5, 58), (0, 62), (-5, 58), (-10, 61), (-13, 52)], 'h')
        p.poly([(-11, 8), (11, 8), (12, 51), (9, 59), (5, 56), (0, 59), (-5, 56), (-9, 59), (-12, 51)], 'H')
        for x in (-7, -2, 3, 8):
            p.line([(x, 22), (x + (1 if x > 0 else -1), 56)], 'l')
    else:
        p.poly([(-1, 8), (10, 8), (12, 48), (10, 60), (5, 57), (2, 44)], 'h')
        p.poly([(0, 8), (9, 8), (11, 47), (9, 57), (5, 54), (3, 43)], 'H')
        p.line([(6, 18), (8, 52)], 'l')


def head_front(p):
    p.ell(-16, 4, 16, 34, 'h')
    p.ell(-16, 4, 15, 32, 'H')
    p.ell(-12, 12, 12, 34, 'S')
    p.poly([(-12, 24), (12, 24), (10, 31), (4, 36), (0, 37), (-4, 36), (-10, 31)], 'S')
    p.poly([(10, 26), (12, 24), (10, 31), (5, 36), (3, 36), (8, 31)], 's')
    p.rect(-14, 9, 14, 15, 'H')
    for x0, x1, y in [(-14, -8, 22), (-9, -3, 20), (-4, 2, 23), (1, 7, 19), (6, 12, 21), (11, 15, 24)]:
        p.poly([(x0, 14), (x1, 14), ((x0 + x1) // 2 + 1, y)], 'H')
    p.poly([(-16, 14), (-12, 14), (-11, 40), (-14, 44), (-16, 30)], 'H')
    p.poly([(16, 14), (12, 14), (11, 40), (14, 44), (16, 30)], 'h')
    p.line([(-11, 9), (-5, 7)], 'L'); p.line([(-4, 7), (2, 7)], 'L'); p.line([(4, 8), (9, 9)], 'l')
    p.poly([(7, 11), (11, 9), (12, 11), (8, 13)], 'R')


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
    p.poly([(8, 11), (12, 9), (13, 11), (9, 13)], 'R')


def head_back(p):
    p.ell(-16, 4, 16, 34, 'h')
    p.ell(-16, 4, 15, 32, 'H')
    p.line([(-11, 9), (-5, 7)], 'L'); p.line([(-4, 7), (2, 7)], 'L'); p.line([(4, 8), (9, 9)], 'l')
    p.poly([(-12, 11), (-8, 9), (-7, 11), (-11, 13)], 'R')


# 顔の細部は縮めずに体の座標で描く（縮めると潰れるため）
def small_eye(p, x, flip=False):
    """目（横3×縦4）：まつげ・瞳のグラデーション・光"""
    f = (lambda dx: x - dx) if flip else (lambda dx: x + dx)
    p.line([(f(-1), 16), (f(3), 16)], 'E')
    for dx in range(3):
        p.px([(f(dx), 17)], 'I'); p.px([(f(dx), 18)], 'J'); p.px([(f(dx), 19)], 'K')
    p.px([(f(1), 17), (f(1), 18)], 'E')
    p.px([(f(0), 17)], 'e')


def face_front(p):
    small_eye(p, -5)
    small_eye(p, 5, flip=True)
    p.px([(-6, 21), (-5, 21), (5, 21), (6, 21)], 'p')
    p.px([(0, 20)], 't')
    p.px([(0, 22)], 'm')


def face_side(p):
    p.line([(-9, 16), (-6, 16)], 'E')
    p.px([(-8, 17), (-7, 17)], 'I'); p.px([(-8, 18), (-7, 18)], 'J'); p.px([(-8, 19), (-7, 19)], 'K')
    p.px([(-8, 17)], 'e')
    p.px([(-9, 21), (-8, 21)], 'p')
    p.px([(-10, 22)], 'm')


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
    back_l, low, up, hd = Pen(), Pen(), Pen(), Pen(head=True)
    if side != 'up':
        hair_back_long(back_l, side)
    legs(low, step, side)
    if side == 'left':
        skirt(up, 'left'); torso_side(up, step); head_side(hd)
    elif side == 'up':
        skirt(up, 'down'); torso_front(up, True); hair_back_long(up, 'up'); head_back(hd)
    else:
        skirt(up, 'down'); torso_front(up, False); head_front(hd)
    im = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
    im.alpha_composite(back_l.im, (0, bob))
    im.alpha_composite(low.im, (0, 0))
    im.alpha_composite(up.im, (0, bob))
    im.alpha_composite(hd.im, (0, bob))
    if side == 'down':
        fp = Pen(); face_front(fp); im.alpha_composite(fp.im, (0, bob))
    elif side == 'left':
        fp = Pen(); face_side(fp); im.alpha_composite(fp.im, (0, bob))
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
