"""キャラクターの歩行グラフィックを一から描いて img/chars/*.png に書き出す。

使い方：python3 tools/sprites/make_chars.py
1コマ72×105px（参考のドットと同じ）、横3コマ（左足・立ち・右足）×縦4段（下・左・右・上）、等倍表示。
形と比率は参考のドットを1ドットずつ測った値をそのまま座標にしている（色と服は自分のキャラのもの）：
  頭（髪）y10〜46・横41px、前髪は目のすぐ上まで厚く、見える顔は小さい（横約17px・縦約8px）、
  目は横2px・縦3pxで頭の下寄り（y36〜38）、首はほぼ見えない、胴 y47〜62、スカート y62〜88、
  靴 y92〜103（太く背が高い）、腕は外へ開き手はスカートの横。マップに合わせてやや上から見下ろす角度。
座標の x は体の中心（CX）からのずれ、y はコマの上端からの位置。右向きは左向きの左右反転。
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
FW, FH = 72, 105
CX = 36
OUTLINE = (40, 28, 30, 255)


def hexc(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


class Pen:
    def __init__(self, pal):
        self.pal = {k: hexc(v) for k, v in pal.items()}
        self.im = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def c(self, k):
        return self.pal[k]

    def ell(self, x0, y0, x1, y1, k, shade=None):
        if shade:
            self.d.ellipse((CX + x0, y0, CX + x1, y1), fill=self.c(shade))
            self.d.ellipse((CX + x0, y0, CX + x1 - 2, y1 - 2), fill=self.c(k))
        else:
            self.d.ellipse((CX + x0, y0, CX + x1, y1), fill=self.c(k))

    def rect(self, x0, y0, x1, y1, k, shade=None):
        if shade:
            self.d.rectangle((CX + x0, y0, CX + x1, y1), fill=self.c(shade))
            self.d.rectangle((CX + x0, y0, CX + x1 - 1, y1 - 1), fill=self.c(k))
        else:
            self.d.rectangle((CX + x0, y0, CX + x1, y1), fill=self.c(k))

    def poly(self, pts, k):
        self.d.polygon([(CX + x, y) for x, y in pts], fill=self.c(k))

    def line(self, pts, k):
        self.d.line([(CX + x, y) for x, y in pts], fill=self.c(k))

    def px(self, pts, k):
        for x, y in pts:
            self.d.point((CX + x, y), fill=self.c(k))


LIFT = {0: (2, 0), 1: (0, 0), 2: (0, 2)}  # コマごとに（左足、右足）を上げる量


def shoe(p, x0, y0, x1, y1):
    """靴（太く背が高い）。上から見下ろすので甲を明るく"""
    p.rect(x0, y0, x1, y1, 'B')
    p.line([(x0 + 1, y0 + 1), (x1 - 1, y0 + 1)], 'b')
    p.line([(x0 + 1, y1 - 2), (x0 + 3, y1 - 2)], 'b')


# ---------------- 脚 ----------------
def legs_front(p, ch, step):
    la, ra = LIFT[step]
    if ch['gender'] == 'boy':
        p.rect(-9, 64, -1, 93 - la, 'P', 'q')
        p.rect(1, 64, 9, 93 - ra, 'P', 'q')
    else:
        p.rect(-8, 86, -3, 93 - la, 'W', 'w')
        p.rect(3, 86, 8, 93 - ra, 'W', 'w')
    shoe(p, -10, 92 - la, -2, 103 - la)
    shoe(p, 2, 92 - ra, 10, 103 - ra)


def legs_side(p, ch, step):
    boy = ch['gender'] == 'boy'
    if step == 1:
        if boy:
            p.rect(-5, 64, 5, 93, 'P', 'q')
        else:
            p.rect(-4, 86, 4, 93, 'W', 'w')
        shoe(p, -9, 92, 4, 103)
        return
    if boy:
        p.poly([(-1, 64), (6, 64), (11, 93), (4, 93)], 'q')
        p.poly([(-6, 64), (1, 64), (-4, 93), (-11, 93)], 'P')
    else:
        p.poly([(1, 86), (6, 86), (9, 93), (4, 93)], 'w')
        p.poly([(-6, 86), (-1, 86), (-4, 93), (-9, 93)], 'W')
    shoe(p, 3, 91, 13, 101)
    shoe(p, -15, 92, -4, 102)


# ---------------- 胴と腕 ----------------
def body_front(p, ch, back=False):
    girl = ch['gender'] == 'girl'
    if girl:  # スカート（裾が広がる）
        p.poly([(-14, 61), (14, 61), (18, 88), (-18, 88)], 'k')
        p.poly([(-14, 61), (13, 61), (17, 86), (-17, 86)], 'K')
        for x in (-11, -5, 1, 7, 13):
            p.line([(x, 65), (x + (2 if x > 0 else -2), 87)], 'k')
    # 胴
    p.poly([(-13, 46), (13, 46), (12, 64), (-12, 64)], 'w')
    p.poly([(-12, 46), (12, 46), (11, 62), (-11, 62)], 'W')
    if not girl:
        p.rect(-12, 62, 12, 65, 'P')
        p.rect(-1, 62, 1, 64, 'B')
        if not back:
            p.poly([(-4, 46), (4, 46), (0, 50)], 'w')
            p.line([(0, 50), (0, 61)], 'w')
    elif back:
        p.poly([(-13, 46), (13, 46), (13, 55), (-13, 55)], 'N')
        p.line([(-13, 53), (13, 53)], 'W')
    else:
        p.poly([(-13, 46), (13, 46), (10, 51), (0, 56), (-10, 51)], 'N')
        p.poly([(-5, 46), (5, 46), (0, 52)], 'W')
        p.poly([(-3, 54), (3, 54), (2, 60), (-2, 60)], 'R')
        p.poly([(-3, 54), (-7, 57), (-3, 57)], 'R')
        p.poly([(3, 54), (7, 57), (3, 57)], 'R')
    # 腕（半袖）：肩から外へ開き、手はスカートの横
    for s in (-1, 1):
        p.poly([(s * 11, 46), (s * 16, 47), (s * 19, 56), (s * 14, 57)], 'w')
        p.poly([(s * 11, 46), (s * 15, 47), (s * 18, 55), (s * 14, 56)], 'W')
        p.poly([(s * 14, 57), (s * 18, 56), (s * 21, 65), (s * 17, 66)], 'S')
        x = s * 19
        p.ell(x - 3, 64, x + 3, 71, 'S', 's')


def body_side(p, ch, step):
    girl = ch['gender'] == 'girl'
    swing = {0: -3, 1: 0, 2: 3}[step]
    if girl:
        p.poly([(-11, 61), (11, 61), (15, 88), (-15, 88)], 'k')
        p.poly([(-11, 61), (10, 61), (14, 86), (-14, 86)], 'K')
        p.line([(-5, 65), (-8, 87)], 'k')
        p.line([(4, 65), (7, 87)], 'k')
    p.poly([(-10, 46), (10, 46), (9, 64), (-9, 64)], 'w')
    p.poly([(-9, 46), (9, 46), (8, 62), (-8, 62)], 'W')
    if not girl:
        p.rect(-9, 62, 9, 65, 'P')
    else:
        p.poly([(0, 46), (11, 46), (11, 53), (2, 53)], 'N')
        p.poly([(-10, 50), (-7, 50), (-7, 57), (-10, 57)], 'R')
    # 手前の腕（歩くと前後にふれる）
    p.poly([(-4, 47), (3, 47), (3, 56), (-4, 56)], 'w')
    p.poly([(-4, 47), (2, 47), (2, 55), (-4, 55)], 'W')
    p.poly([(-3, 56), (1, 56), (1 + swing, 65), (-3 + swing, 65)], 'S')
    p.ell(-4 + swing, 63, 2 + swing, 70, 'S', 's')


# ---------------- 頭 ----------------
def bangs(p, x0, x1, top, base, tips):
    """前髪：top〜base は髪で埋め、そこから毛先（tips：[(x, 下端y), ...]）を三角に垂らす"""
    p.rect(x0, top, x1, base, 'H')
    for x, y in tips:
        p.poly([(x - 3, base), (x + 3, base), (x, y)], 'H')


def eye(p, x, y, ch):
    """目：横2px・縦3px（上にまつげ、左上に白い光）"""
    p.rect(x - 1, y, x + 2, y, 'E')
    p.rect(x, y + 1, x + 1, y + 3, 'I')
    p.px([(x, y + 1)], 'e')


def head_front(p, ch):
    boy = ch['gender'] == 'boy'
    # 髪のかたまり（頭頂が見えるので厚い）
    p.ell(-20, 10, 20, 45, 'H', 'h')
    if boy:
        for x, y in [(-14, 9), (-6, 7), (2, 7), (10, 9)]:
            p.poly([(x - 4, y + 6), (x + 4, y + 6), (x + 1, y - 2)], 'H')
    else:  # 肩まで落ちる横の髪
        p.poly([(-20, 28), (-15, 28), (-15, 49), (-19, 47)], 'H')
        p.poly([(15, 28), (20, 28), (19, 47), (15, 49)], 'h')
    # 顔（小さく、頭の下寄り）
    p.ell(-10, 27, 10, 45, 'S', 's')
    p.rect(-2, 44, 2, 46, 'n')
    # 前髪（目のすぐ上まで厚く）
    bangs(p, -12, 12, 22, 31, [(-9, 35), (-4, 36), (1, 35), (6, 36), (10, 34)])
    p.rect(-13, 28, -10, 42, 'H')
    p.rect(10, 28, 13, 42, 'H')
    p.px([(-10, 16), (-9, 15), (-8, 15), (-7, 14), (-6, 14), (-5, 14), (4, 15), (5, 15)], 'L')
    eye(p, -6, 36, ch)
    eye(p, 4, 36, ch)
    p.px([(-1, 42), (0, 42)], 'm')
    if not boy:
        p.poly([(12, 13), (16, 16), (20, 13), (20, 20), (16, 16), (12, 20)], 'R')


def head_side(p, ch):
    boy = ch['gender'] == 'boy'
    p.ell(-17, 10, 21, 45, 'H', 'h')
    if boy:
        for x, y in [(-6, 8), (3, 7), (12, 9), (18, 15)]:
            p.poly([(x - 4, y + 6), (x + 4, y + 6), (x + 2, y - 2)], 'H')
    else:
        p.poly([(4, 28), (20, 28), (19, 48), (6, 48)], 'h')
        p.poly([(4, 28), (18, 28), (17, 47), (6, 47)], 'H')
    p.ell(-20, 26, -2, 45, 'S', 's')
    p.rect(-7, 44, -3, 46, 'n')
    bangs(p, -20, 0, 20, 31, [(-18, 34), (-13, 36), (-8, 35), (-3, 33)])
    p.poly([(-2, 22), (12, 22), (8, 44), (-2, 42)], 'H')
    p.px([(-6, 15), (-5, 14), (-4, 14), (-3, 14), (6, 15)], 'L')
    eye(p, -15, 35, ch)
    p.px([(-19, 42)], 'm')
    if not boy:
        p.poly([(10, 13), (14, 16), (18, 13), (18, 20), (14, 16), (10, 20)], 'R')


def head_back(p, ch):
    boy = ch['gender'] == 'boy'
    p.rect(-3, 42, 3, 47, 'n')
    if not boy:
        p.poly([(-19, 28), (19, 28), (18, 49), (-18, 49)], 'h')
        p.poly([(-18, 28), (18, 28), (17, 48), (-17, 48)], 'H')
    p.ell(-20, 10, 20, 46, 'H', 'h')
    if boy:
        for x, y in [(-14, 9), (-6, 7), (2, 7), (10, 9)]:
            p.poly([(x - 4, y + 6), (x + 4, y + 6), (x + 1, y - 2)], 'H')
        for x in (-12, -6, 0, 6, 12):
            p.poly([(x - 3, 42), (x + 3, 42), (x, 47)], 'H')
    p.px([(-10, 16), (-9, 15), (-8, 15), (-7, 14), (-6, 14), (-5, 14), (4, 15), (5, 15)], 'L')
    if not boy:
        p.poly([(-20, 13), (-16, 16), (-12, 13), (-12, 20), (-16, 16), (-20, 20)], 'R')


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
    im.alpha_composite(lower.im, (0, -1))
    im.alpha_composite(upper.im, (0, bob - 1))
    im = outline(im)
    if d == 'right':
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im


CHARS = {
    'haru': {
        'gender': 'boy',
        'pal': {
            'H': '#3a3c44', 'h': '#25272d', 'L': '#6a6e7a',
            'S': '#f7dcc4', 's': '#e2b597', 'n': '#d8a282', 'm': '#c9826e',
            'E': '#2a2022', 'I': '#3b3436', 'e': '#ffffff',
            'W': '#f7f7f3', 'w': '#cdd0d8', 'P': '#2f3242', 'q': '#1f2130', 'B': '#2a2220', 'b': '#5a4a42',
        },
    },
    'yui': {
        'gender': 'girl',
        'pal': {
            'H': '#94593a', 'h': '#663922', 'L': '#c48a63',
            'S': '#f8ddc6', 's': '#e4b89b', 'n': '#d8a282', 'm': '#c9806c',
            'E': '#2e1d1a', 'I': '#7a4430', 'e': '#ffffff',
            'W': '#f7f7f3', 'w': '#d0d3da', 'N': '#2f3e68', 'R': '#c8343f',
            'K': '#2f3e68', 'k': '#1f2a4a', 'B': '#4a3226', 'b': '#7a5a44',
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
