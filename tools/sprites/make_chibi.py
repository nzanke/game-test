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
    'eyeW': '#ffffff', 'handO': '#97502c', 'earO': '#7a3c20', 'lash': '#1a0f1c', 'mouth': '#c85a5e', 'line': '#2a1e2a',
}
CHARS = {
    'yui_chibi': dict(BASE, girl=True, **{
        'hair1': '#343a62', 'hair2': '#16172a', 'hairL': '#55609a', 'hairLine': '#0e0f1c',
        'iris1': '#5a3aa0', 'iris2': '#8a5ad8', 'iris3': '#d8c2ff',
        'top1': '#f7ecd4', 'top2': '#cdb88f', 'topLine': '#4a3826', 'inner': '#ffffff', 'ribbon1': '#ee4a5e', 'ribbon2': '#9a1f34',
        'low1': '#8e93a6', 'low2': '#4f5366', 'leg': '#2a2730', 'shoe1': '#7a5a4c', 'shoe2': '#2e201c',
    }),
    'haru_chibi': dict(BASE, girl=False, **{
        'hair1': '#3c3f4c', 'hair2': '#16171d', 'hairL': '#626778', 'hairLine': '#0d0d12',
        'iris1': '#5a3a28', 'iris2': '#8a6040', 'iris3': '#c09a78',
        'top1': '#ffffff', 'top2': '#d6dbe6', 'topLine': '#363a4a', 'inner': '#f1c9b1', 'ribbon1': '#2a2420', 'ribbon2': '#2a2420',
        'low1': '#4d6290', 'low2': '#2e3c62', 'leg': '#2e3c62', 'shoe1': '#7a6a66', 'shoe2': '#463c40',
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
        # 横向き：胴は細く（9〜11ドット）、手は胴の中ほどより後ろ。前（左）がマイナス
        sw = {0: -1, 1: 0, 2: 1}[step]
        if girl:
            span_part(a, SKIRT_SIDE_GIRL, c['low1'], c['low2'], c['line'], bottom_line=True)
            for x, y0 in ((-5, 41), (-2, 41), (1, 42)):  # 折り目
                a.dots(x, y0, ['p'] * (44 - y0), {'p': c['low2']})
            span_part(a, TORSO_SIDE_GIRL, c['top1'], c['top2'], c['topLine'])
        else:
            span_part(a, PANTS_SIDE_BOY, c['low1'], c['low2'], c['line'], bottom_line=True)
            span_part(a, BELT_SIDE_BOY, c['ribbon1'], c['ribbon1'], c['line'])
            span_part(a, TORSO_SIDE_BOY, c['top1'], c['top2'], c['topLine'])
        a.stroke([(-3, 36), (2, 36)], (255, 253, 244))  # 肩の上の面
        # 腕（肩から手へ）と手
        a.part([('p', [(-0.4, 36.4), (3, 36.4), (3.4 + sw, 38.6), (0 + sw, 38.6)])], c['top1'], c['top2'], line=c['topLine'], lw=0.6)
        a.dots(sw, 38, ['.oKo.', 'oLMKo', 'oMMKo', 'oKdKE', '.EEE.'], {'o': c['handO'], 'd': c['handO'], 'E': c['line'], 'K': c['skinS'], 'L': c['skin2'], 'M': c['skin1']})
        if girl:
            a.part([('p', [(-5, 36.4), (-3, 36.4), (-4, 38.4)])], c['ribbon1'], c['ribbon2'], lw=0.4)
        feet(a, c, 'side', step)
        return
    # 正面。あごの下（35行）から なで肩で始まり、下へ広がる
    if girl:
        a.part([('p', [(-5.6, 38.4), (5.6, 38.4), (7.8, 43.6), (-7.8, 43.6)])], c['low1'], c['low2'], shade=c['low2'], line=c['line'], lw=0.7)
        for x, y0 in ((-2, 41), (2, 41), (-5, 42), (5, 42)):  # スカートの折り目：下半分に、地より濃い縦の線
            a.dots(x, y0, ['p'] * (44 - y0), {'p': c['low2']})
    else:  # ズボンは3段（41〜44行）、股の線
        a.part([('r', -5.6, 40.6, 5.6, 44.6)], c['low1'], c['low2'], shade=c['low2'], line=c['line'], lw=0.7)
        a.dots(0, 43, ['o', 'o'], {'o': c['line']})
    bottom = 39.4 if girl else 40.4
    m = a.part([('p', [(-7.6, 34.6), (7.6, 34.6), (10.6, 37.6), (10.6, 38.4), (5.6, bottom), (-5.6, bottom), (-10.6, 38.4), (-10.6, 37.6)])],
               c['top1'], c['top2'], shade=c['top2'], light=(255, 252, 240), line=c['topLine'], lw=0.7)
    for s in (-1, 1):
        a.stroke([(s * 6.4, 35), (s * 2.6, 35)], (255, 253, 244))  # 肩の上の面（あごのすぐ下に見える）
    if not back:
        if girl:
            a.clip(m, [('p', [(-1.4, 35), (1.4, 35), (1.4, 39.6), (-1.4, 39.6)])], c['inner'], 1.0)
            a.part([('p', [(-2.4, 35), (0, 36.4), (2.4, 35), (1.8, 37.8), (0, 37), (-1.8, 37.8)])], c['ribbon1'], c['ribbon2'], lw=0.4)
        else:
            a.clip(m, [('p', [(-1.8, 35), (1.8, 35), (0, 37.4)])], c['inner'], 1.0)
            a.clip(m, [('r', -0.2, 37.4, 0.2, 40.4)], c['topLine'], 0.7)
    if not girl:
        a.dots(-5, 41, ['bbbbbbbbbbb'], {'b': c['ribbon1']})  # ベルト（1段）
    hands(a, c)
    feet(a, c, 'front', step)


# 手：丸ではなくミトン形。外側の輪郭は茶色、内側と下は濃い線（腕と胴の境目にもなる）。
# 明るい肌は真ん中上寄りに2×2、下の段の内側は欠けていて、その上に親指の付け根の点
HAND = ['.oKLEE', 'oKMMKE', 'oLMMKE', 'oLLdKE', 'oKKEEE', '.EEE..']


def hands(a, c):
    pal = {'o': c['handO'], 'd': c['handO'], 'E': c['line'], 'K': c['skinS'], 'L': c['skin2'], 'M': c['skin1']}
    a.dots(-12, 38, HAND, pal)
    a.dots(7, 38, [r[::-1] for r in HAND], pal)


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
        if step == 1:  # 前後の足が並んで見える（奥の足を先に描く）
            a.dots(-1, 45, ['olllo', 'odddo', 'odddo'], pal)
            a.dots(-5, 45, foot, pal)
        else:
            a.dots(1, 44, ['olllo', 'odddo', 'odddo'], pal)  # 奥の足（上がっている）
            a.dots(-6, 45, foot, pal)


# ---------------- 頭（大きく、前髪は目のすぐ上まで、目は大きく下寄り） ----------------
# 左の目（外側が左）。E まつげ／g 影の白目／w 白目／i 濃い黒目／I 黒目／K 明るい黒目／P 瞳孔
EYE_GIRL = ['EEEE.', 'giEEE', 'wiPig', 'wIPIw', 'wKKKw']   # 女子は外側にまつげを1ドット足す
EYE_BOY = ['.EEE.', 'giEEE', 'wiPig', 'wIPIw', 'wKKKw']


# 横向きの目（x −9〜−4、24行から）：茶色の上まぶたの線、黒いまつげ、前の縁は黒、黒目は2ドット幅で上に瞳孔、
# 白目は白と灰色の2列、目尻は濃い影の肌、いちばん下の段は明るい黒目
EYE_SIDE = ['ooooo.',
            'oEEooo',
            '.IEgg4',
            '.EDwg4',
            '.EIwg4',
            '.LLw..']


def eye(a, c, cx, flip=False, side=False):
    if isinstance(a, Pixel):
        rows = EYE_GIRL if c['girl'] else EYE_BOY
        if side:  # 横向き：手本を1ドットずつ測った作り（EYE_SIDE）。女子は目尻の列が髪にかかるので描かない
            rows = [r[:-1] + '.' for r in EYE_SIDE] if c['girl'] else EYE_SIDE
            a.dots(-9, 24, rows, {'o': c['earO'], 'E': c['lash'], 'D': c['iris1'], 'I': c['iris2'], 'L': c['iris3'],
                                   'w': (255, 255, 255), 'g': (196, 190, 200), '4': c['handO']})
            return
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


def face_shade(a, c, m, hw_top=9):
    """顔の上下と左右の明暗を1ドットずつ塗る（立体感）。
    上から：前髪の下は中間色 → 目の下から頬（29〜31行）がいちばん明るい → 32〜33行は中間色 → あごの段は影色。
    左右の端は内側へ 濃い影→影→（頬の段はもう1段影）→中間色 と暗くなる"""
    tone = {1: c['skin1'], 2: c['skin2'], 3: c['skinS'], 4: c['handO']}
    px = m.load()
    for Y in range(FH):
        xs = [X for X in range(FW) if px[X, Y] > 127]
        if not xs:
            continue
        L, R = min(xs), max(xs)
        if Y <= 29:  # 目の高さまでは横の髪が顔の縁になる
            L, R = max(L, CX - hw_top), min(R, CX + hw_top)
        base = 2 if Y <= 27 else 1 if Y <= 31 else 2 if Y <= 33 else 3
        if Y == 28 and abs(xs[0] + xs[-1] - 2 * CX) <= 1:
            base = 2
        for X in xs:
            if X < L or X > R:
                continue
            d = min(X - L, R - X) + 1
            t = base
            if d == 1:
                t = max(t, 4 if Y >= 31 else 3)
            elif d == 2:
                t = max(t, 3)
            elif d == 3:
                t = max(t, 3 if Y in (30, 31) else 2)
            elif d == 4 and Y in (30, 31):
                t = max(t, 2)
            if Y == 28 and abs(X - CX) <= 1:
                t = max(t, 2)
            a.im.putpixel((X, Y), rgb_t(tone[t]))


# ---- 横向きは「行ごとの前端・後端の表」で形を決める（手本をドット単位で測った値をそのまま書ける）
# 横顔：(前端, 後端)。27〜28行が鼻筋（−12）、29〜31行で1ドット前に出て鼻（−13）、32行で輪郭1ドット分引っ込んで あごへ
FACE_SIDE = {**{y: (-9, -1) for y in range(16, 23)}, 23: (-10, 2), 24: (-10, 2), 25: (-11, 2), 26: (-11, 2),
             27: (-12, 2), 28: (-12, 2), 29: (-13, 3), 30: (-13, 3), 31: (-13, 3), 32: (-11, 3), 33: (-10, 3), 34: (-8, 2)}
FACE_SIDE_LINE = [(-12, 32), (-11, 33), (-10, 34), (-9, 34)] + [(x, 35) for x in range(-8, 4)]  # あごの下だけ濃い輪郭（前の縁は輪郭なし）
# 横向きの胴：上は細く、前の縁を斜めに下へ広げて、下半身の広さとの落差を出す
TORSO_SIDE_BOY = {36: (-4, 4), 37: (-5, 4), 38: (-5, 4), 39: (-6, 5), 40: (-6, 5)}
BELT_SIDE_BOY = {41: (-6, 5)}
PANTS_SIDE_BOY = {42: (-6, 4), 43: (-6, 4), 44: (-5, 4)}
TORSO_SIDE_GIRL = {36: (-5, 4), 37: (-6, 4), 38: (-6, 4), 39: (-7, 4)}
SKIRT_SIDE_GIRL = {40: (-7, 4), 41: (-7, 4), 42: (-8, 5), 43: (-8, 5), 44: (-8, 5)}


def span_mask(spans):
    m = Image.new('L', (FW, FH), 0)
    for Y, (f, b) in spans.items():
        for x in range(f, b + 1):
            m.putpixel((CX + x, Y), 255)
    return m


def span_part(a, spans, fill, shade, line, top_line=False, bottom_line=False):
    """表の形を塗る：両端は輪郭、後ろ側の1ドットは影、指定があれば上下の行も輪郭"""
    ys = sorted(spans)
    for Y in ys:
        f, b = spans[Y]
        for x in range(f, b + 1):
            col = fill
            if x in (f, b) or (bottom_line and Y == ys[-1]) or (top_line and Y == ys[0]):
                col = line
            elif x == b - 1:
                col = shade
            a.im.putpixel((CX + x, Y), rgb_t(col))
    return span_mask(spans)


def side_face_shade(a, c, m):
    """横顔の明暗：前の縁は濃い影、前寄りの頬（28〜31行）がいちばん明るく、耳に近い後ろほど暗い。あごの段は影色"""
    tone = {1: c['skin1'], 2: c['skin2'], 3: c['skinS'], 4: c['handO']}
    px = m.load()
    for Y in range(FH):
        xs = [X for X in range(FW) if px[X, Y] > 127]
        if not xs:
            continue
        L, R = min(xs), max(xs)
        for X in xs:
            df, db = X - L + 1, R - X + 1
            t = 2 if Y <= 27 else (1 if df <= 7 else 2) if Y <= 31 else 2 if Y <= 33 else 3
            if df == 1:
                t = max(t, 4 if Y >= 29 else 3)
            elif df == 2 and t == 1:
                t = 2
            if db == 1:
                t = max(t, 4)
            elif db <= 3:
                t = max(t, 3)
            elif db <= 5:
                t = max(t, 2)
            a.im.putpixel((X, Y), rgb_t(tone[t]))


def rgb_t(c):
    return tuple(c[:3]) + (255,)


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
        # 横向き：顔は頭の前・下寄り（x −12〜+1）、後ろに耳。いちばん前の前髪は額の前に垂れる
        if girl:  # 後ろ髪はあごの高さまで
            a.part([('p', [(1, 14), (15.6, 14), (15.4, 32.6), (10.4, 35.2), (3, 32)])], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
        hm = a.part([('e', -14.2, 7 if girl else 6.4, 14.6, 33)], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
        if isinstance(a, Pixel):
            fm = span_mask(FACE_SIDE)
            a.tint(fm, c['skin1'], 1.0)
            side_face_shade(a, c, fm)
            for x, y in FACE_SIDE_LINE:
                a.im.putpixel((CX + x, y), rgb_t(c['line']))
        else:
            fm = a.part([('e', -12.6, 16, 2.8, 34.6)], c['skin1'], c['skin2'], shade=c['skinS'], line=c['skinLine'], lw=0.6)
        bangs(a, c, -15.2, 3, [(-16, -12.4, 25.4), (-12.6, -9, 23.4), (-9.2, -5.6, 24.2), (-5.8, -2.4, 23), (-2.6, 1, 22.4)], base=18, face=fm)
        # 耳（顔の後ろ）
        if not isinstance(a, Pixel):
            a.part([('e', 1, 23.6, 4.6, 29.6)], c['skin2'], c['skin2'], shade=c['skinS'], line=c['skinLine'], lw=0.6)
        if isinstance(a, Pixel):
            a.stroke([(-6, 9), (-2, 7), (3, 7)], c['hairL'])
        else:
            a.clip(hm, [('e', -8, 8.4, 6, 11.6)], c['hairL'], 0.45, blur=0.6)
        if isinstance(a, Pixel):  # 鼻筋から下は、顔より前に髪の輪郭を残さない（鼻の出っ張りを見せる）
            line = set(FACE_SIDE_LINE)
            for Y in range(26, 36):
                f = -13 if Y == 26 else FACE_SIDE[Y][0] if Y in FACE_SIDE else 99  # 26行は前髪の毛先が −13 まで
                for x in range(-16, min(f, 4)):
                    if (x, Y) not in line:
                        a.im.putpixel((CX + x, Y), (0, 0, 0, 0))
        eye(a, c, -6, side=True)  # 目の前端は x −8（鼻筋から肌4ドット後ろ）
        if girl:
            a.blob(-11.6, 29.8, -8.4, 31.4, c['blush'], 0.45, 0.6)
        if girl:
            a.part([('p', [(6, 9.6), (9.6, 8), (10.4, 9.8), (6.8, 11.4)])], c['ribbon1'], c['ribbon2'], lw=0.4)
        if not girl:
            a.part([('p', [(-2, 7.4), (0, 3.6), (2.4, 7.2)]), ('p', [(9, 9), (14.6, 8.6), (12.4, 13)])], c['hair1'], c['hair2'], line=c['hairLine'], lw=0.6)
        return
    # 正面
    if girl:
        a.part([('p', [(-15.6, 16), (-11.4, 16), (-11.2, 35.6), (-13.6, 36.4)]), ('p', [(15.6, 16), (11.4, 16), (11.2, 35.6), (13.6, 36.4)])], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
    hm = a.part([('e', -15.2, 7 if girl else 6.4, 15.2, 33)], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
    if not girl:
        a.part([('p', [(-11, 10), (-13, 6.4), (-6, 8)]), ('p', [(-2, 7.4), (0, 3.6), (2.4, 7.2)]), ('p', [(8, 9), (13, 6.6), (12, 12)])], c['hair1'], c['hair2'], line=c['hairLine'], lw=0.6)
    fm = a.part([('e', -10.4, 15.6, 10.4, 33.6)], c['skin1'], c['skin2'], shade=c['skinS'], sh=(1.2, 1.4), sb=1.0, line=c['skinLine'], lw=0.6)
    if isinstance(a, Pixel):
        face_shade(a, c, fm)
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
    a.dots(0, 31, ['n'], {'n': c['skinS']})  # 鼻（点）。口は省く
    if girl:
        a.part([('p', [(6.4, 9), (10, 7.4), (10.8, 9.2), (7.2, 10.8)])], c['ribbon1'], c['ribbon2'], lw=0.4)


HAIR_TONES = ['#a3aee6', '#6873b0', '#454d84', '#30365e', '#1e2240']  # 女子の髪：光・明・中・暗・影


def hair_shade(im, c, side):
    """女子の髪を束ごとに塗り分ける（髪の色だけを塗り直す。輪郭や飾りはそのまま）。
    頭頂：つむじから放射状の束、境目は暗い線、頭の丸みに沿った天使の輪（束の真ん中だけいちばん明るい）。
    前髪：毛先の束ごと、上が明るく下ほど暗い、束の真ん中に光の筋。横・後ろの髪：縦の束、左が明るく右と下が暗い"""
    import math
    T = [rgb(h) for h in HAIR_TONES]
    src = {tuple(c[k][:3]) for k in ('hair1', 'hair2', 'hairL')}
    px = im.load()
    front = side == 'down'
    cx0 = -4 if side == 'left' else 0   # 横向きはつむじが後ろ寄り
    tips = [(-12.4, -8.2), (-8.8, -4.6), (-4.6, -1.8), (-1.6, 1.6), (1.8, 4.6), (4.6, 8.8), (8.2, 12.4)]
    bx = [(-12.4 + -8.2) / 2] + [(t0 + t1) / 2 for t0, t1 in tips[1:]]

    def strand(x, y):  # 頭頂の束の番号と、束の中の位置（0〜1）
        th = math.atan2(x - cx0, y + 3)
        v = th / 0.24 + 0.5
        return math.floor(v), v - math.floor(v)
    if side == 'up':
        strand = lambda x, y, _s=strand: (lambda th: (math.floor(th / 0.2 + 0.5), th / 0.2 + 0.5 - math.floor(th / 0.2 + 0.5)))(math.atan2(x, y - 2))

    for Y in range(FH):
        for X in range(FW):
            p = px[X, Y]
            if p[3] < 128 or tuple(p[:3]) not in src:
                continue
            x, y = X - CX + 0.5, Y + 0.5
            if front and y >= 18 and abs(x) < 9.6:   # 前髪
                k = sum(1 for b in (-8.5, -4.7, -1.7, 1.7, 4.7, 8.5) if x > b)
                edges = [-8.5, -4.7, -1.7, 1.7, 4.7, 8.5]
                left = max([b for b in edges if b < x], default=-12.4)
                right = min([b for b in edges if b > x], default=12.4)
                t = 2 if y < 21 else 3 if y < 23.5 else 4
                if abs(x - left) < 0.6 or abs(x - right) < 0.6:
                    t = 4  # 束の境目
                elif abs(x - (left + right) / 2) < 0.6 and 18.5 < y < 22:
                    t = 1 if k % 2 else 2 if y > 20.5 else 1  # 束の真ん中の光の筋
                    if k % 2 and y < 20:
                        t = 0
            elif y >= 16 and abs(x) >= 9.6 and side == 'down':   # 顔の横の髪・後ろ髪（縦の束）
                t = 2
                if (X - CX) % 3 == 0:
                    t = 3  # 縦の束の境目
                elif (X - CX) % 3 == 1 and y < 27:
                    t = 1  # 束の光
                if y > 30:
                    t = min(4, t + 1)
                if x > 0:
                    t = min(4, t + 1)  # 右側は陰
            else:   # 頭頂（後ろ向き・横向きは頭全体）。つむじから放射状の束と、ギザギザの天使の輪
                n, f = strand(x, y)
                band = (11.2 if side != 'up' else 13.5) + 0.018 * (x - cx0) ** 2 + [0, 1, 0.5, -0.5][n % 4]
                t = 2 if y < band + 2.5 else 3
                if y > band + 9:
                    t = 4 if f < 0.2 else 3
                if abs(y - band) < 1.1:
                    t = 1
                    if abs(y - band) < 0.6 and 0.25 < f < 0.75:
                        t = 0
                if f < 0.2 and y > band - 3:
                    t = 2 if abs(y - band) < 1.1 else max(t, 3)  # 束の境目（輪の中では1段だけ暗く）
                if x - cx0 < -6 and 2 <= t <= 3 and y < band + 6:
                    t -= 1  # 左上から光
                if x - cx0 > 8 and y > band + 1:
                    t = min(4, t + 1)
            px[X, Y] = T[t] + (255,)


# ---- 横向きの耳のまわり（手本を1ドットずつ測った作りを表にしたもの。左端の列 x、23行から）
# 1〜4 肌（明・中・影・濃い影）／# 濃い輪郭／o 耳の縁の茶色／H 髪（髪でなければ中間の髪色で塗る）／S 髪の影の色／_ 透明／. そのまま
EAR_SIDE_BOY = (-2, 23, [
    'SHH.#ooo....',
    'SHH.#434o...',
    'SHH#o312o...',
    'SHH#4312#...',
    'SH#43324#...',
    '##33334#S...',
    '33333##SS...',
    '223334SS....',
    '223334SS....',
    '233334SSS...',
    '333344SSS###',
    '33344##SSSS_',
    '#####__####_',
])
EAR_SIDE_GIRL = (-4, 23, [
    'SHHHHSHooo....',
    'SHHHH#o434o...',
    'SHHHH#o312o...',
    'SHHHH#4312#...',
    'SHHHS#3324#...',
    'SHHH#4334#S...',
    'SHHH#43##SS...',
    'SHHS#334SS....',
    'SHH#4334SS....',
    'SHS#4334SS....',
    'SH#44444SSSSS.',
])


def ear_side(im, c):
    girl = c['girl']
    x0, y0, rows = EAR_SIDE_GIRL if girl else EAR_SIDE_BOY
    if girl:
        hairs = {rgb(h) for h in HAIR_TONES}
        mid, dark = rgb(HAIR_TONES[2]), rgb(HAIR_TONES[4])
    else:
        hairs = {tuple(c[k][:3]) for k in ('hair1', 'hair2', 'hairL')}
        mid, dark = tuple(c['hair1'][:3]), tuple(c['hair2'][:3])
    pal = {'1': c['skin1'], '2': c['skin2'], '3': c['skinS'], '4': c['handO'], '#': c['line'], 'o': c['earO'], 'S': dark}
    px = im.load()
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            X, Y = CX + x0 + i, y0 + j
            if ch == '.':
                continue
            if ch == '_':
                px[X, Y] = (0, 0, 0, 0)
            elif ch == 'H':
                if px[X, Y][3] < 128 or tuple(px[X, Y][:3]) not in hairs:
                    px[X, Y] = mid + (255,)
            else:
                px[X, Y] = tuple(pal[ch][:3]) + (255,)


Art = Pixel  # 塗り方：Pixel（くっきりしたドット絵）／Chibi（イラストを縮めた柔らかい塗り）


def frame(ch, d, step):
    c = colors(ch)
    side = 'left' if d in ('left', 'right') else d
    a = Art()
    body(a, c, side, step, side == 'up')
    up = Art()
    head(up, c, side)
    if c['girl'] and Art is Pixel:
        hair_shade(up.im, c, side)
    if side == 'left' and Art is Pixel:
        ear_side(up.im, c)
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
