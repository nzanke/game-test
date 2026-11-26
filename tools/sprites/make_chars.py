"""キャラクターの歩行グラフィックを一から描いて img/chars/*.png に書き出す（1コマ48px、等倍表示）。

使い方：python3 tools/sprites/make_chars.py
横3コマ（左足・立ち・右足）×縦4段（下・左・右・上）。
部品（顔・髪・前髪・目・胴・腕・脚）を図形で描き、最後に輪郭を自動でつける。
右向きは左向きを左右反転して作る。座標は 48×48 のコマの中のピクセル位置。
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
F = 48
OUTLINE = (38, 26, 26, 255)


def hexc(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


class Pen:
    """パレットの文字で色を指定して描く道具"""

    def __init__(self, pal):
        self.pal = {k: hexc(v) for k, v in pal.items()}
        self.im = Image.new('RGBA', (F, F), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def c(self, k):
        return self.pal[k]

    def ell(self, box, k, shade=None):
        """楕円。shade を渡すと右下に影の縁をつける"""
        if shade:
            self.d.ellipse(box, fill=self.c(shade))
            x0, y0, x1, y1 = box
            self.d.ellipse((x0, y0, x1 - 2, y1 - 2), fill=self.c(k))
        else:
            self.d.ellipse(box, fill=self.c(k))

    def rect(self, box, k, shade=None):
        if shade:
            self.d.rectangle(box, fill=self.c(shade))
            x0, y0, x1, y1 = box
            self.d.rectangle((x0, y0, x1 - 1, y1 - 1), fill=self.c(k))
        else:
            self.d.rectangle(box, fill=self.c(k))

    def poly(self, pts, k):
        self.d.polygon(pts, fill=self.c(k))

    def px(self, pts, k):
        for p in pts:
            self.d.point(p, fill=self.c(k))


# ---------------- 部品 ----------------
LIFT = {0: (2, 0), 1: (0, 0), 2: (0, 2)}  # コマごとに（左足、右足）を上げる量


def legs_front(p, ch, step):
    la, ra = LIFT[step]
    if ch['gender'] == 'boy':
        p.rect((18, 37 - la, 22, 43 - la), 'P', 'q')
        p.rect((26, 37 - ra, 30, 43 - ra), 'P', 'q')
        p.rect((17, 43 - la, 22, 45 - la), 'B')
        p.rect((26, 43 - ra, 31, 45 - ra), 'B')
    else:
        p.rect((19, 39 - la, 21, 42 - la), 'S', 's')
        p.rect((27, 39 - ra, 29, 42 - ra), 'S', 's')
        p.rect((19, 42 - la, 21, 43 - la), 'W')
        p.rect((27, 42 - ra, 29, 43 - ra), 'W')
        p.rect((18, 44 - la, 22, 45 - la), 'B')
        p.rect((26, 44 - ra, 30, 45 - ra), 'B')


def legs_side(p, ch, step):
    if ch['gender'] == 'boy':
        if step == 1:
            p.rect((20, 37, 27, 43), 'P', 'q')
            p.rect((18, 43, 27, 45), 'B')
        else:
            back, front = ('q', 'P') if step == 0 else ('P', 'q')
            p.rect((24, 37, 28, 42), back)
            p.rect((24, 42, 30, 44), 'B')
            p.rect((17, 37, 21, 42), front)
            p.rect((15, 42, 21, 44), 'B')
    else:
        if step == 1:
            p.rect((22, 39, 25, 42), 'S', 's')
            p.rect((22, 42, 25, 43), 'W')
            p.rect((20, 44, 25, 45), 'B')
        else:
            p.rect((26, 39, 28, 42), 'S', 's')
            p.rect((26, 42, 28, 43), 'W')
            p.rect((26, 43, 30, 44), 'B')
            p.rect((18, 39, 20, 42), 'S', 's')
            p.rect((18, 42, 20, 43), 'W')
            p.rect((15, 43, 20, 44), 'B')


def body_front(p, ch, back=False):
    # 腕（半袖）
    for x0 in (13, 31):
        p.rect((x0, 28, x0 + 4, 31), 'W', 'w')
        p.rect((x0 + 1, 32, x0 + 3, 36), 'S', 's')
    if ch['gender'] == 'girl':
        p.poly([(17, 34), (31, 34), (34, 40), (14, 40)], 'K')
        for x in (18, 22, 26, 30):
            p.d.line([(x, 36), (x + (1 if x > 24 else -1), 40)], fill=p.c('k'))
    p.rect((17, 27, 31, 37 if ch['gender'] == 'boy' else 35), 'W', 'w')
    if ch['gender'] == 'boy':
        p.rect((17, 36, 31, 37), 'P')
        if not back:
            p.poly([(21, 27), (27, 27), (24, 30)], 'w')
    else:
        if back:
            p.rect((17, 27, 31, 32), 'N')
            p.d.line([(17, 31), (31, 31)], fill=p.c('W'))
        else:
            p.poly([(17, 27), (31, 27), (29, 31), (24, 33), (19, 31)], 'N')
            p.poly([(21, 27), (27, 27), (24, 31)], 'W')
            p.poly([(22, 31), (26, 31), (25, 34), (23, 34)], 'R')


def body_side(p, ch, step):
    swing = {0: -2, 1: 0, 2: 2}[step]
    if ch['gender'] == 'girl':
        p.poly([(18, 34), (29, 34), (31, 40), (16, 40)], 'K')
        p.d.line([(21, 36), (20, 40)], fill=p.c('k'))
        p.d.line([(26, 36), (27, 40)], fill=p.c('k'))
    p.rect((19, 27, 29, 37 if ch['gender'] == 'boy' else 35), 'W', 'w')
    if ch['gender'] == 'boy':
        p.rect((19, 36, 29, 37), 'P')
    else:
        p.poly([(24, 27), (30, 27), (30, 31), (26, 31)], 'N')
        p.poly([(19, 30), (21, 30), (21, 33), (19, 33)], 'R')
    # 手前の腕（歩くと前後にふれる）
    p.rect((22, 28, 26, 31), 'W', 'w')
    p.rect((23 + swing, 32, 25 + swing, 36), 'S', 's')


def hair_highlight(p, pts):
    p.px(pts, 'L')


def head_front(p, ch):
    boy = ch['gender'] == 'boy'
    if not boy:  # 肩までの髪（後ろ）とサイドテール
        p.rect((11, 14, 15, 32), 'H', 'h')
        p.rect((33, 14, 37, 32), 'H', 'h')
        p.poly([(36, 8), (42, 10), (43, 20), (41, 30), (38, 27), (37, 14)], 'h')
        p.poly([(36, 9), (41, 11), (41, 20), (39, 27), (37, 14)], 'H')
    p.ell((11, 1, 37, 25), 'H', 'h')
    if boy:  # とがった髪
        p.poly([(14, 6), (11, 0), (19, 3)], 'H')
        p.poly([(21, 3), (24, -2), (28, 3)], 'H')
        p.poly([(29, 3), (37, 0), (34, 7)], 'H')
        p.poly([(11, 12), (8, 16), (12, 18)], 'H')
        p.poly([(37, 12), (40, 16), (36, 18)], 'H')
    p.rect((22, 26, 26, 28), 's')
    p.ell((14, 9, 34, 29), 'S', 's')
    if boy:
        p.poly([(13, 9), (35, 9), (35, 17), (32, 13), (29, 18), (26, 12), (23, 18), (20, 13), (17, 17), (14, 13), (13, 17)], 'H')
        p.rect((12, 12, 14, 21), 'H')
        p.rect((34, 12, 36, 21), 'H')
        hair_highlight(p, [(17, 5), (18, 5), (19, 5), (20, 4), (21, 4), (16, 6)])
        p.px([(23, 25), (24, 25)], 'm')
    else:
        p.poly([(13, 9), (35, 9), (35, 15), (31, 13), (28, 16), (24, 12), (20, 16), (17, 13), (13, 15)], 'H')
        p.rect((12, 12, 14, 22), 'H')
        p.rect((34, 12, 36, 22), 'H')
        hair_highlight(p, [(17, 5), (18, 5), (19, 5), (20, 4), (21, 4), (16, 6), (27, 5), (28, 5)])
        # 大きな目（まつげ・瞳・光）
        for x0 in (17, 28):
            p.rect((x0 - 1, 17, x0 + 3, 17), 'E')
            p.rect((x0, 18, x0 + 3, 21), 'I')
            p.rect((x0, 21, x0 + 3, 21), 'J')
            p.px([(x0 + 1, 18), (x0 + 1, 19)], 'e')
        p.px([(16, 23), (17, 23), (31, 23), (32, 23)], 'p')
        p.px([(23, 25), (24, 25)], 'm')
        p.poly([(34, 4), (37, 7), (40, 4), (40, 9), (37, 7), (34, 10)], 'R')


def head_side(p, ch):
    boy = ch['gender'] == 'boy'
    if not boy:
        p.poly([(26, 12), (37, 12), (36, 32), (28, 32)], 'h')
        p.poly([(27, 12), (36, 12), (35, 31), (29, 31)], 'H')
        p.poly([(35, 6), (42, 9), (42, 20), (39, 28), (36, 22)], 'h')
        p.poly([(35, 7), (41, 10), (40, 20), (38, 26), (36, 20)], 'H')
    p.ell((12, 1, 37, 26), 'H', 'h')
    if boy:
        p.poly([(29, 3), (39, 0), (35, 8)], 'H')
        p.poly([(33, 10), (41, 9), (36, 16)], 'H')
        p.poly([(17, 4), (19, -1), (24, 3)], 'H')
        p.poly([(31, 20), (37, 23), (31, 25)], 'H')
    p.rect((19, 26, 24, 28), 's')
    p.ell((10, 10, 28, 29), 'S', 's')
    p.poly([(26, 9), (37, 9), (37, 24), (30, 27), (26, 22)], 'H')
    if boy:
        p.poly([(10, 9), (27, 9), (26, 16), (23, 12), (20, 17), (17, 12), (14, 16), (11, 13), (10, 15)], 'H')
        hair_highlight(p, [(20, 5), (21, 5), (22, 5), (23, 4)])
        p.px([(12, 25), (13, 25)], 'm')
    else:
        p.poly([(10, 9), (27, 9), (26, 15), (22, 12), (18, 16), (15, 12), (11, 15), (10, 14)], 'H')
        hair_highlight(p, [(20, 5), (21, 5), (22, 5), (23, 4), (28, 5)])
        p.rect((11, 17, 15, 17), 'E')
        p.rect((12, 18, 15, 21), 'I')
        p.rect((12, 21, 15, 21), 'J')
        p.px([(13, 18), (13, 19)], 'e')
        p.px([(11, 23), (12, 23)], 'p')
        p.px([(12, 25), (13, 25)], 'm')
        p.poly([(31, 3), (34, 6), (37, 3), (37, 8), (34, 6), (31, 9)], 'R')


def head_back(p, ch):
    boy = ch['gender'] == 'boy'
    p.rect((22, 24, 26, 28), 's')
    if not boy:
        p.rect((12, 16, 36, 33), 'H', 'h')
        p.poly([(12, 8), (6, 10), (5, 20), (7, 30), (10, 27), (11, 14)], 'h')
        p.poly([(12, 9), (7, 11), (7, 20), (9, 27), (11, 14)], 'H')
    p.ell((11, 1, 37, 27), 'H', 'h')
    if boy:
        p.poly([(14, 6), (11, 0), (19, 3)], 'H')
        p.poly([(21, 3), (24, -2), (28, 3)], 'H')
        p.poly([(29, 3), (37, 0), (34, 7)], 'H')
        for x in (16, 21, 26, 31):
            p.poly([(x - 2, 24), (x, 29), (x + 2, 24)], 'H')
        hair_highlight(p, [(18, 5), (19, 5), (20, 5), (21, 4), (22, 4), (17, 6)])
    else:
        hair_highlight(p, [(18, 5), (19, 5), (20, 5), (21, 4), (22, 4), (17, 6), (27, 5), (28, 5)])
        p.poly([(8, 4), (11, 7), (14, 4), (14, 9), (11, 7), (8, 10)], 'R')


def outline(im):
    src = im.load()
    out = im.copy()
    dst = out.load()
    for y in range(F):
        for x in range(F):
            if src[x, y][3]:
                continue
            if any(0 <= x + dx < F and 0 <= y + dy < F and src[x + dx, y + dy][3]
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
    im = lower.im
    im.alpha_composite(upper.im, (0, bob))
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
    sheet = Image.new('RGBA', (F * 3, F * 4), (0, 0, 0, 0))
    for r, d in enumerate(['down', 'left', 'right', 'up']):
        for s in range(3):
            sheet.paste(frame(ch, d, s), (s * F, r * F))
    return sheet


if __name__ == '__main__':
    out = ROOT / 'img' / 'chars'
    out.mkdir(parents=True, exist_ok=True)
    for name, ch in CHARS.items():
        render(ch).save(out / f'{name}.png')
        print(f'img/chars/{name}.png')
