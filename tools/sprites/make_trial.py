"""試作：美少女アニメ風の歩行グラフィック（設定なしの自由制作）。img/chars/trial.png に書き出す。

使い方：python3 tools/sprites/make_trial.py
1コマ64×96px、横3コマ（左足・立ち・右足）×縦4段（下・左・右・上）、等倍。
版4：「イラストをドットに落とし込んだ」描き方。6倍の大きさでなめらかな面・グラデーション・柔らかい影と光で
イラストとして描き、最後に64×96pxへ縮める（縮めるときに色が混ざって、輪郭や陰影がなめらかになる）。
体つきは約4頭身・やや上から見下ろす角度（頭頂が見え顔は下寄り、体は下へすぼまる）。
座標は 64×96 のコマの中の位置（x は体の中心 CX からのずれ）。
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
FW, FH, CX = 64, 96, 32
SS = 6  # 描くときの倍率


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


C = {k: rgb(v) for k, v in {
    'hair1': '#343a62', 'hair2': '#16172a', 'hairL': '#7d8fd6', 'hairLine': '#0e0f1c',
    'skin1': '#fff0e4', 'skin2': '#f4cdb6', 'skinS': '#d99b86', 'skinLine': '#a8685a', 'blush': '#ff8f96',
    'eyeW': '#ffffff', 'iris1': '#2a1650', 'iris2': '#8a5ad8', 'iris3': '#d8c2ff', 'lash': '#1a0f1c',
    'mouth': '#c85a5e', 'ribbon1': '#ee4a5e', 'ribbon2': '#9a1f34',
    'blouse1': '#ffffff', 'blouse2': '#d8dbe6', 'card1': '#f7ecd4', 'card2': '#cdb88f', 'cardLine': '#8c7754',
    'skirt1': '#8e93a6', 'skirt2': '#4f5366', 'plaid': '#3f4252', 'plaidR': '#b84a5a',
    'tights1': '#4a4556', 'tights2': '#1c1a22', 'shoe1': '#7a5a4c', 'shoe2': '#2e201c', 'line': '#2a1e2a',
}.items()}


class Art:
    """6倍の大きさで描く画用紙。部品ごとに「形（マスク）」を作って、塗り・影・光・輪郭をつける"""

    def __init__(self):
        self.W, self.H = FW * SS, FH * SS
        self.im = Image.new('RGBA', (self.W, self.H), (0, 0, 0, 0))

    @staticmethod
    def P(x, y):
        return ((CX + x) * SS, y * SS)

    def mask(self, shapes):
        m = Image.new('L', (self.W, self.H), 0)
        d = ImageDraw.Draw(m)
        for kind, *a in shapes:
            if kind == 'e':
                x0, y0, x1, y1 = a
                d.ellipse(self.P(x0, y0) + self.P(x1, y1), fill=255)
            elif kind == 'p':
                d.polygon([self.P(x, y) for x, y in a[0]], fill=255)
            elif kind == 'r':
                x0, y0, x1, y1 = a
                d.rectangle(self.P(x0, y0) + self.P(x1, y1), fill=255)
        return m

    def fill(self, m, c1, c2=None, alpha=1.0):
        """マスクの範囲を、上 c1 → 下 c2 のグラデーションで塗る"""
        box = m.getbbox()
        if not box:
            return
        c2 = c2 or c1
        g = Image.new('RGBA', (1, 256))
        for i in range(256):
            t = i / 255
            g.putpixel((0, i), tuple(round(c1[j] + (c2[j] - c1[j]) * t) for j in range(3)) + (255,))
        x0, y0, x1, y1 = box
        g = g.resize((x1 - x0, max(1, y1 - y0)))
        layer = Image.new('RGBA', (self.W, self.H), (0, 0, 0, 0))
        layer.paste(g, (x0, y0))
        a = m if alpha >= 1 else m.point(lambda v: round(v * alpha))
        layer.putalpha(ImageChops.multiply(layer.getchannel('A'), a))
        self.im.alpha_composite(layer)

    def edge(self, m, dx, dy, blur):
        """光の当たらない縁（右下）を取り出してぼかす。dx・dy は最終のピクセル単位"""
        sh = ImageChops.offset(m, round(-dx * SS), round(-dy * SS))
        e = ImageChops.subtract(m, sh).filter(ImageFilter.GaussianBlur(blur * SS))
        return ImageChops.multiply(e, m)

    def tint(self, m, color, alpha=1.0):
        layer = Image.new('RGBA', (self.W, self.H), color + (0,))
        layer.putalpha(m.point(lambda v: round(v * alpha)))
        self.im.alpha_composite(layer)

    def part(self, shapes, c1, c2, shade=None, light=None, line=None, lw=0.9, sh=(1.6, 2.2), sb=1.2, la=0.55):
        m = self.mask(shapes)
        self.fill(m, c1, c2)
        if shade:
            self.tint(self.edge(m, *sh, sb), shade, 0.75)
        if light:
            self.tint(self.edge(m, -1.2, -1.2, 0.8), light, la)
        if line:
            ring = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(int(lw * SS) | 1)), m)
            self.tint(ring, line, 0.95)
        return m

    def clip(self, m, shapes, color, alpha=1.0, blur=0):
        """形 shapes を m の範囲に切り抜いて色をのせる（影や模様）"""
        s = self.mask(shapes)
        if blur:
            s = s.filter(ImageFilter.GaussianBlur(blur * SS))
        self.tint(ImageChops.multiply(s, m), color, alpha)

    def stroke(self, pts, color, w=0.6, alpha=1.0, blur=0):
        layer = Image.new('L', (self.W, self.H), 0)
        ImageDraw.Draw(layer).line([self.P(x, y) for x, y in pts], fill=255, width=max(1, round(w * SS)), joint='curve')
        if blur:
            layer = layer.filter(ImageFilter.GaussianBlur(blur * SS))
        self.tint(layer, color, alpha)

    def blob(self, x0, y0, x1, y1, color, alpha, blur):
        m = self.mask([('e', x0, y0, x1, y1)])
        if blur:
            m = m.filter(ImageFilter.GaussianBlur(blur * SS))
        self.tint(m, color, alpha)

    def shrink(self):
        im = self.im.resize((FW, FH), Image.BOX)
        return im.filter(ImageFilter.UnsharpMask(radius=0.6, percent=60, threshold=0))


LIFT = {0: (1.6, 0), 1: (0, 0), 2: (0, 1.6)}


# ---------------- 部品 ----------------
def back_hair(a, side, bob):
    b = bob
    if side == 'down':
        pts = [(-10.5, 12 + b), (10.5, 12 + b), (11.5, 50 + b), (9, 57 + b), (4, 54 + b), (0, 58 + b), (-4, 54 + b), (-9, 57 + b), (-11.5, 50 + b)]
    elif side == 'up':
        pts = [(-11.5, 11 + b), (11.5, 11 + b), (12.5, 52 + b), (9.5, 60 + b), (5, 57 + b), (0, 61 + b), (-5, 57 + b), (-9.5, 60 + b), (-12.5, 52 + b)]
    else:
        pts = [(-1, 11 + b), (10, 11 + b), (11.5, 48 + b), (9.5, 59 + b), (5, 56 + b), (2, 44 + b)]
    m = a.part([('p', pts)], C['hair1'], C['hair2'], shade=C['hair2'], line=C['hairLine'])
    xs = (-7, -3, 1, 5, 8) if side != 'left' else (3, 6, 8.5)
    for x in xs:  # 毛の流れ
        a.clip(m, [('p', [(x - 0.3, 14 + b), (x + 0.3, 14 + b), (x + (0.8 if x > 0 else -0.8), 56 + b), (x + (0.2 if x > 0 else -0.2), 56 + b)])], C['hairL'], 0.35)


def legs(a, step, side):
    la, ra = LIFT[step]
    if side == 'left':
        if step == 1:
            a.part([('p', [(-2, 70), (2, 70), (1.6, 88), (-1.8, 88)])], C['tights1'], C['tights2'], shade=C['tights2'], line=C['line'])
            a.part([('e', -5, 86.5, 2.5, 93)], C['shoe1'], C['shoe2'], light=(200, 170, 150), line=C['line'])
        else:
            a.part([('p', [(0, 70), (3, 70), (6.5, 87), (3.5, 88)])], C['tights2'], C['tights2'], line=C['line'])
            a.part([('e', 3, 85.5, 9.5, 91.5)], C['shoe1'], C['shoe2'], line=C['line'])
            a.part([('p', [(-3, 70), (0, 70), (-3.5, 88), (-6.5, 87)])], C['tights1'], C['tights2'], shade=C['tights2'], line=C['line'])
            a.part([('e', -10, 86.5, -3, 92.5)], C['shoe1'], C['shoe2'], light=(200, 170, 150), line=C['line'])
        return
    for x0, x1, lift in ((-5, -1.6, la), (1.6, 5, ra)):
        m = a.part([('p', [(x0, 70), (x1, 70), (x1 - 0.4, 88 - lift), (x0 + 0.4, 88 - lift)])], C['tights1'], C['tights2'], shade=C['tights2'], line=C['line'])
        a.clip(m, [('r', (x0 + x1) / 2 - 0.4, 71, (x0 + x1) / 2 + 0.3, 87)], (110, 100, 125), 0.5, blur=0.4)
        a.part([('e', x0 - 1.3, 86 - lift, x1 + 1.3, 93 - lift)], C['shoe1'], C['shoe2'], light=(210, 180, 160), line=C['line'], la=0.7)


def skirt(a, side, bob):
    b = bob
    w0, w1 = (8.6, 11.2) if side != 'left' else (6.4, 9)
    m = a.part([('p', [(-w0, 52 + b), (w0, 52 + b), (w1, 70 + b), (-w1, 70 + b)])], C['skirt1'], C['skirt2'], shade=C['skirt2'], line=C['line'])
    for i in range(-3, 4):  # プリーツとチェック
        x = i * (w1 / 3.6)
        a.clip(m, [('p', [(x * 0.77 - 0.25, 52 + b), (x * 0.77 + 0.25, 52 + b), (x + 0.4, 70 + b), (x - 0.4, 70 + b)])], C['plaid'], 0.6)
    a.clip(m, [('r', -12, 57.6 + b, 12, 58.3 + b)], C['plaid'], 0.55)
    a.clip(m, [('r', -12, 64 + b, 12, 64.6 + b)], C['plaidR'], 0.85)


def torso_front(a, back, bob):
    b = bob
    a.part([('r', -2, 30 + b, 2, 35 + b)], C['skin2'], C['skinS'], line=C['skinLine'])  # 首
    m = a.part([('p', [(-9.6, 33.5 + b), (9.6, 33.5 + b), (8.6, 54 + b), (-8.6, 54 + b)])], C['card1'], C['card2'],
               shade=C['card2'], light=(255, 250, 235), line=C['cardLine'])
    if not back:
        a.part([('p', [(-2.2, 33.5 + b), (2.2, 33.5 + b), (2, 53.5 + b), (-2, 53.5 + b)])], C['blouse1'], C['blouse2'], line=C['cardLine'], lw=0.6)
        a.part([('p', [(-4.4, 32.6 + b), (0, 35.6 + b), (4.4, 32.6 + b), (3.4, 36.6 + b), (0, 37.4 + b), (-3.4, 36.6 + b)])], C['blouse1'], C['blouse2'], line=C['line'], lw=0.5)
        a.part([('p', [(-3, 35.6 + b), (0, 37.2 + b), (3, 35.6 + b), (2.4, 39.6 + b), (0, 38.4 + b), (-2.4, 39.6 + b)])], C['ribbon1'], C['ribbon2'], light=(255, 200, 205), line=C['ribbon2'], lw=0.5)
        a.clip(m, [('e', -7, 42 + b, -3.5, 46 + b), ('e', 3.5, 42 + b, 7, 46 + b)], C['card2'], 0.5, blur=0.8)  # 胸のふくらみの影
        for y in (41.5, 47.5):
            a.blob(-2.9, y + b, -1.9, y + 1 + b, C['cardLine'], 0.9, 0)  # ボタン
    else:
        a.clip(m, [('r', -0.3, 36 + b, 0.3, 53 + b)], C['card2'], 0.6)
    for s in (-1, 1):  # 長袖の腕と手
        arm = [(s * 8.2, 34 + b), (s * 10.8, 35 + b), (s * 11.6, 53.5 + b), (s * 9, 54.2 + b)]
        a.part([('p', arm)], C['card1'], C['card2'], shade=C['card2'], line=C['cardLine'])
        a.part([('e', s * 10.4 - 1.7, 53 + b, s * 10.4 + 1.7, 57.4 + b)], C['skin1'], C['skin2'], shade=C['skinS'], line=C['skinLine'], lw=0.6)
        a.stroke([(s * 8.4, 33.8 + b), (s * 10.4, 34.6 + b)], (255, 252, 240), 0.7, 0.9)  # 肩の上面


def torso_side(a, step, bob):
    b = bob
    sw = {0: -2.6, 1: 0, 2: 2.6}[step]
    a.part([('r', -1.8, 30 + b, 1.4, 35 + b)], C['skin2'], C['skinS'], line=C['skinLine'])
    a.part([('p', [(-6.4, 33.5 + b), (6, 33.5 + b), (5, 54 + b), (-5.4, 54 + b)])], C['card1'], C['card2'], shade=C['card2'], light=(255, 250, 235), line=C['cardLine'])
    a.part([('p', [(-6.6, 33.5 + b), (-3.2, 33.5 + b), (-4.4, 38.5 + b)])], C['blouse1'], C['blouse2'], line=C['line'], lw=0.5)
    a.part([('p', [(-7.2, 36 + b), (-4.2, 37 + b), (-6.2, 40.5 + b)])], C['ribbon1'], C['ribbon2'], line=C['ribbon2'], lw=0.5)
    a.part([('p', [(-2, 34.5 + b), (2.2, 34.5 + b), (2 + sw, 53.5 + b), (-2 + sw, 53.5 + b)])], C['card1'], C['card2'], shade=C['card2'], line=C['cardLine'])
    a.part([('e', -1.8 + sw, 52.5 + b, 1.8 + sw, 57 + b)], C['skin1'], C['skin2'], line=C['skinLine'], lw=0.6)


def eye(a, cx, cy, flip=False, side=False):
    """アニメ風の目：白目・グラデーションの瞳・瞳孔・光2つ・太い上まつげ"""
    s = -1 if flip else 1
    w, h = (3.6, 4.6) if not side else (2.6, 4.4)
    a.part([('e', cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)], C['eyeW'], (235, 230, 245))
    a.part([('e', cx - w / 2 + 0.3, cy - h / 2 + 0.2, cx + w / 2 - 0.3, cy + h / 2)], C['iris1'], C['iris2'])
    a.blob(cx - 0.9, cy + 0.6, cx + 0.9, cy + 2.1, C['iris3'], 0.7, 0.3)
    a.blob(cx - 0.6, cy - 0.9, cx + 0.6, cy + 0.6, (15, 8, 30), 0.9, 0)
    a.blob(cx - s * 1.3 - 0.6, cy - 1.7, cx - s * 1.3 + 0.6, cy - 0.5, (255, 255, 255), 1.0, 0)
    a.blob(cx + s * 0.9 - 0.35, cy + 0.9, cx + s * 0.9 + 0.35, cy + 1.6, (255, 255, 255), 0.9, 0)
    x0, x1 = cx - w / 2 - 0.4, cx + w / 2 + 0.4
    a.stroke([(x0, cy - h / 2 + 0.6), ((x0 + x1) / 2, cy - h / 2 - 0.2), (x1, cy - h / 2 + 0.4)], C['lash'], 0.9)
    a.stroke([(cx + s * (w / 2 + 0.3), cy - h / 2 + 0.4), (cx + s * (w / 2 + 1.1), cy - h / 2 + 1.2)], C['lash'], 0.6)
    a.stroke([(cx - w / 2 + 0.5, cy + h / 2 + 0.2), (cx + w / 2 - 0.5, cy + h / 2 + 0.2)], C['skinLine'], 0.35, 0.6)


def head_front(a, bob):
    b = bob
    hm = a.part([('e', -10.6, 8.5 + b, 10.6, 30 + b)], C['hair1'], C['hair2'], shade=C['hair2'], line=C['hairLine'])
    face = [('e', -7.6, 15 + b, 7.6, 30 + b), ('p', [(-7.6, 22.5 + b), (7.6, 22.5 + b), (6.2, 27.5 + b), (2.4, 30.8 + b), (0, 31.4 + b), (-2.4, 30.8 + b), (-6.2, 27.5 + b)])]
    fm = a.part(face, C['skin1'], C['skin2'], shade=C['skinS'], sh=(1.2, 1.4), sb=1.0, line=C['skinLine'], lw=0.6)
    a.clip(fm, [('r', -9, 14 + b, 9, 19.5 + b)], C['skinS'], 0.55, blur=0.9)  # 前髪の下の影
    bang = [('r', -9.4, 11 + b, 9.4, 17 + b)]
    for x0, x1, y in [(-9.4, -5.2, 21.5), (-6, -2, 20.3), (-2.8, 1.4, 22), (0.6, 4.6, 19.8), (3.8, 7.8, 21), (7, 9.8, 22.6)]:
        bang.append(('p', [(x0, 16.5 + b), (x1, 16.5 + b), ((x0 + x1) / 2 + 0.5, y + b)]))
    bm = a.part(bang, C['hair1'], C['hair2'], shade=C['hair2'], line=C['hairLine'], lw=0.7)
    a.part([('p', [(-10.4, 15 + b), (-7.8, 15 + b), (-7.2, 31 + b), (-9.2, 34 + b), (-10.6, 25 + b)])], C['hair1'], C['hair2'], line=C['hairLine'], lw=0.7)
    a.part([('p', [(10.4, 15 + b), (7.8, 15 + b), (7.2, 31 + b), (9.2, 34 + b), (10.6, 25 + b)])], C['hair2'], C['hair2'], line=C['hairLine'], lw=0.7)
    a.clip(hm, [('e', -7.5, 11.6 + b, 1, 13.6 + b)], C['hairL'], 0.4, blur=0.6)  # つや（天使の輪。左上だけ柔らかく）
    a.clip(bm, [('e', -7.5, 11.6 + b, 1, 13.6 + b)], C['hairL'], 0.3, blur=0.6)
    eye(a, -3.8, 23.6 + b)
    eye(a, 3.8, 23.6 + b, flip=True)
    a.blob(-6.8, 26 + b, -3.2, 27.6 + b, C['blush'], 0.45, 0.6)
    a.blob(3.2, 26 + b, 6.8, 27.6 + b, C['blush'], 0.45, 0.6)
    a.blob(-0.35, 26.6 + b, 0.35, 27.4 + b, C['skinS'], 0.6, 0.2)
    a.stroke([(-0.9, 29 + b), (0, 29.3 + b), (0.9, 29 + b)], C['mouth'], 0.5)
    a.part([('p', [(4.6, 11.6 + b), (7.6, 10.4 + b), (8.2, 11.8 + b), (5.2, 13 + b)])], C['ribbon1'], C['ribbon2'], line=C['ribbon2'], lw=0.4)


def head_side(a, bob):
    b = bob
    hm = a.part([('e', -9.6, 8.5 + b, 10.4, 30 + b)], C['hair1'], C['hair2'], shade=C['hair2'], line=C['hairLine'])
    fm = a.part([('e', -10.4, 15 + b, 2.6, 30 + b), ('p', [(-10.4, 22.5 + b), (1.4, 22.5 + b), (0, 28 + b), (-3.4, 30.8 + b), (-6, 31.4 + b), (-9.8, 28 + b)])],
                C['skin1'], C['skin2'], shade=C['skinS'], line=C['skinLine'], lw=0.6)
    a.clip(fm, [('r', -11, 14 + b, 3, 19.5 + b)], C['skinS'], 0.55, blur=0.9)
    bang = [('r', -9.8, 11 + b, 2, 17 + b)]
    for x0, x1, y in [(-10.4, -6.4, 21.5), (-7.2, -3.2, 20.3), (-4, 0, 21.6), (-0.8, 2.8, 19.6)]:
        bang.append(('p', [(x0, 16.5 + b), (x1, 16.5 + b), ((x0 + x1) / 2, y + b)]))
    a.part(bang, C['hair1'], C['hair2'], shade=C['hair2'], line=C['hairLine'], lw=0.7)
    a.part([('p', [(0.6, 13 + b), (9.6, 13 + b), (9, 29 + b), (4, 32 + b), (1.2, 25 + b)])], C['hair1'], C['hair2'], shade=C['hair2'], line=C['hairLine'], lw=0.7)
    a.clip(hm, [('e', -5, 11.6 + b, 4, 13.6 + b)], C['hairL'], 0.4, blur=0.6)
    eye(a, -7.2, 23.6 + b, side=True)
    a.blob(-9.6, 26 + b, -6.4, 27.6 + b, C['blush'], 0.45, 0.6)
    a.stroke([(-10, 29 + b), (-9.2, 29.2 + b)], C['mouth'], 0.5)
    a.part([('p', [(5, 11.6 + b), (8, 10.4 + b), (8.6, 11.8 + b), (5.6, 13 + b)])], C['ribbon1'], C['ribbon2'], line=C['ribbon2'], lw=0.4)


def head_back(a, bob):
    b = bob
    hm = a.part([('e', -10.6, 8.5 + b, 10.6, 30 + b)], C['hair1'], C['hair2'], shade=C['hair2'], line=C['hairLine'])
    a.clip(hm, [('e', -7.5, 11.6 + b, 1, 13.6 + b)], C['hairL'], 0.4, blur=0.6)
    a.part([('p', [(-7.6, 11.6 + b), (-4.6, 10.4 + b), (-4, 11.8 + b), (-7, 13 + b)])], C['ribbon1'], C['ribbon2'], line=C['ribbon2'], lw=0.4)


def frame(d, step):
    side = 'left' if d in ('left', 'right') else d
    bob = 0 if step == 1 else 0.6
    a = Art()
    if side != 'up':
        back_hair(a, side, bob)
    legs(a, step, side)
    if side == 'left':
        skirt(a, 'left', bob); torso_side(a, step, bob); head_side(a, bob)
    elif side == 'up':
        skirt(a, 'down', bob); torso_front(a, True, bob); back_hair(a, 'up', bob); head_back(a, bob)
    else:
        skirt(a, 'down', bob); torso_front(a, False, bob); head_front(a, bob)
    im = a.shrink()
    return im.transpose(Image.FLIP_LEFT_RIGHT) if d == 'right' else im


if __name__ == '__main__':
    sheet = Image.new('RGBA', (FW * 3, FH * 4), (0, 0, 0, 0))
    for r, d in enumerate(['down', 'left', 'right', 'up']):
        for s in range(3):
            sheet.paste(frame(d, s), (s * FW, r * FH))
    out = ROOT / 'img' / 'chars' / 'trial.png'
    sheet.save(out)
    print(out.relative_to(ROOT))
