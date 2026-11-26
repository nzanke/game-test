"""キャラクターの歩行グラフィックを一から描いて img/chars/*.png に書き出す（1コマ64×96px、等倍表示、約3頭身）。

使い方：python3 tools/sprites/make_chars.py
横3コマ（左足・立ち・右足）×縦4段（下・左・右・上）。
部品（顔・髪・前髪・目・胴・腕・脚）を図形で描き、最後に輪郭を自動でつける。
右向きは左向きを左右反転して作る。座標はコマの中のピクセル位置（CX が体の中心）。
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
FW, FH = 64, 96
CX = 32
OUTLINE = (38, 26, 26, 255)


def hexc(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


class Pen:
    """パレットの文字で色を指定して描く道具。x は体の中心からのずれで指定する"""

    def __init__(self, pal):
        self.pal = {k: hexc(v) for k, v in pal.items()}
        self.im = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def c(self, k):
        return self.pal[k]

    @staticmethod
    def b(box):
        x0, y0, x1, y1 = box
        return (CX + x0, y0, CX + x1, y1)

    def ell(self, box, k, shade=None):
        x0, y0, x1, y1 = self.b(box)
        if shade:
            self.d.ellipse((x0, y0, x1, y1), fill=self.c(shade))
            self.d.ellipse((x0, y0, x1 - 2, y1 - 2), fill=self.c(k))
        else:
            self.d.ellipse((x0, y0, x1, y1), fill=self.c(k))

    def rect(self, box, k, shade=None):
        x0, y0, x1, y1 = self.b(box)
        if shade:
            self.d.rectangle((x0, y0, x1, y1), fill=self.c(shade))
            self.d.rectangle((x0, y0, x1 - 1, y1 - 1), fill=self.c(k))
        else:
            self.d.rectangle((x0, y0, x1, y1), fill=self.c(k))

    def poly(self, pts, k):
        self.d.polygon([(CX + x, y) for x, y in pts], fill=self.c(k))

    def line(self, pts, k):
        self.d.line([(CX + x, y) for x, y in pts], fill=self.c(k))

    def px(self, pts, k):
        for x, y in pts:
            self.d.point((CX + x, y), fill=self.c(k))


LIFT = {0: (3, 0), 1: (0, 0), 2: (0, 3)}  # コマごとに（左足、右足）を上げる量


# ---------------- 脚 ----------------
def legs_front(p, ch, step):
    la, ra = LIFT[step]
    if ch['gender'] == 'boy':
        p.rect((-8, 58, -2, 86 - la), 'P', 'q')
        p.rect((2, 58, 8, 86 - ra), 'P', 'q')
        p.rect((-9, 86 - la, -2, 90 - la), 'B')
        p.rect((2, 86 - ra, 9, 90 - ra), 'B')
    else:
        p.rect((-6, 70, -3, 79 - la), 'S', 's')
        p.rect((3, 70, 6, 79 - ra), 'S', 's')
        p.rect((-6, 79 - la, -3, 86 - la), 'W', 'w')
        p.rect((3, 79 - ra, 6, 86 - ra), 'W', 'w')
        p.rect((-7, 86 - la, -2, 90 - la), 'B')
        p.rect((2, 86 - ra, 7, 90 - ra), 'B')


def legs_side(p, ch, step):
    boy = ch['gender'] == 'boy'
    if step == 1:
        if boy:
            p.rect((-4, 58, 4, 86), 'P', 'q')
            p.rect((-7, 86, 4, 90), 'B')
        else:
            p.rect((-2, 70, 2, 79), 'S', 's')
            p.rect((-2, 79, 2, 86), 'W', 'w')
            p.rect((-5, 86, 2, 90), 'B')
        return
    back, front = ('q', 'P') if step == 0 else ('P', 'q')
    if boy:
        p.poly([(-2, 58), (4, 58), (9, 86), (4, 86)], back)
        p.rect((4, 86, 11, 89), 'B')
        p.poly([(-4, 58), (2, 58), (-4, 86), (-9, 86)], front)
        p.rect((-12, 86, -4, 89), 'B')
    else:
        p.poly([(1, 70), (4, 70), (8, 86), (5, 86)], 's')
        p.poly([(5, 80), (7, 80), (8, 86), (5, 86)], 'w')
        p.rect((5, 86, 10, 89), 'B')
        p.poly([(-3, 70), (0, 70), (-5, 86), (-8, 86)], 'S')
        p.poly([(-5, 80), (-2, 80), (-5, 86), (-8, 86)], 'W')
        p.rect((-11, 86, -5, 89), 'B')


# ---------------- 胴 ----------------
def body_front(p, ch, back=False):
    girl = ch['gender'] == 'girl'
    # 腕（半袖）
    for s in (-1, 1):
        x0 = -14 if s < 0 else 10
        p.rect((x0, 37, x0 + 4, 45), 'W', 'w')
        p.rect((x0 + 1, 46, x0 + 3, 59), 'S', 's')
        p.rect((x0 + 1, 59, x0 + 3, 61), 'S')
    if girl:
        p.poly([(-10, 56), (10, 56), (14, 72), (-14, 72)], 'K')
        for x in (-8, -3, 3, 8):
            p.line([(x, 60), (x + (1 if x > 0 else -1) * 2, 72)], 'k')
    p.poly([(-11, 36), (11, 36), (9, 58 if not girl else 57), (-9, 58 if not girl else 57)], 'w')
    p.poly([(-10, 36), (10, 36), (8, 56), (-8, 56)], 'W')
    if not girl:
        p.rect((-9, 56, 9, 59), 'P')
        p.rect((-1, 56, 1, 58), 'B')  # ベルトの留め具
        if not back:
            p.poly([(-4, 36), (4, 36), (0, 41)], 'w')
            p.line([(0, 41), (0, 54)], 'w')
    else:
        if back:
            p.poly([(-11, 36), (11, 36), (11, 45), (-11, 45)], 'N')
            p.line([(-11, 43), (11, 43)], 'W')
        else:
            p.poly([(-11, 36), (11, 36), (8, 42), (0, 47), (-8, 42)], 'N')
            p.poly([(-5, 36), (5, 36), (0, 43)], 'W')
            p.poly([(-3, 44), (3, 44), (2, 50), (-2, 50)], 'R')
            p.poly([(-3, 44), (-6, 47), (-3, 47)], 'R')
            p.poly([(3, 44), (6, 47), (3, 47)], 'R')


def body_side(p, ch, step):
    girl = ch['gender'] == 'girl'
    swing = {0: -3, 1: 0, 2: 3}[step]
    if girl:
        p.poly([(-7, 56), (7, 56), (11, 72), (-11, 72)], 'K')
        p.line([(-3, 60), (-5, 72)], 'k')
        p.line([(3, 60), (5, 72)], 'k')
    p.poly([(-7, 36), (7, 36), (6, 57), (-6, 57)], 'w')
    p.poly([(-6, 36), (6, 36), (5, 55), (-5, 55)], 'W')
    if not girl:
        p.rect((-6, 56, 6, 59), 'P')
    else:
        p.poly([(0, 36), (8, 36), (8, 43), (2, 43)], 'N')
        p.poly([(-7, 40), (-4, 40), (-4, 47), (-7, 47)], 'R')
    # 手前の腕（歩くと前後にふれる）
    p.rect((-2, 37, 3, 45), 'W', 'w')
    p.poly([(-1, 46), (2, 46), (2 + swing, 59), (-1 + swing, 59)], 'S')
    p.rect((-1 + swing, 59, 2 + swing, 61), 'S')


# ---------------- 頭 ----------------
def head_front(p, ch):
    boy = ch['gender'] == 'boy'
    if not boy:  # 肩までの髪（後ろ）とサイドテール
        p.rect((-14, 14, -10, 42), 'H', 'h')
        p.rect((10, 14, 14, 42), 'H', 'h')
        p.poly([(12, 6), (19, 9), (20, 24), (18, 46), (15, 40), (13, 16)], 'h')
        p.poly([(12, 7), (18, 10), (18, 24), (16, 40), (14, 16)], 'H')
    p.ell((-15, 1, 15, 30), 'H', 'h')
    if boy:  # とがった髪
        p.poly([(-11, 6), (-15, -1), (-4, 3)], 'H')
        p.poly([(-4, 3), (0, -3), (5, 3)], 'H')
        p.poly([(5, 3), (15, -1), (11, 7)], 'H')
        p.poly([(-15, 13), (-19, 19), (-14, 22)], 'H')
        p.poly([(15, 13), (19, 19), (14, 22)], 'H')
    p.rect((-3, 31, 3, 37), 's')
    p.ell((-11, 9, 11, 34), 'S', 's')
    if boy:
        p.poly([(-12, 9), (12, 9), (12, 19), (9, 15), (6, 20), (3, 14), (0, 20), (-3, 14), (-6, 20), (-9, 15), (-12, 19)], 'H')
        p.rect((-13, 12, -11, 24), 'H')
        p.rect((11, 12, 13, 24), 'H')
        p.px([(-8, 5), (-7, 5), (-6, 5), (-5, 4), (-4, 4), (-9, 6)], 'L')
        p.px([(-1, 29), (0, 29)], 'm')
    else:
        p.poly([(-12, 9), (12, 9), (12, 17), (8, 15), (5, 18), (1, 14), (-3, 18), (-7, 15), (-12, 17)], 'H')
        p.rect((-13, 12, -11, 26), 'H')
        p.rect((11, 12, 13, 26), 'H')
        p.px([(-8, 5), (-7, 5), (-6, 5), (-5, 4), (-4, 4), (-9, 6), (3, 5), (4, 5)], 'L')
        for x0 in (-8, 3):  # 大きな目（まつげ・瞳・光）
            p.rect((x0 - 1, 20, x0 + 4, 20), 'E')
            p.rect((x0, 21, x0 + 4, 25), 'I')
            p.rect((x0, 25, x0 + 4, 25), 'J')
            p.px([(x0 + 1, 21), (x0 + 1, 22)], 'e')
        p.px([(-9, 27), (-8, 27), (8, 27), (9, 27)], 'p')
        p.px([(-1, 30), (0, 30)], 'm')
        p.poly([(9, 3), (12, 6), (15, 3), (15, 9), (12, 6), (9, 10)], 'R')


def head_side(p, ch):
    boy = ch['gender'] == 'boy'
    if not boy:
        p.poly([(1, 12), (13, 12), (12, 42), (4, 42)], 'h')
        p.poly([(2, 12), (12, 12), (11, 41), (5, 41)], 'H')
        p.poly([(11, 6), (18, 9), (19, 24), (16, 46), (13, 36)], 'h')
        p.poly([(11, 7), (17, 10), (17, 24), (15, 42), (13, 34)], 'H')
    p.ell((-13, 1, 14, 31), 'H', 'h')
    if boy:
        p.poly([(4, 3), (15, -1), (11, 8)], 'H')
        p.poly([(10, 11), (18, 10), (12, 18)], 'H')
        p.poly([(-8, 4), (-6, -2), (0, 3)], 'H')
        p.poly([(8, 23), (14, 26), (8, 29)], 'H')
    p.rect((-4, 31, 1, 37), 's')
    p.ell((-15, 10, 4, 34), 'S', 's')
    p.poly([(2, 9), (14, 9), (14, 28), (7, 31), (2, 26)], 'H')
    if boy:
        p.poly([(-15, 9), (3, 9), (2, 18), (-1, 13), (-4, 19), (-7, 13), (-10, 18), (-13, 14), (-15, 16)], 'H')
        p.px([(-4, 5), (-3, 5), (-2, 5), (-1, 4)], 'L')
        p.px([(-13, 29), (-12, 29)], 'm')
    else:
        p.poly([(-15, 9), (3, 9), (2, 17), (-2, 14), (-6, 18), (-9, 14), (-13, 17), (-15, 16)], 'H')
        p.px([(-4, 5), (-3, 5), (-2, 5), (-1, 4), (5, 5)], 'L')
        p.rect((-14, 20, -9, 20), 'E')
        p.rect((-13, 21, -10, 25), 'I')
        p.rect((-13, 25, -10, 25), 'J')
        p.px([(-12, 21), (-12, 22)], 'e')
        p.px([(-14, 27), (-13, 27)], 'p')
        p.px([(-13, 30), (-12, 30)], 'm')
        p.poly([(8, 3), (11, 6), (14, 3), (14, 8), (11, 6), (8, 9)], 'R')


def head_back(p, ch):
    boy = ch['gender'] == 'boy'
    p.rect((-3, 28, 3, 37), 's')
    if not boy:
        p.rect((-13, 16, 13, 43), 'H', 'h')
        p.poly([(-12, 6), (-19, 9), (-20, 24), (-18, 46), (-15, 40), (-13, 16)], 'h')
        p.poly([(-12, 7), (-18, 10), (-18, 24), (-16, 40), (-14, 16)], 'H')
    p.ell((-15, 1, 15, 32), 'H', 'h')
    if boy:
        p.poly([(-11, 6), (-15, -1), (-4, 3)], 'H')
        p.poly([(-4, 3), (0, -3), (5, 3)], 'H')
        p.poly([(5, 3), (15, -1), (11, 7)], 'H')
        for x in (-9, -3, 3, 9):
            p.poly([(x - 3, 29), (x, 35), (x + 3, 29)], 'H')
        p.px([(-8, 5), (-7, 5), (-6, 5), (-5, 4), (-4, 4), (-9, 6)], 'L')
    else:
        p.px([(-8, 5), (-7, 5), (-6, 5), (-5, 4), (-4, 4), (-9, 6), (3, 5), (4, 5)], 'L')
        p.poly([(-15, 3), (-12, 6), (-9, 3), (-9, 9), (-12, 6), (-15, 10)], 'R')


def outline(im):
    src = im.load()
    out = im.copy()
    dst = out.load()
    for y in range(FH):
        for x in range(FW):
            if src[x, y][3]:
                continue
            if any(0 <= x + dx < FW and 0 <= y + dy < FH and src[x + dx, y + dy][3]
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                dst[x, y] = OUTLINE
    return out


def frame(ch, d, step):
    side = 'left' if d in ('left', 'right') else d
    bob = 0 if step == 1 else 1
    lower, upper = Pen(ch['pal']), Pen(ch['pal'])
    if side == 'down':
        legs_front(lower, ch, step)
        body_front(upper, ch)
        head_front(upper, ch)
    elif side == 'up':
        legs_front(lower, ch, step)
        body_front(upper, ch, back=True)
        head_back(upper, ch)
    else:
        legs_side(lower, ch, step)
        body_side(upper, ch, step)
        head_side(upper, ch)
    im = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
    # 全体を少し下げ、足元をコマの下端近くにそろえる
    im.alpha_composite(lower.im, (0, 3))
    im.alpha_composite(upper.im, (0, 3 + bob))
    im = outline(im)
    if d == 'right':
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im


CHARS = {
    'haru': {
        'gender': 'boy',
        'pal': {
            'H': '#3a3c44', 'h': '#25272d', 'L': '#6a6e7a',
            'S': '#f7dcc4', 's': '#e2b597', 'm': '#c9826e',
            'W': '#f7f7f3', 'w': '#cdd0d8', 'P': '#2f3242', 'q': '#1f2130', 'B': '#2a2220',
        },
    },
    'yui': {
        'gender': 'girl',
        'pal': {
            'H': '#94593a', 'h': '#663922', 'L': '#c48a63',
            'S': '#f8ddc6', 's': '#e4b89b', 'p': '#f4aa9e', 'm': '#c9806c',
            'E': '#2e1d1a', 'I': '#8a4a2c', 'J': '#d4924f', 'e': '#ffffff',
            'W': '#f7f7f3', 'w': '#d0d3da', 'N': '#2f3e68', 'R': '#c8343f',
            'K': '#2f3e68', 'k': '#1f2a4a', 'B': '#4a3226',
        },
    },
}


def render(ch):
    sheet = Image.new('RGBA', (FW * 3, FH * 4), (0, 0, 0, 0))
    for r, d in enumerate(['down', 'left', 'right', 'up']):
        for s in range(3):
            sheet.paste(frame(ch, d, s), (s * FW, r * FH))
    return sheet


if __name__ == '__main__':
    out = ROOT / 'img' / 'chars'
    out.mkdir(parents=True, exist_ok=True)
    for name, ch in CHARS.items():
        render(ch).save(out / f'{name}.png')
        print(f'img/chars/{name}.png')
