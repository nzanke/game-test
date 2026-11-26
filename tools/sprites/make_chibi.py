"""ちびキャラ（手本：RPGツクールMVの標準キャラの比率、約1.5頭身）でハルとユイを描く。

使い方：python3 tools/sprites/make_chibi.py
1コマ48×48px、横3コマ（左足・立ち・右足）×縦4段（下・左・右・上）、等倍。
塗りは手本と同じくっきりしたドット絵（48×48pxに直接描く。ベタ塗り、段をつけた影と光、部品ごとに1ドットの濃い輪郭）。
（Art = Chibi にすると、6倍で描いて縮める柔らかい塗りになる）
比率は手本を測った値：頭（髪）y5〜33・横31px、前髪は目のすぐ上まで、大きな目（y25〜29）、首なし、胴 y33〜43、足 y44〜47。
座標は 48×48 のコマの中の位置（x は体の中心からのずれ）。手本の絵は写さない。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_trial as mt  # noqa: E402
from PIL import Image, ImageFilter, ImageChops, ImageDraw  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
FW = FH = 48
CX = 24
SS = mt.SS
rgb = mt.rgb


class Chibi(mt.Art):
    def __init__(self):
        self.W, self.H = FW * SS, FH * SS
        self.im = Image.new('RGBA', (self.W, self.H), (0, 0, 0, 0))

    @staticmethod
    def P(x, y):
        return ((CX + x) * SS, y * SS)

    def shrink(self):
        im = self.im.resize((FW, FH), Image.BOX)
        return im.filter(ImageFilter.UnsharpMask(radius=0.6, percent=70, threshold=0))


class Pixel(Chibi):
    """手本と同じ、くっきりしたドット絵の塗り：48×48pxに直接描く。ベタ塗り、影と光は段をつけ、部品ごとに1ドットの濃い輪郭"""

    def __init__(self):
        self.W, self.H = FW, FH
        self.im = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))

    @staticmethod
    def P(x, y):
        return (round(CX + x), round(y))

    def fill(self, m, c1, c2=None, alpha=1.0):
        super().fill(m, c1, c1, alpha)

    def edge(self, m, dx, dy, blur):
        sh = ImageChops.offset(m, round(-dx), round(-dy))
        e = ImageChops.subtract(m, sh)
        return ImageChops.multiply(e.point(lambda v: 255 if v > 127 else 0), m)

    def part(self, shapes, c1, c2, shade=None, light=None, line=None, lw=0.9, sh=(1.6, 2.2), sb=1.2, la=0.55):
        m = self.mask(shapes)
        self.fill(m, c1)
        if shade:
            self.tint(self.edge(m, *sh, 0), shade, 1.0)
        if light:
            self.tint(self.edge(m, -1, -1, 0), light, 1.0)
        if line:
            ring = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(3)), m)
            self.tint(ring, line, 1.0)
        return m

    def clip(self, m, shapes, color, alpha=1.0, blur=0):
        self.tint(ImageChops.multiply(self.mask(shapes), m), color, alpha)

    def dots(self, x0, y0, rows, pal):
        """1ドットずつ描く：rows の文字を pal の色で置く（'.' は何もしない）"""
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch != '.':
                    self.im.putpixel((CX + x0 + i, y0 + j), pal[ch] + (255,))

    def stroke(self, pts, color, w=0.6, alpha=1.0, blur=0):
        layer = Image.new('L', (self.W, self.H), 0)
        ImageDraw.Draw(layer).line([self.P(x, y) for x, y in pts], fill=255, width=1)
        self.tint(layer, color, 1.0)

    def blob(self, x0, y0, x1, y1, color, alpha, blur):
        self.tint(self.mask([('e', x0, y0, x1, y1)]), color, 1.0 if alpha >= 0.5 else alpha)

    def shrink(self):
        return self.im


BASE = {
    'skin1': '#fbdcc8', 'skin2': '#f6bf9c', 'skinS': '#e2916f', 'skinLine': '#5a2c20', 'blush': '#ff8f96',
    'eyeW': '#ffffff', 'lash': '#1a0f1c', 'mouth': '#c85a5e', 'line': '#2a1e2a',
}
CHARS = {
    'yui_chibi': dict(BASE, girl=True, **{
        'hair1': '#343a62', 'hair2': '#16172a', 'hairL': '#55609a', 'hairLine': '#0e0f1c',
        'iris1': '#5a3aa0', 'iris2': '#8a5ad8', 'iris3': '#d8c2ff',
        'top1': '#f7ecd4', 'top2': '#cdb88f', 'topLine': '#8c7754', 'inner': '#ffffff', 'ribbon1': '#ee4a5e', 'ribbon2': '#9a1f34',
        'low1': '#8e93a6', 'low2': '#4f5366', 'leg': '#2a2730', 'shoe1': '#7a5a4c', 'shoe2': '#2e201c',
    }),
    'haru_chibi': dict(BASE, girl=False, **{
        'hair1': '#3c3f4c', 'hair2': '#16171d', 'hairL': '#626778', 'hairLine': '#0d0d12',
        'iris1': '#5a3a28', 'iris2': '#8a6040', 'iris3': '#c09a78',
        'top1': '#ffffff', 'top2': '#d6dbe6', 'topLine': '#7d8496', 'inner': '#f1c9b1', 'ribbon1': '#2a2420', 'ribbon2': '#2a2420',
        'low1': '#3d4360', 'low2': '#1b1e2c', 'leg': '#1b1e2c', 'shoe1': '#4a4446', 'shoe2': '#101012',
    }),
}


def colors(ch):
    return {k: (rgb(v) if isinstance(v, str) else v) for k, v in ch.items()}


# ---------------- 体（首なし・胴は短い・足は小さい） ----------------
def body(a, c, side, step, back):
    """首なし・胴は短い。やや上から見下ろしつつ、足先まで全身を見せる（胴→スカート／ズボン→脚→甲の見える靴）"""
    girl = c['girl']
    la, ra = {0: (1.2, 0), 1: (0, 0), 2: (0, 1.2)}[step]
    if side == 'left':
        sw = {0: -1.6, 1: 0, 2: 1.6}[step]
        if girl:
            a.part([('p', [(-5.8, 37.4), (5.8, 37.4), (7.6, 43.6), (-7.6, 43.6)])], c['low1'], c['low2'], shade=c['low2'], line=c['line'], lw=0.7)
        else:
            a.part([('p', [(-4.2, 38.6), (4.2, 38.6), (4.4, 43.6), (-4.4, 43.6)])], c['low1'], c['low2'], shade=c['low2'], line=c['line'], lw=0.7)
        a.part([('p', [(-3.8, 34), (4, 34), (4.4, 39.4), (-4.2, 39.4)]), ('e', -6.4, 31.4, 6.4, 37)], c['top1'], c['top2'], shade=c['top2'], line=c['topLine'], lw=0.7)
        a.part([('p', [(-1.8, 33.2), (2, 33.2), (2 + sw, 38.4), (-1.8 + sw, 38.4)])], c['top1'], c['top2'], line=c['topLine'], lw=0.6)
        a.part([('e', -2.3 + sw, 37.2, 2.3 + sw, 41.4)], c['skin1'], c['skin2'], shade=c['skinS'], line=c['skinLine'], lw=0.5)
        if girl:
            a.part([('p', [(-5.4, 32.6), (-3, 32.6), (-4, 35.4)])], c['ribbon1'], c['ribbon2'], lw=0.4)
        feet(a, c, 'side', step)
        return
    # 脚と靴（靴は甲が見える）
    if girl:
        a.part([('p', [(-5.6, 37.4), (5.6, 37.4), (7.8, 43.6), (-7.8, 43.6)])], c['low1'], c['low2'], shade=c['low2'], line=c['line'], lw=0.7)
    else:
        for x0, x1, l in ((-4.6, -0.4, la), (0.4, 4.6, ra)):
            a.part([('p', [(x0, 38.6), (x1, 38.6), (x1, 43.6), (x0, 43.6)])], c['low1'], c['low2'], shade=c['low2'], line=c['line'], lw=0.7)
    for s in (-1, 1):  # 腕：大きな肩から外へ開く
        a.part([('p', [(s * 7.2, 35.4), (s * 9.8, 35.4), (s * 10.8, 38.4), (s * 8.4, 39.2)])], c['top1'], c['top2'], shade=c['top2'], line=c['topLine'], lw=0.6)
    # 胴は細く、肩は大きく（上から見下ろすので、肩の丸みと上の面が見える）
    m = a.part([('p', [(-5.2, 35), (5.2, 35), (5.8, 39.6), (-5.8, 39.6)]), ('e', -10.2, 32.6, -2.4, 38.2), ('e', 2.4, 32.6, 10.2, 38.2)],
               c['top1'], c['top2'], shade=c['top2'], light=(255, 252, 240), line=c['topLine'], lw=0.7)
    for s in (-1, 1):
        a.stroke([(s * 9, 34.2), (s * 4, 33.4)], (255, 253, 244))  # 肩の上の面（あごの下に見える）
        a.part([('e', s * 9.8 - 2.4, 36.8, s * 9.8 + 2.4, 41.4)], c['skin1'], c['skin2'], shade=c['skinS'], line=c['skinLine'], lw=0.5)  # 大きめの手
    if not back:
        if girl:
            a.clip(m, [('p', [(-1.4, 32.4), (1.4, 32.4), (1.4, 39.6), (-1.4, 39.6)])], c['inner'], 1.0)
            a.part([('p', [(-2.4, 32.4), (0, 34), (2.4, 32.4), (1.8, 35.6), (0, 34.8), (-1.8, 35.6)])], c['ribbon1'], c['ribbon2'], lw=0.4)
        else:
            a.clip(m, [('p', [(-1.8, 32.4), (1.8, 32.4), (0, 35)])], c['inner'], 1.0)
            a.clip(m, [('r', -0.2, 35, 0.2, 38.4)], c['topLine'], 0.7)
    if not girl:
        a.part([('r', -5.6, 38.2, 5.6, 39.6)], c['ribbon1'], c['ribbon2'], lw=0.4)  # ベルト
    feet(a, c, 'front', step)


def feet(a, c, side, step):
    """手本どおり：左右の足は幅5ドット（輪郭＋中身3）で間に1ドットのすき間。脚1ドット・靴2ドット（上が明るく下が暗い）。
    歩くと上げた足が1ドット上がる"""
    leg = c['skin2'] if c['girl'] else c['low1']  # 女子は素足（肌色）
    pal = {'o': c['line'], 'l': leg, 's': c['shoe1'], 'd': c['shoe2']}
    foot = ['olllo', 'ossso', 'odddo']
    if side == 'front':
        lift = {0: (1, 0), 1: (0, 0), 2: (0, 1)}[step]
        for x0, l in ((-5, lift[0]), (1, lift[1])):
            a.dots(x0, 45 - l, foot, pal)
    else:
        if step == 1:
            a.dots(-3, 45, foot, pal)
        else:
            a.dots(1, 44, ['olllo', 'odddo', 'odddo'], pal)  # 奥の足（上がっている）
            a.dots(-6, 45, foot, pal)


# ---------------- 頭（大きく、前髪は目のすぐ上まで、目は大きく下寄り） ----------------
# 左の目（外側が左）。E まつげ／g 影の白目／w 白目／i 濃い黒目／I 黒目／K 明るい黒目／P 瞳孔
EYE_GIRL = ['EEEE.', 'giEEE', 'wiPig', 'wIPIw', 'wKKKw']   # 女子は外側にまつげを1ドット足す
EYE_BOY = ['.EEE.', 'giEEE', 'wiPig', 'wIPIw', 'wKKKw']


def eye(a, c, cx, flip=False, side=False):
    if isinstance(a, Pixel):
        rows = EYE_GIRL if c['girl'] else EYE_BOY
        if side:
            rows = [r[1:] for r in rows]
        if flip:
            rows = [r[::-1] for r in rows]
        w = len(rows[0])
        pal = {'E': c['lash'], 'P': c['lash'], 'w': (255, 255, 255), 'g': (214, 208, 216), 'i': c['iris1'], 'I': c['iris2'], 'K': c['iris3']}
        # 左の目は白目が外側（左）、右の目は反転して外側（右）
        a.dots(round(cx) - w // 2, 25, rows, pal)
        return
    s = -1 if flip else 1
    w, h = (3.6, 4.6) if not side else (2.6, 4.4)
    cy = 27.2
    if not c['girl']:
        h -= 0.8
    a.part([('e', cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)], c['eyeW'], (235, 230, 245))
    a.part([('e', cx - w / 2 + 0.25, cy - h / 2 + 0.1, cx + w / 2 - 0.25, cy + h / 2)], c['iris1'], c['iris2'])
    a.blob(cx - 0.9, cy + 0.5, cx + 0.9, cy + 2, c['iris3'], 0.6, 0.3)
    a.blob(cx - s * 1.0 - 0.6, cy - 1.7, cx - s * 1.0 + 0.6, cy - 0.5, (255, 255, 255), 1.0, 0)
    if c['girl']:
        a.blob(cx + s * 0.8 - 0.3, cy + 0.9, cx + s * 0.8 + 0.3, cy + 1.5, (255, 255, 255), 0.9, 0)
    x0, x1 = cx - w / 2 - 0.4, cx + w / 2 + 0.4
    a.stroke([(x0, cy - h / 2 + 0.5), ((x0 + x1) / 2, cy - h / 2 - 0.2), (x1, cy - h / 2 + 0.4)], c['lash'], 0.9)
    if c['girl']:
        a.stroke([(cx + s * (w / 2 + 0.3), cy - h / 2 + 0.4), (cx + s * (w / 2 + 1.1), cy - h / 2 + 1.1)], c['lash'], 0.6)


def bangs(a, c, x0, x1, tips, top=12, base=21.6, face=None):
    shapes = [('r', x0, top, x1, base)]
    for tx0, tx1, y in tips:
        shapes.append(('p', [(tx0, base - 0.5), (tx1, base - 0.5), ((tx0 + tx1) / 2, y)]))
    if isinstance(a, Pixel) and face is not None:
        # ドット絵では、前髪の輪郭は顔と接するところ（毛先）にだけ引く（頭の中に四角い線が出ないように）
        m = a.part(shapes, c['hair1'], c['hair2'])
        ring = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(3)), m)
        a.tint(ImageChops.multiply(ring, face), c['hairLine'], 1.0)
        below = lambda n: ImageChops.multiply(ImageChops.subtract(ImageChops.offset(m, 0, n), m.filter(ImageFilter.MaxFilter(3)) if n > 1 else m), face)
        a.tint(below(3), c['skin2'], 1.0)
        a.tint(below(2), c['skinS'], 1.0)
        for k, (tx0, tx1, y) in enumerate(tips):  # 1本おきの毛束に短い明るい筋、束の間に暗い線
            mx = (tx0 + tx1) / 2
            if k % 2 == 1:
                a.stroke([(mx - 0.6, base - 4), (mx - 0.4, base - 1)], c['hairL'])
            a.stroke([(tx1, base - 3), (tx1 - 0.2, base)], c['hair2'])
        return m
    return a.part(shapes, c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'], lw=0.7)


def head(a, c, side):
    girl = c['girl']
    if side == 'up':
        if girl:
            a.part([('p', [(-15.6, 18), (15.6, 18), (15, 36), (10, 38.6), (0, 37.4), (-10, 38.6), (-15, 36)])], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
        hm = a.part([('e', -15.2, 7 if girl else 6.4, 15.2, 33.4)], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
        if not girl:
            a.part([('p', [(x - 3, 30), (x + 3, 30), (x, 34)]) for x in (-8, -3, 3, 8)], c['hair1'], c['hair2'], line=c['hairLine'], lw=0.6)
        if isinstance(a, Pixel):
            a.stroke([(-10, 10), (-6, 8), (-1, 8)], c['hairL'])
        else:
            a.clip(hm, [('e', -11, 8.4, 1, 11.6)], c['hairL'], 0.45, blur=0.6)
        return
    if side == 'left':
        if girl:
            a.part([('p', [(1, 14), (15.6, 14), (15, 36), (9, 38.6), (3, 33)])], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
        hm = a.part([('e', -14.2, 7 if girl else 6.4, 14.6, 33)], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
        fm = a.part([('e', -15.4, 15.6, 3.6, 33.6)], c['skin1'], c['skin2'], shade=c['skinS'], line=c['skinLine'], lw=0.6)
        a.clip(fm, [('r', -16, 17, 4, 19.4)], c['skinS'], 0.5, blur=0.8)
        bangs(a, c, -15.2, 3, [(-15.6, -12, 22.6), (-11.6, -8.6, 20.6), (-8, -5, 21.8), (-4.4, -1.4, 20.4), (-0.8, 2.6, 21.4)], base=18, face=fm)
        sideline = None if isinstance(a, Pixel) else c['hairLine']
        sm = a.part([('p', [(4.6, 14), (14.4, 14), (14, 28.4), (8.6, 32.4), (5.6, 26)])], c['hair1'], c['hair2'], shade=None if isinstance(a, Pixel) else c['hair2'], line=sideline, lw=0.7)
        if isinstance(a, Pixel):
            a.tint(ImageChops.multiply(ImageChops.subtract(sm.filter(ImageFilter.MaxFilter(3)), sm), fm), c['hairLine'], 1.0)
        if isinstance(a, Pixel):
            a.stroke([(-6, 9), (-2, 7), (3, 7)], c['hairL'])
        else:
            a.clip(hm, [('e', -8, 8.4, 6, 11.6)], c['hairL'], 0.45, blur=0.6)
        eye(a, c, -10.4, side=True)
        if girl:
            a.blob(-13.4, 29.8, -10, 31.4, c['blush'], 0.45, 0.6)
        a.dots(-14, 30, ['n'], {'n': c['skinS']})  # 鼻（点）
        if girl:
            a.part([('p', [(6, 9.6), (9.6, 8), (10.4, 9.8), (6.8, 11.4)])], c['ribbon1'], c['ribbon2'], lw=0.4)
        if not girl:
            a.part([('p', [(-2, 7.4), (0, 3.6), (2.4, 7.2)]), ('p', [(9, 9), (14.6, 8.6), (12.4, 13)])], c['hair1'], c['hair2'], line=c['hairLine'], lw=0.6)
        return
    # 正面
    if girl:
        a.part([('p', [(-15.8, 16), (-11.4, 16), (-11.2, 36), (-15.2, 38)]), ('p', [(15.8, 16), (11.4, 16), (11.2, 36), (15.2, 38)])], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
    hm = a.part([('e', -15.2, 7 if girl else 6.4, 15.2, 33)], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
    if not girl:
        a.part([('p', [(-11, 10), (-13, 6.4), (-6, 8)]), ('p', [(-2, 7.4), (0, 3.6), (2.4, 7.2)]), ('p', [(8, 9), (13, 6.6), (12, 12)])], c['hair1'], c['hair2'], line=c['hairLine'], lw=0.6)
    fm = a.part([('e', -10.4, 15.6, 10.4, 33.6)], c['skin1'], c['skin2'], shade=c['skinS'], sh=(1.2, 1.4), sb=1.0, line=c['skinLine'], lw=0.6)
    tips = [(-12.4, -8.2, 25), (-8.8, -4.6, 24.6), (-4.6, -1.8, 22.2), (-1.6, 1.6, 20.6), (1.8, 4.6, 22.2), (4.6, 8.8, 24.6), (8.2, 12.4, 25)]  # 毛先は目の上端まで。真ん中だけ短く額が見える
    bm = bangs(a, c, -12.4, 12.4, tips, base=18, face=fm)
    for s in (-1, 1):  # 顔の横の髪：目の外側の端から あごの近くまで顔を縁取る
        pts = [(s * 15.4, 16), (s * 9.6, 18), (s * 9.6, 29), (s * 11.2, 33.4), (s * 15, 28)] if girl else \
              [(s * 14.8, 16), (s * 9.6, 18), (s * 9.6, 28.6), (s * 10.8, 32.6), (s * 12.4, 30.6), (s * 14.2, 22)]  # 男子は細く短め
        a.part([('p', pts)], c['hair1'], c['hair2'], line=c['hairLine'], lw=0.6)
    a.clip(hm, [('e', -11, 8.4, 1, 11.6)], c['hairL'], 0.45, blur=0.6) if not isinstance(a, Pixel) else a.stroke([(-10, 10), (-6, 8), (-1, 8)], c['hairL'])
    eye(a, c, -6, flip=False)   # 左目 x -8..-4、右目 4..8（目の間7ドット）
    eye(a, c, 6, flip=True)
    if girl:
        a.blob(-8.6, 29.8, -4.8, 31.4, c['blush'], 0.45, 0.6)
        a.blob(4.8, 29.8, 8.6, 31.4, c['blush'], 0.45, 0.6)
    a.dots(0, 30, ['n'], {'n': c['skinS']})  # 鼻（点）。口は省く
    if girl:
        a.part([('p', [(6.4, 9), (10, 7.4), (10.8, 9.2), (7.2, 10.8)])], c['ribbon1'], c['ribbon2'], lw=0.4)


Art = Pixel  # 塗り方：Pixel（くっきりしたドット絵）／Chibi（イラストを縮めた柔らかい塗り）


def frame(ch, d, step):
    c = colors(ch)
    side = 'left' if d in ('left', 'right') else d
    a = Art()
    body(a, c, side, step, side == 'up')
    up = Art()
    head(up, c, side)
    im = a.im
    bob = 0 if step == 1 else (1 if Art is Pixel else round(0.6 * SS))
    im.alpha_composite(up.im, (0, bob))
    a.im = im
    out = a.shrink()
    return out.transpose(Image.FLIP_LEFT_RIGHT) if d == 'right' else out


if __name__ == '__main__':
    for name, ch in CHARS.items():
        sheet = Image.new('RGBA', (FW * 3, FH * 4), (0, 0, 0, 0))
        for r, d in enumerate(['down', 'left', 'right', 'up']):
            for s in range(3):
                sheet.paste(frame(ch, d, s), (s * FW, r * FH))
        out = ROOT / 'img' / 'chars' / f'{name}.png'
        sheet.save(out)
        print(out.relative_to(ROOT))
