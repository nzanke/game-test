"""自作の家具・小物を描いて img/tiles/objects.png に書き出す（1マス48px、8列×8段）。
参考画像は寸法と描き込みの細かさだけ合わせ、デザインは自分で考えたもの（参考画像は写さない・リポジトリに入れない）。

大学の教室・研究棟にある家具として、スチール（塗装した鋼板と、銀色のパイプ）を前提に描く。
描き方：
- 濃い輪郭1ドット。光は左上から。
- 鋼板の面は、左上が明るく右下が暗い段階的なグラデーション（なめらかにせず段で塗る）に、
  左寄りの縦の照り返しの帯を重ねる。縁は上と左に光の線、下と右に影の線、左上の角にいちばん明るい点。
- 凹んだ部分（取っ手のくぼみ・扉の継ぎ目・通気口）は、上と左が暗く下と右が明るい。
- パイプは断面の明暗（暗い縁・光の筋・地・影）で丸みを出す。円筒（ごみ箱・消火器）も同じ考え方。
- 床に落ちる影は半透明の暗い色。
寸法の目安：1ドット≒3.5〜4cm。机の天板は床から約19ドット（約70cm）、椅子の座面は約12ドット（約42cm）、
長机は1人1マス（3人掛けで3マス）、背の高い家具は1×2マス。

使い方：python3 -I tools/sprites/make_objects.py
置き場所（列, 段, 幅, 高さ）は OBJECTS の表のとおり。地図では { tile: ['objects', 列, 段, 幅, 高さ], x, y }。
"""
import random
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
T = 48
im = Image.new('RGBA', (T * 8, T * 8), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
px = im.load()
OUT = (30, 30, 38)
SHADOW = (16, 16, 28, 78)

IVORY = (206, 206, 198)     # 事務用の塗装鋼板（明るい灰色）
GRAY = (150, 158, 168)      # 灰色の鋼板
SILVER = (176, 182, 192)    # 銀色のパイプ
TOP = (226, 226, 220)       # 机の天板（白っぽいメラミン）


def sh(c, k):
    return tuple(max(0, min(255, round(v * k))) for v in c[:3])


def put(x, y, c):
    px[x, y] = tuple(c[:3]) + (255,)


def gfill(x0, y0, x1, y1, c, kx=(1.08, 0.86), ky=(1.04, 0.92), spec=(0.24, 0.2, 0.12), step=0.05):
    """段のついたグラデーションで塗る（kx 左→右、ky 上→下、spec＝照り返しの帯（位置, 幅, 強さ））"""
    for y in range(y0, y1 + 1):
        ty = (y - y0) / max(1, y1 - y0)
        for x in range(x0, x1 + 1):
            tx = (x - x0) / max(1, x1 - x0)
            k = (kx[0] + (kx[1] - kx[0]) * tx) * (ky[0] + (ky[1] - ky[0]) * ty)
            if spec:
                cx, w, a = spec
                k *= 1 + a * max(0.0, 1 - abs(tx - cx) / w)
            put(x, y, sh(c, round(k / step) * step))


def panel(x0, y0, x1, y1, c, line=OUT, **kw):
    """鋼板の面：輪郭、グラデーション、縁の光と影、角の光"""
    d.rectangle((x0, y0, x1, y1), outline=line)
    gfill(x0 + 1, y0 + 1, x1 - 1, y1 - 1, c, **kw)
    d.line((x0 + 1, y0 + 1, x1 - 1, y0 + 1), fill=sh(c, 1.26))
    d.line((x0 + 1, y0 + 2, x0 + 1, y1 - 1), fill=sh(c, 1.14))
    d.line((x0 + 2, y1 - 1, x1 - 1, y1 - 1), fill=sh(c, 0.66))
    d.line((x1 - 1, y0 + 2, x1 - 1, y1 - 2), fill=sh(c, 0.76))
    put(x0 + 1, y0 + 1, sh(c, 1.42))


def inset(x0, y0, x1, y1, c):
    """凹み：上と左が暗く、下と右が明るい"""
    gfill(x0, y0, x1, y1, sh(c, 0.82), kx=(0.92, 1.02), ky=(0.94, 1.04), spec=None)
    d.line((x0, y0, x1, y0), fill=sh(c, 0.52))
    d.line((x0, y0, x0, y1), fill=sh(c, 0.6))
    d.line((x0 + 1, y1, x1, y1), fill=sh(c, 1.24))
    d.line((x1, y0 + 1, x1, y1), fill=sh(c, 1.12))


PROFILE = {1: [1.2], 2: [1.32, 0.8], 3: [1.02, 1.38, 0.76], 4: [0.96, 1.42, 1.02, 0.7], 5: [0.9, 1.3, 1.46, 1.0, 0.66]}


def tube_v(x, y0, y1, w, c=SILVER):
    """縦のパイプ（x から幅 w、y0〜y1。下の端は輪郭で閉じる）"""
    d.rectangle((x - 1, y0, x + w, y1), fill=OUT)
    for i, k in enumerate(PROFILE[w]):
        for y in range(y0, y1):
            t = (y - y0) / max(1, y1 - y0)
            put(x + i, y, sh(c, k * (1.02 - 0.12 * t)))


def tube_h(x0, x1, y, h, c=SILVER):
    """横のパイプ（y から高さ h、x0〜x1。両端は輪郭で閉じる）"""
    d.rectangle((x0, y - 1, x1, y + h), fill=OUT)
    for i, k in enumerate(PROFILE[h]):
        for x in range(x0 + 1, x1):
            put(x, y + i, sh(c, k))


def cyl_k(t):
    """円筒の明暗：左の縁は暗め、左寄りに光、右へ暗く"""
    pts = [(0, 0.78), (0.12, 1.08), (0.26, 1.4), (0.38, 1.12), (0.6, 0.96), (0.85, 0.74), (1, 0.6)]
    for (a, ka), (b, kb) in zip(pts, pts[1:]):
        if t <= b:
            return ka + (kb - ka) * (t - a) / (b - a)
    return 0.6


def cylinder(x0, y0, x1, y1, c, step=0.06):
    for x in range(x0, x1 + 1):
        k = round(cyl_k((x - x0) / max(1, x1 - x0)) / step) * step
        for y in range(y0, y1 + 1):
            put(x, y, sh(c, k * (1.02 - 0.08 * (y - y0) / max(1, y1 - y0))))


def shadow(x0, y0, x1, y1):
    d.ellipse((x0, y0, x1, y1), fill=SHADOW)


def cell(c, r):
    return c * T, r * T


def screw(x, y):
    put(x, y, (232, 234, 238))
    put(x + 1, y, (120, 124, 132))


# ---------------- 背の高い家具（1×2マス）
def vending(c, r, body, accent):     # 自販機：塗装鋼板の本体、ステンレスの縁、ガラスの窓
    x, y = cell(c, r)
    shadow(x + 3, y + 89, x + 45, y + 95)
    panel(x + 4, y + 5, x + 43, y + 92, body, spec=(0.18, 0.16, 0.16))
    panel(x + 5, y + 6, x + 42, y + 13, accent, spec=(0.3, 0.3, 0.1))   # 上の看板
    for k in range(5):
        d.line((x + 10 + k * 5, y + 9, x + 12 + k * 5, y + 9), fill=sh(body, 1.1))
    d.rectangle((x + 7, y + 15, x + 32, y + 59), fill=(170, 176, 186), outline=OUT)   # ステンレスの窓枠
    d.line((x + 8, y + 16, x + 31, y + 16), fill=(236, 240, 246))
    d.line((x + 8, y + 16, x + 8, y + 58), fill=(222, 226, 232))
    gfill(x + 9, y + 17, x + 30, y + 57, (60, 70, 86), kx=(1.2, 0.9), ky=(1.25, 0.8), spec=None)   # 窓の奥
    for row in range(3):
        yy = y + 20 + row * 13
        for k in range(4):
            col = [(214, 58, 58), (58, 130, 214), (236, 196, 60), (80, 180, 104)][(k + row) % 4]
            cx = x + 10 + k * 5
            cylinder(cx, yy, cx + 3, yy + 7, col)
            d.rectangle((cx, yy, cx + 3, yy + 7), outline=sh(col, 0.5))
            d.line((cx + 1, yy, cx + 2, yy), fill=(214, 218, 224))               # 缶の口（銀）
            d.rectangle((cx, yy + 9, cx + 3, yy + 10), fill=(230, 90, 70) if (k + row) % 2 else (70, 170, 230))   # 値段の光
        d.line((x + 9, yy + 8, x + 30, yy + 8), fill=(196, 200, 208))
    for o in (3, 9):                                                        # ガラスの反射
        d.line((x + 9 + o, y + 55, x + 9 + o + 18, y + 19), fill=(224, 236, 246))
        d.line((x + 10 + o, y + 55, x + 10 + o + 18, y + 19), fill=(150, 170, 190))
    for k in range(4):                                                      # 押しボタン
        yy = y + 17 + k * 6
        d.rectangle((x + 34, yy, x + 40, yy + 4), fill=OUT)
        gfill(x + 35, yy + 1, x + 39, yy + 3, (236, 236, 228), spec=None)
        put(x + 35, yy + 1, (255, 255, 255))
        put(x + 39, yy + 3, (240, 110, 70))
    inset(x + 34, y + 43, x + 40, y + 56, (60, 62, 70))                      # お金の口
    d.line((x + 37, y + 46, x + 37, y + 52), fill=(20, 20, 26))
    put(x + 36, y + 46, (210, 214, 220))
    panel(x + 7, y + 63, x + 40, y + 82, sh(body, 0.86), spec=None)          # 取り出し口
    inset(x + 10, y + 67, x + 37, y + 79, (54, 56, 64))
    d.line((x + 11, y + 70, x + 36, y + 70), fill=(110, 114, 124))           # ふたの光
    panel(x + 5, y + 86, x + 42, y + 92, (120, 124, 132), spec=None)         # 台座
    d.line((x + 43, y + 8, x + 43, y + 90), fill=sh(body, 0.45))             # 右の側面の影


def showcase(c, r):     # 冷蔵ショーケース：ステンレスの枠、ガラス扉
    x, y = cell(c, r)
    shadow(x + 3, y + 89, x + 45, y + 95)
    panel(x + 4, y + 4, x + 43, y + 92, SILVER, spec=(0.2, 0.16, 0.2))
    panel(x + 6, y + 6, x + 41, y + 12, (70, 140, 204), spec=(0.3, 0.3, 0.1))
    d.rectangle((x + 7, y + 14, x + 40, y + 82), fill=(150, 156, 166), outline=OUT)
    gfill(x + 8, y + 15, x + 39, y + 81, (190, 214, 228), kx=(1.08, 0.9), ky=(1.1, 0.86), spec=None)
    for k in range(4):
        yy = y + 20 + k * 15
        for j in range(5):
            col = [(236, 236, 236), (226, 120, 60), (116, 196, 116), (246, 216, 90), (196, 80, 110)][(j + k) % 5]
            cx = x + 10 + j * 6
            cylinder(cx, yy + 2, cx + 3, yy + 10, col)
            d.rectangle((cx, yy + 2, cx + 3, yy + 10), outline=sh(col, 0.55))
            d.rectangle((cx + 1, yy, cx + 2, yy + 1), fill=sh(col, 0.7))       # ペットボトルのふた
        d.line((x + 8, yy + 11, x + 39, yy + 11), fill=(236, 240, 244))
        d.line((x + 8, yy + 12, x + 39, yy + 12), fill=(130, 140, 150))
    for o in (2, 8):
        d.line((x + 8 + o, y + 80, x + 8 + o + 26, y + 18), fill=(236, 244, 250))
    tube_v(x + 37, y + 38, y + 58, 2, (210, 214, 222))                       # 取っ手
    panel(x + 6, y + 85, x + 41, y + 92, (96, 100, 110), spec=None)
    for k in range(6):                                                       # 下の通気口
        d.line((x + 10 + k * 5, y + 88, x + 12 + k * 5, y + 88), fill=(40, 40, 48))


def locker(c, r):       # スチールロッカー（2人用）：通気口、名札入れ、取っ手と鍵、蝶番
    x, y = cell(c, r)
    body = (140, 158, 176)
    shadow(x + 2, y + 89, x + 46, y + 95)
    panel(x + 3, y + 4, x + 44, y + 92, sh(body, 0.9), spec=None)
    d.rectangle((x + 3, y + 4, x + 44, y + 8), fill=OUT)                     # 天板の厚み
    gfill(x + 4, y + 5, x + 43, y + 7, sh(body, 1.12), spec=None)
    for k in range(2):
        xx = x + 5 + k * 19
        panel(xx, y + 10, xx + 18, y + 87, body, spec=(0.25, 0.22, 0.16))
        for v in range(5):                                                   # 通気口（凹み）
            yy = y + 15 + v * 3
            d.line((xx + 4, yy, xx + 14, yy), fill=sh(body, 0.45))
            d.line((xx + 4, yy + 1, xx + 14, yy + 1), fill=sh(body, 1.3))
        d.rectangle((xx + 4, y + 32, xx + 14, y + 37), fill=(110, 116, 126))   # 名札入れ（金属の枠）
        d.rectangle((xx + 5, y + 33, xx + 13, y + 36), fill=(246, 246, 238))
        d.line((xx + 6, y + 34, xx + 11, y + 34), fill=(150, 150, 160))
        tube_v(xx + 14, y + 48, y + 60, 2, (206, 210, 218))                    # 取っ手
        d.rectangle((xx + 13, y + 62, xx + 16, y + 65), fill=OUT)              # 鍵
        put(xx + 14, y + 63, (226, 196, 90))
        put(xx + 15, y + 64, (150, 120, 50))
        for hy in (16, 78):                                                  # 蝶番
            d.rectangle((xx + 1, y + hy, xx + 2, y + hy + 4), fill=sh(body, 0.55))
            put(xx + 1, y + hy, sh(body, 1.3))
        for yy in (y + 68, y + 72):                                          # 下の通気口
            d.line((xx + 4, yy, xx + 14, yy), fill=sh(body, 0.45))
            d.line((xx + 4, yy + 1, xx + 14, yy + 1), fill=sh(body, 1.3))
    d.rectangle((x + 4, y + 88, x + 43, y + 91), fill=sh(body, 0.5))           # 台輪


def cabinet(c, r):      # スチール書庫：上はガラスの引き違い戸（中にファイル）、下は両開きの鋼板の扉
    x, y = cell(c, r)
    shadow(x + 2, y + 89, x + 46, y + 95)
    panel(x + 3, y + 6, x + 44, y + 92, IVORY, spec=(0.2, 0.18, 0.12))
    d.rectangle((x + 2, y + 4, x + 45, y + 8), fill=OUT)                      # 天板
    gfill(x + 3, y + 5, x + 44, y + 7, sh(IVORY, 1.12), spec=None)
    rnd = random.Random(3)
    for k in range(2):                                                       # ガラス戸（2段の棚）
        yy = y + 11 + k * 19
        d.rectangle((x + 6, yy, x + 41, yy + 17), fill=OUT)
        gfill(x + 7, yy + 1, x + 40, yy + 16, (70, 76, 88), spec=None, kx=(1.2, 0.8))
        xx = x + 8
        while xx < x + 39:                                                   # ファイルの背表紙
            w = rnd.choice((3, 3, 4))
            col = rnd.choice(((60, 96, 170), (196, 60, 60), (230, 230, 222), (70, 140, 96), (236, 196, 70)))
            gfill(xx, yy + 3, min(x + 39, xx + w - 1), yy + 16, col, kx=(1.25, 0.8), spec=None)
            d.rectangle((xx + 1, yy + 6, min(x + 39, xx + w - 2), yy + 7), fill=(246, 246, 240))   # ラベル
            xx += w
        d.line((x + 23, yy + 1, x + 23, yy + 16), fill=(150, 156, 166))       # 戸の重なり
        for o in (3, 26):
            d.line((x + 7 + o, yy + 15, x + 7 + o + 6, yy + 1), fill=(200, 216, 230))
    d.rectangle((x + 4, y + 48, x + 43, y + 49), fill=sh(IVORY, 0.6))         # 中段
    for k in range(2):
        xx = x + 6 + k * 18
        panel(xx, y + 51, xx + 17, y + 87, IVORY, spec=(0.3, 0.3, 0.14))
        hx = xx + (14 if k == 0 else 2)
        inset(hx, y + 62, hx + 1, y + 72, (90, 94, 102))                     # 取っ手のくぼみ
        put(hx, y + 73, (240, 242, 246))
    d.rectangle((x + 20, y + 75, x + 26, y + 79), fill=(226, 226, 218), outline=OUT)   # 鍵穴の座
    put(x + 23, y + 77, OUT)


def file_cabinet(c, r):   # 4段の書類棚：ラベル入れ、引き手のくぼみ
    x, y = cell(c, r)
    shadow(x + 4, y + 89, x + 44, y + 95)
    panel(x + 5, y + 10, x + 42, y + 92, IVORY, spec=None)
    d.rectangle((x + 4, y + 8, x + 43, y + 12), fill=OUT)
    gfill(x + 5, y + 9, x + 42, y + 11, sh(IVORY, 1.12), spec=None)
    for k in range(4):
        yy = y + 14 + k * 19
        panel(x + 7, yy, x + 40, yy + 17, IVORY, spec=(0.22, 0.2, 0.14))
        d.rectangle((x + 17, yy + 3, x + 30, yy + 7), fill=(120, 126, 136))   # ラベル入れ
        d.rectangle((x + 18, yy + 4, x + 29, yy + 6), fill=(248, 248, 240))
        d.line((x + 19, yy + 5, x + 25, yy + 5), fill=(160, 160, 170))
        inset(x + 15, yy + 10, x + 32, yy + 13, (110, 114, 122))             # 引き手
        d.line((x + 16, yy + 10, x + 31, yy + 10), fill=(36, 36, 44))
        put(x + 31, yy + 13, (250, 250, 252))
    d.rectangle((x + 6, y + 89, x + 41, y + 91), fill=sh(IVORY, 0.5))


def bookshelf(c, r):    # スチールのオープン書棚（4段、本とファイル）
    x, y = cell(c, r)
    shadow(x + 2, y + 89, x + 46, y + 95)
    panel(x + 3, y + 6, x + 44, y + 92, GRAY, spec=(0.15, 0.15, 0.1))
    rnd = random.Random(11)
    for k in range(4):
        yy = y + 9 + k * 20
        gfill(x + 6, yy, x + 41, yy + 16, (60, 64, 74), kx=(0.8, 1.1), ky=(0.7, 1.05), spec=None)   # 棚の奥（上が暗い）
        xx = x + 7
        while xx < x + 40:
            w = rnd.choice((2, 3, 3, 4))
            h = rnd.randint(10, 15)
            col = rnd.choice(((170, 60, 60), (60, 96, 160), (70, 130, 90), (210, 180, 90), (226, 222, 210), (110, 80, 140), (60, 60, 70)))
            x1 = min(x + 40, xx + w - 1)
            if rnd.random() < 0.12 and xx < x + 36:                          # 横に寝かせた本
                gfill(xx, yy + 13, xx + 6, yy + 16, col, kx=(1.2, 0.85), spec=None)
                xx += 7
                continue
            gfill(xx, yy + 17 - h, x1, yy + 16, col, kx=(1.25, 0.78), spec=None)
            put(xx, yy + 17 - h, sh(col, 1.4))
            if h > 12:
                d.line((xx, yy + 20 - h, x1, yy + 20 - h), fill=sh(col, 1.35))   # 背の帯
            xx += w
        d.rectangle((x + 5, yy + 17, x + 42, yy + 19), fill=OUT)             # 棚板（鋼板の縁）
        d.line((x + 6, yy + 18, x + 41, yy + 18), fill=sh(GRAY, 1.3))
        put(x + 6, yy + 18, (240, 242, 246))


# ---------------- 机と椅子
def long_desk(c, r, n):   # 大学の長机（n人掛け＝nマス）：白い天板、スチールの脚と幕板、物置の棚
    x, y = cell(c, r)
    W = T * n
    shadow(x + 3, y + 38, x + W - 4, y + 47)
    gfill(x + 8, y + 27, x + W - 9, y + 36, (86, 90, 100), kx=(0.95, 0.85), ky=(0.8, 1.0), spec=None)   # 奥の幕板（陰）
    d.rectangle((x + 7, y + 26, x + W - 8, y + 37), outline=OUT)
    for k in range(1, n):                                                    # 幕板の継ぎ目
        d.line((x + k * T, y + 28, x + k * T, y + 36), fill=(60, 62, 72))
    d.rectangle((x + 6, y + 27, x + W - 7, y + 29), fill=OUT)                # 物置の棚（鋼板）
    d.line((x + 7, y + 28, x + W - 8, y + 28), fill=sh(GRAY, 1.15))
    for lx in (x + 4, x + W - 8):                                            # 脚（角パイプ）と床の足
        tube_v(lx, y + 26, y + 45, 4, SILVER)
        tube_h(lx - 2, lx + 5, y + 43, 2, SILVER)
    d.rectangle((x + 2, y + 8, x + W - 3, y + 26), fill=OUT)                 # 天板
    gfill(x + 3, y + 9, x + W - 4, y + 23, TOP, kx=(1.06, 0.92), ky=(1.04, 0.9), spec=(0.16, 0.1 / n, 0.06))
    d.line((x + 3, y + 9, x + W - 4, y + 9), fill=sh(TOP, 1.14))
    d.line((x + 3, y + 9, x + 3, y + 23), fill=sh(TOP, 1.1))
    for k in range(n):                                                       # 天板の照り（席ごとに斜めの光）
        sx = x + 10 + k * T
        d.line((sx, y + 20, sx + 9, y + 11), fill=sh(TOP, 1.05))
    gfill(x + 3, y + 24, x + W - 4, y + 25, (120, 126, 136), kx=(1.15, 0.85), spec=None)   # 天板の縁（樹脂のエッジ）
    d.line((x + 3, y + 24, x + W - 4, y + 24), fill=(196, 200, 208))


def lectern(c, r):     # 教卓（2マス）：天板、正面の鋼板、マイク
    x, y = cell(c, r)
    W = T * 2
    shadow(x + 2, y + 40, x + W - 3, y + 47)
    panel(x + 4, y + 18, x + W - 5, y + 45, IVORY, spec=(0.18, 0.14, 0.12))  # 正面
    panel(x + 10, y + 23, x + W - 11, y + 41, sh(IVORY, 0.96), spec=(0.3, 0.16, 0.1))   # 正面の化粧板
    inset(x + 10, y + 23, x + W - 11, y + 23, IVORY)
    d.rectangle((x + 40, y + 29, x + 55, y + 34), fill=(110, 116, 126))      # 名札（大学名などは入れない）
    d.rectangle((x + 41, y + 30, x + 54, y + 33), fill=(240, 240, 232))
    d.rectangle((x + 5, y + 43, x + W - 6, y + 45), fill=(80, 84, 94))       # 幅木
    d.rectangle((x + 1, y + 6, x + W - 2, y + 19), fill=OUT)                 # 天板
    gfill(x + 2, y + 7, x + W - 3, y + 16, TOP, kx=(1.06, 0.92), spec=(0.14, 0.06, 0.06))
    d.line((x + 2, y + 7, x + W - 3, y + 7), fill=sh(TOP, 1.14))
    gfill(x + 2, y + 17, x + W - 3, y + 18, (120, 126, 136), kx=(1.15, 0.85), spec=None)
    d.line((x + 2, y + 17, x + W - 3, y + 17), fill=(196, 200, 208))
    d.rectangle((x + 60, y + 9, x + 79, y + 14), fill=OUT)                   # 操作盤
    gfill(x + 61, y + 10, x + 78, y + 13, (70, 74, 84), spec=None)
    for k in range(4):
        put(x + 63 + k * 4, y + 11, (120, 220, 140) if k == 0 else (210, 214, 220))
    d.line((x + 26, y + 13, x + 26, y + 6), fill=OUT, width=2)               # マイク
    d.line((x + 26, y + 6, x + 31, y + 2), fill=OUT, width=2)
    d.rectangle((x + 22, y + 12, x + 30, y + 15), fill=OUT)
    gfill(x + 23, y + 13, x + 29, y + 14, (60, 62, 70), spec=None)
    d.ellipse((x + 30, y + 0, x + 34, y + 4), fill=(50, 52, 60), outline=OUT)
    put(x + 31, y + 1, (190, 196, 206))
    for sx in (x + 8, x + 70):                                               # 天板の照り
        d.line((sx, y + 15, sx + 7, y + 8), fill=sh(TOP, 1.05))


SEAT = (78, 94, 120)      # 椅子の座面・背もたれ（紺の樹脂）


def chair(c, r, view):    # スタッキングチェア：銀色のパイプの脚、紺の樹脂の座面と背もたれ
    x, y = cell(c, r)
    shadow(x + 11, y + 40, x + 36, y + 47)
    if view == 'back':    # 後ろ向き（机に向かって座る側から見る）
        tube_v(x + 15, y + 30, y + 42, 2)                                    # 奥の脚（前脚）
        tube_v(x + 31, y + 30, y + 42, 2)
        d.rectangle((x + 12, y + 25, x + 35, y + 31), fill=OUT)              # 座面（背もたれの向こう）
        gfill(x + 13, y + 26, x + 34, y + 30, SEAT, spec=(0.3, 0.2, 0.12))
        tube_v(x + 13, y + 22, y + 45, 3)                                    # 手前の脚（後ろ脚）
        tube_v(x + 32, y + 22, y + 45, 3)
        d.rectangle((x + 12, y + 9, x + 35, y + 24), fill=OUT)               # 背もたれ（裏）
        gfill(x + 13, y + 10, x + 34, y + 23, sh(SEAT, 0.9), ky=(1.1, 0.84), spec=(0.26, 0.2, 0.16))
        d.line((x + 13, y + 10, x + 34, y + 10), fill=sh(SEAT, 1.3))
        d.rectangle((x + 19, y + 14, x + 28, y + 16), fill=OUT)              # 持ち手の穴
        d.line((x + 20, y + 17, x + 27, y + 17), fill=sh(SEAT, 1.2))
        for sx in (x + 15, x + 31):
            screw(sx, y + 20)
    elif view == 'front':
        tube_v(x + 14, y + 20, y + 41, 2)                                    # 奥の脚
        tube_v(x + 32, y + 20, y + 41, 2)
        d.rectangle((x + 13, y + 7, x + 34, y + 21), fill=OUT)               # 背もたれ
        gfill(x + 14, y + 8, x + 33, y + 20, SEAT, ky=(1.12, 0.82), spec=(0.26, 0.2, 0.16))
        d.line((x + 14, y + 8, x + 33, y + 8), fill=sh(SEAT, 1.35))
        d.rectangle((x + 11, y + 24, x + 36, y + 33), fill=OUT)              # 座面
        gfill(x + 12, y + 25, x + 35, y + 30, SEAT, ky=(1.16, 0.96), spec=(0.26, 0.2, 0.18))
        d.line((x + 12, y + 25, x + 35, y + 25), fill=sh(SEAT, 1.35))
        gfill(x + 12, y + 31, x + 35, y + 32, sh(SEAT, 0.62), spec=None)     # 座面の厚み
        tube_v(x + 12, y + 33, y + 45, 3)                                    # 手前の脚
        tube_v(x + 33, y + 33, y + 45, 3)
    else:                 # 横向き（左向き）
        tube_v(x + 15, y + 31, y + 45, 3)                                    # 前脚
        tube_v(x + 30, y + 22, y + 45, 3)                                    # 後ろ脚（背もたれを支える）
        tube_h(x + 15, x + 33, y + 39, 2)                                    # 横の補強
        d.rectangle((x + 12, y + 26, x + 34, y + 32), fill=OUT)              # 座面
        gfill(x + 13, y + 27, x + 33, y + 29, SEAT, ky=(1.2, 1.0), spec=(0.25, 0.2, 0.15))
        gfill(x + 13, y + 30, x + 33, y + 31, sh(SEAT, 0.62), spec=None)
        d.rectangle((x + 29, y + 7, x + 35, y + 26), fill=OUT)               # 背もたれ（横から、少し後ろへ反る）
        gfill(x + 30, y + 8, x + 34, y + 25, SEAT, kx=(1.25, 0.75), spec=None)


def pipe_chair(c, r):     # 折りたたみのパイプ椅子
    x, y = cell(c, r)
    shadow(x + 10, y + 40, x + 37, y + 47)
    tube_v(x + 16, y + 26, y + 42, 2)
    tube_v(x + 30, y + 26, y + 42, 2)
    tube_v(x + 13, y + 8, y + 45, 3)
    tube_v(x + 32, y + 8, y + 45, 3)
    panel(x + 12, y + 9, x + 35, y + 20, (66, 76, 96), spec=(0.25, 0.2, 0.18))   # 背もたれ
    panel(x + 11, y + 25, x + 36, y + 33, (66, 76, 96), spec=(0.25, 0.2, 0.18))  # 座面
    tube_h(x + 12, x + 35, y + 38, 2)                                        # 足をつなぐ棒


def round_table(c, r):    # 丸テーブル：白い天板、スチールの柱と十字の脚
    x, y = cell(c, r)
    shadow(x + 8, y + 38, x + 40, y + 47)
    tube_h(x + 10, x + 37, y + 42, 2)
    tube_v(x + 21, y + 26, y + 43, 5)
    d.ellipse((x + 4, y + 8, x + 43, y + 32), fill=OUT)
    d.ellipse((x + 5, y + 11, x + 42, y + 31), fill=(120, 126, 136))         # 縁の厚み
    d.ellipse((x + 5, y + 9, x + 42, y + 28), fill=TOP)
    d.ellipse((x + 8, y + 11, x + 32, y + 22), fill=sh(TOP, 1.08))
    d.line((x + 12, y + 18, x + 18, y + 13), fill=(255, 255, 255))


def low_drawers(c, r):    # スチールのワゴン（3段、キャスター）
    x, y = cell(c, r)
    shadow(x + 8, y + 40, x + 40, y + 47)
    panel(x + 10, y + 8, x + 37, y + 42, IVORY, spec=None)
    for k in range(3):
        yy = y + 11 + k * 10
        panel(x + 12, yy, x + 35, yy + 8, IVORY, spec=(0.22, 0.2, 0.14))
        inset(x + 18, yy + 5, x + 29, yy + 6, (110, 114, 122))
        put(x + 29, yy + 6, (250, 250, 252))
    for xx in (14, 33):
        d.rectangle((x + xx - 2, y + 42, x + xx + 2, y + 46), fill=OUT)
        put(x + xx - 1, y + 43, (120, 124, 132))


def trash(c, r):          # ステンレスのごみ箱（円筒、ふちの照り返し）
    x, y = cell(c, r)
    shadow(x + 11, y + 41, x + 37, y + 47)
    d.rectangle((x + 14, y + 19, x + 33, y + 44), fill=OUT)
    cylinder(x + 15, y + 20, x + 32, y + 43, (172, 178, 188))
    for yy in (y + 24, y + 39):                                              # 胴の帯
        for xx in range(x + 15, x + 33):
            put(xx, yy, sh((172, 178, 188), cyl_k((xx - x - 15) / 17) * 0.8))
    d.ellipse((x + 13, y + 14, x + 34, y + 23), fill=OUT)                    # 口
    d.ellipse((x + 14, y + 15, x + 33, y + 22), fill=(210, 214, 222))
    d.ellipse((x + 16, y + 16, x + 31, y + 21), fill=(40, 42, 50))
    d.arc((x + 14, y + 15, x + 33, y + 22), 150, 250, fill=(250, 252, 255))
    d.polygon([(x + 19, y + 18), (x + 24, y + 12), (x + 29, y + 18)], fill=(240, 240, 232), outline=OUT)   # 紙くず
    d.line((x + 22, y + 16, x + 26, y + 15), fill=(190, 190, 186))


def clock(c, r):          # 掛け時計（ステンレスの枠）
    x, y = cell(c, r)
    d.ellipse((x + 9, y + 9, x + 38, y + 38), fill=OUT)
    d.ellipse((x + 10, y + 10, x + 37, y + 37), fill=(150, 156, 166))
    d.arc((x + 10, y + 10, x + 37, y + 37), 160, 290, fill=(240, 244, 250), width=2)
    d.arc((x + 10, y + 10, x + 37, y + 37), 340, 100, fill=(96, 100, 110), width=2)
    d.ellipse((x + 13, y + 13, x + 34, y + 34), fill=OUT)
    d.ellipse((x + 14, y + 14, x + 33, y + 33), fill=(248, 248, 244))
    for dx, dy in ((0, -8), (8, 0), (0, 8), (-8, 0)):
        put(x + 23 + dx, y + 23 + dy, OUT)
    d.line((x + 23, y + 23, x + 23, y + 16), fill=OUT)
    d.line((x + 23, y + 23, x + 28, y + 25), fill=OUT)
    put(x + 23, y + 23, (200, 50, 50))
    d.line((x + 16, y + 18, x + 19, y + 15), fill=(255, 255, 255))


def board(c, r, cork):   # 掲示板（コルク）／ホワイトボード（2×1、壁につける。アルミの枠）
    x, y = cell(c, r)
    d.rectangle((x + 4, y + 6, x + 91, y + 40), fill=OUT)
    gfill(x + 5, y + 7, x + 90, y + 39, SILVER, kx=(1.1, 0.9), spec=None)
    d.line((x + 5, y + 7, x + 90, y + 7), fill=(240, 244, 250))
    d.line((x + 5, y + 39, x + 90, y + 39), fill=(110, 116, 126))
    if cork:
        gfill(x + 8, y + 10, x + 87, y + 36, (190, 146, 94), spec=None, kx=(1.05, 0.92))
        rnd = random.Random(5)
        for _ in range(120):
            put(x + rnd.randint(8, 87), y + rnd.randint(10, 36), rnd.choice(((150, 108, 66), (214, 172, 116))))
        for xx, yy, col in ((12, 12, (250, 250, 240)), (34, 14, (250, 230, 120)), (56, 11, (200, 230, 250)), (72, 18, (250, 250, 240)), (22, 24, (250, 200, 210))):
            d.rectangle((x + xx + 1, y + yy + 1, x + xx + 13, y + yy + 14), fill=(120, 86, 52))   # 紙の影
            d.rectangle((x + xx, y + yy, x + xx + 12, y + yy + 13), fill=col)
            d.line((x + xx + 2, y + yy + 4, x + xx + 9, y + yy + 4), fill=(140, 140, 150))
            d.line((x + xx + 2, y + yy + 7, x + xx + 8, y + yy + 7), fill=(140, 140, 150))
            put(x + xx + 6, y + yy + 1, (220, 50, 50))
            put(x + xx + 5, y + yy + 1, (255, 150, 150))
    else:
        gfill(x + 8, y + 10, x + 87, y + 34, (240, 244, 246), kx=(1.03, 0.95), spec=None)
        d.line((x + 12, y + 16, x + 40, y + 14), fill=(60, 90, 200))
        d.line((x + 12, y + 21, x + 34, y + 21), fill=(60, 90, 200))
        d.line((x + 50, y + 18, x + 66, y + 26, x + 80, y + 15), fill=(210, 60, 60))
        d.line((x + 52, y + 32, x + 84, y + 12), fill=(255, 255, 255))
        d.line((x + 58, y + 32, x + 87, y + 14), fill=(255, 255, 255))
        tube_h(x + 28, x + 66, y + 36, 3)                                    # ペン置き
        d.rectangle((x + 36, y + 35, x + 43, y + 36), fill=(40, 60, 180))
        d.rectangle((x + 46, y + 35, x + 52, y + 36), fill=(200, 50, 50))


def cardboard(c, r):     # 段ボール箱
    x, y = cell(c, r)
    col = (196, 156, 100)
    shadow(x + 6, y + 40, x + 42, y + 47)
    d.rectangle((x + 8, y + 18, x + 39, y + 44), fill=OUT)
    gfill(x + 9, y + 19, x + 38, y + 43, col, kx=(1.08, 0.88), spec=None)
    d.polygon([(x + 8, y + 18), (x + 14, y + 10), (x + 45, y + 10), (x + 39, y + 18)], fill=sh(col, 1.15), outline=OUT)
    d.polygon([(x + 39, y + 18), (x + 45, y + 10), (x + 45, y + 36), (x + 39, y + 44)], fill=sh(col, 0.72), outline=OUT)
    d.rectangle((x + 21, y + 18, x + 26, y + 30), fill=(214, 186, 136))
    d.line((x + 23, y + 11, x + 28, y + 11), fill=(214, 186, 136))


def extinguisher(c, r):  # 消火器（赤い円筒、黒いホース）
    x, y = cell(c, r)
    red = (206, 44, 40)
    shadow(x + 13, y + 41, x + 35, y + 47)
    d.rounded_rectangle((x + 16, y + 14, x + 31, y + 44), radius=5, fill=OUT)
    cylinder(x + 17, y + 17, x + 30, y + 43, red)
    d.rectangle((x + 19, y + 15, x + 28, y + 16), fill=sh(red, 0.9))
    d.rectangle((x + 19, y + 24, x + 28, y + 33), fill=OUT)
    gfill(x + 20, y + 25, x + 27, y + 32, (250, 250, 240), spec=None)
    d.line((x + 21, y + 27, x + 26, y + 27), fill=(200, 40, 40))
    d.line((x + 21, y + 30, x + 25, y + 30), fill=(120, 120, 130))
    d.rectangle((x + 20, y + 7, x + 27, y + 14), fill=OUT)                   # レバー
    gfill(x + 21, y + 8, x + 26, y + 13, (60, 62, 70), spec=None)
    d.line((x + 27, y + 10, x + 34, y + 14, x + 34, y + 26), fill=OUT, width=2)   # ホース


# ---------------- 2×1マス・2×2マス
def sofa(c, r):          # ロビーのソファ：布張り、スチールの脚
    x, y = cell(c, r)
    col = (86, 110, 140)
    shadow(x + 3, y + 40, x + 92, y + 47)
    for lx in (x + 8, x + 85):
        tube_v(lx, y + 42, y + 46, 2)
    panel(x + 4, y + 7, x + 91, y + 25, sh(col, 0.92), spec=(0.2, 0.1, 0.1))     # 背もたれ
    panel(x + 2, y + 17, x + 12, y + 43, col, spec=None)                     # ひじかけ
    panel(x + 83, y + 17, x + 93, y + 43, col, spec=None)
    for k in range(2):                                                       # 座面（ふくらみ）
        panel(x + 12 + k * 36, y + 24, x + 47 + k * 36, y + 39, sh(col, 1.06), spec=(0.3, 0.3, 0.12))
    d.rectangle((x + 12, y + 39, x + 83, y + 43), fill=OUT)
    gfill(x + 13, y + 40, x + 82, y + 42, sh(col, 0.6), spec=None)


def meeting_table(c, r):  # 会議机（2×2）：白い天板、スチールの脚
    x, y = cell(c, r)
    W = T * 2
    shadow(x + 3, y + 80, x + W - 4, y + 95)
    for lx in (x + 5, x + W - 9):
        tube_v(lx, y + 68, y + 93, 4)
    tube_h(x + 8, x + W - 9, y + 78, 2)                                      # 脚をつなぐ棒
    d.rectangle((x + 1, y + 8, x + W - 2, y + 71), fill=OUT)
    gfill(x + 2, y + 9, x + W - 3, y + 68, TOP, kx=(1.06, 0.9), ky=(1.04, 0.9), spec=(0.14, 0.06, 0.06))
    d.line((x + 2, y + 9, x + W - 3, y + 9), fill=sh(TOP, 1.14))
    gfill(x + 2, y + 69, x + W - 3, y + 70, (120, 126, 136), kx=(1.15, 0.85), spec=None)
    d.line((x + 2, y + 69, x + W - 3, y + 69), fill=(196, 200, 208))
    d.rectangle((x + 18, y + 22, x + 33, y + 41), fill=OUT)                  # 資料
    gfill(x + 19, y + 23, x + 32, y + 40, (250, 250, 246), spec=None)
    for k in range(5):
        d.line((x + 21, y + 26 + k * 3, x + 30 - (k % 2) * 3, y + 26 + k * 3), fill=(150, 150, 160))
    d.ellipse((x + 60, y + 28, x + 70, y + 36), fill=OUT)                    # 紙コップ
    d.ellipse((x + 61, y + 29, x + 69, y + 35), fill=(240, 240, 236))
    d.ellipse((x + 63, y + 30, x + 68, y + 34), fill=(120, 80, 50))
    d.line((x + 10, y + 60, x + 32, y + 14), fill=sh(TOP, 1.05))


def wide_shelf(c, r):     # スチールのオープン棚（2×2）：ファイルボックスと段ボール
    x, y = cell(c, r)
    W = T * 2
    shadow(x + 2, y + 88, x + W - 3, y + 95)
    for lx in (x + 3, x + W - 7):
        tube_v(lx, y + 6, y + 94, 4, GRAY)
    rnd = random.Random(7)
    for k in range(3):
        yy = y + 10 + k * 27
        gfill(x + 8, yy, x + W - 9, yy + 21, (64, 68, 78), kx=(0.85, 1.05), ky=(0.7, 1.05), spec=None)
        xx = x + 9
        while xx < x + W - 12:
            if rnd.random() < 0.25:                                          # ファイルボックス
                w = 9
                col = rnd.choice(((226, 226, 216), (90, 120, 170)))
                d.rectangle((xx, yy + 5, xx + w - 1, yy + 21), fill=OUT)
                gfill(xx + 1, yy + 6, xx + w - 2, yy + 20, col, kx=(1.2, 0.82), spec=None)
                d.rectangle((xx + 2, yy + 9, xx + w - 3, yy + 11), fill=(250, 250, 244))
                xx += w
            else:
                w = rnd.choice((3, 3, 4))
                h = rnd.randint(13, 20)
                col = rnd.choice(((170, 60, 60), (60, 96, 160), (70, 130, 90), (210, 180, 90), (226, 222, 210), (60, 60, 70)))
                gfill(xx, yy + 22 - h, xx + w - 1, yy + 21, col, kx=(1.25, 0.78), spec=None)
                put(xx, yy + 22 - h, sh(col, 1.4))
                xx += w
        d.rectangle((x + 2, yy + 22, x + W - 3, yy + 25), fill=OUT)          # 棚板
        gfill(x + 3, yy + 23, x + W - 4, yy + 24, GRAY, kx=(1.25, 0.85), spec=None)
        put(x + 3, yy + 23, (240, 242, 246))


def blackboard(c, r):     # 黒板（3×2、壁につける）：アルミの枠、緑の板、消し跡、チョーク受け
    """壁の中段（地図の y が壁の2段目）に置くと、板の下端が床から約20ドット（約75cm）、高さ約1.5mになる"""
    x, y = cell(c, r)
    W = T * 3
    d.rectangle((x + 2, y + 28, x + W - 3, y + 72), fill=OUT)
    gfill(x + 3, y + 29, x + W - 4, y + 71, SILVER, kx=(1.1, 0.88), spec=None)
    d.line((x + 3, y + 29, x + W - 4, y + 29), fill=(240, 244, 250))
    green = (52, 86, 70)
    gfill(x + 6, y + 32, x + W - 7, y + 68, green, kx=(1.06, 0.92), ky=(1.04, 0.94), spec=(0.3, 0.18, 0.06), step=0.03)
    d.line((x + 6, y + 32, x + W - 7, y + 32), fill=sh(green, 0.7))          # 枠の内側の影
    d.line((x + 6, y + 32, x + 6, y + 68), fill=sh(green, 0.76))
    rnd = random.Random(c * 7 + r)
    for _ in range(9):                                                       # 消し跡（横に流れた白いかすれ）
        sx, sy, ln = rnd.randint(10, W - 40), rnd.randint(36, 62), rnd.randint(14, 30)
        for k in range(ln):
            if rnd.random() < 0.7:
                put(x + sx + k, y + sy + rnd.choice((0, 0, 1)), sh(green, 1.16))
    for k in range(3):                                                       # うっすら残った字
        yy = y + 38 + k * 8
        xx = x + 14 + rnd.randint(0, 20)
        for j in range(rnd.randint(4, 8)):
            if rnd.random() < 0.8:
                d.line((xx + j * 6, yy, xx + j * 6 + 3, yy + rnd.choice((0, 2))), fill=sh(green, 1.3))
    d.rectangle((x + 1, y + 72, x + W - 2, y + 76), fill=OUT)                # チョーク受け
    gfill(x + 2, y + 73, x + W - 3, y + 75, SILVER, kx=(1.1, 0.88), ky=(1.2, 0.8), spec=None)
    for i, col in enumerate(((246, 246, 240), (240, 220, 90), (230, 110, 110))):
        d.rectangle((x + 20 + i * 7, y + 72, x + 24 + i * 7, y + 73), fill=col)
    d.rectangle((x + 100, y + 69, x + 112, y + 73), fill=OUT)                # 黒板消し
    gfill(x + 101, y + 70, x + 111, y + 71, (70, 80, 120), spec=None)
    d.line((x + 101, y + 72, x + 111, y + 72), fill=(220, 220, 214))


def plant(c, r):         # 観葉植物（1×1）：白い陶器の鉢、葉の茂み
    x, y = cell(c, r)
    shadow(x + 11, y + 41, x + 37, y + 47)
    leaf = (70, 140, 70)
    tube_v(x + 23, y + 24, y + 34, 2, (120, 90, 60))                          # 幹
    rnd = random.Random(4)
    blobs = [(24, 10, 9), (15, 16, 8), (33, 16, 8), (19, 24, 7), (30, 25, 7), (24, 18, 8)]
    for bx, by, rr in blobs:                                                 # 輪郭
        d.ellipse((x + bx - rr - 1, y + by - rr - 1, x + bx + rr + 1, y + by + rr), fill=OUT)
    for bx, by, rr in blobs:                                                 # 葉のかたまり（左上が明るい）
        for yy in range(by - rr, by + rr):
            for xx in range(bx - rr, bx + rr + 1):
                dx, dy = (xx - bx) / rr, (yy - by) / rr
                if dx * dx + dy * dy <= 1:
                    k = 1.15 - 0.35 * (dx + dy) / 2 - 0.1 * (dy > 0.4)
                    put(x + xx, y + yy, sh(leaf, round(k / 0.1) * 0.1))
    for _ in range(40):                                                      # 葉先の光と葉の間の影
        xx, yy = rnd.randint(9, 39), rnd.randint(2, 31)
        if px[x + xx, y + yy][3] and px[x + xx, y + yy][:3] != OUT:
            put(x + xx, y + yy, sh(leaf, rnd.choice((1.45, 0.62))))
    d.rectangle((x + 15, y + 31, x + 32, y + 45), fill=OUT)                  # 鉢
    cylinder(x + 16, y + 32, x + 31, y + 44, (232, 230, 224))
    d.rectangle((x + 14, y + 30, x + 33, y + 33), fill=OUT)                  # 鉢の縁
    cylinder(x + 15, y + 31, x + 32, y + 32, (244, 242, 238))
    d.line((x + 17, y + 33, x + 30, y + 33), fill=(70, 54, 40))              # 土


# ---------------- 配置（列, 段, 幅, 高さ, 名前）
OBJECTS = [
    (0, 0, 1, 2, '自販機（赤）', lambda: vending(0, 0, (196, 50, 48), (236, 222, 214))),
    (1, 0, 1, 2, '自販機（青）', lambda: vending(1, 0, (48, 96, 176), (236, 238, 246))),
    (2, 0, 1, 2, '冷蔵ショーケース', lambda: showcase(2, 0)),
    (3, 0, 1, 2, 'スチールロッカー', lambda: locker(3, 0)),
    (4, 0, 1, 2, 'スチール書庫', lambda: cabinet(4, 0)),
    (5, 0, 1, 2, '書類棚（4段）', lambda: file_cabinet(5, 0)),
    (6, 0, 1, 2, 'スチール書棚', lambda: bookshelf(6, 0)),
    (7, 0, 1, 1, '掛け時計', lambda: clock(7, 0)),
    (7, 1, 1, 1, 'ごみ箱', lambda: trash(7, 1)),
    (0, 2, 3, 1, '長机（3人掛け）', lambda: long_desk(0, 2, 3)),
    (3, 2, 2, 1, '長机（2人掛け）', lambda: long_desk(3, 2, 2)),
    (5, 2, 2, 1, '教卓', lambda: lectern(5, 2)),
    (7, 2, 1, 1, 'ワゴン', lambda: low_drawers(7, 2)),
    (0, 3, 1, 1, '椅子（後ろ）', lambda: chair(0, 3, 'back')),
    (1, 3, 1, 1, '椅子（正面）', lambda: chair(1, 3, 'front')),
    (2, 3, 1, 1, '椅子（横）', lambda: chair(2, 3, 'side')),
    (3, 3, 1, 1, 'パイプ椅子', lambda: pipe_chair(3, 3)),
    (4, 3, 1, 1, '丸テーブル', lambda: round_table(4, 3)),
    (5, 3, 1, 1, '段ボール箱', lambda: cardboard(5, 3)),
    (6, 3, 1, 1, '消火器', lambda: extinguisher(6, 3)),
    (0, 4, 2, 2, '会議机', lambda: meeting_table(0, 4)),
    (2, 4, 2, 2, 'スチールの棚', lambda: wide_shelf(2, 4)),
    (4, 4, 2, 1, '掲示板', lambda: board(4, 4, True)),
    (6, 4, 2, 1, 'ホワイトボード', lambda: board(6, 4, False)),
    (4, 5, 2, 1, 'ソファ', lambda: sofa(4, 5)),
    (0, 6, 3, 2, '黒板', lambda: blackboard(0, 6)),
    (3, 6, 1, 1, '観葉植物', lambda: plant(3, 6)),
]

if __name__ == '__main__':
    for *_, fn in OBJECTS:
        fn()
    out = ROOT / 'img' / 'tiles' / 'objects.png'
    im.save(out)
    print(out.relative_to(ROOT))
