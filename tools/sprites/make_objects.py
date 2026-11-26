"""自作の家具・小物を描いて img/tiles/objects.png に書き出す（1マス48px、8列×6段）。
参考画像は寸法と描き込みの細かさだけ合わせ、デザインは自分で考えたもの（参考画像は写さない・リポジトリに入れない）。
描き方：濃い輪郭（1ドット）、3段の明暗（光・地・影）、角の光、ガラスの反射、ボタンなどの細部。光は左上から。

使い方：python3 -I tools/sprites/make_objects.py
置き場所（列, 段, 幅, 高さ）は OBJECTS の表のとおり。地図では { tile: ['objects', 列, 段, 幅, 高さ], x, y }。
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
T = 48
im = Image.new('RGBA', (T * 8, T * 6), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
OUT = (34, 30, 36)


def sh(c, k):
    return tuple(max(0, min(255, round(v * k))) for v in c[:3])


def box(x0, y0, x1, y1, c, line=OUT, light=1.18, dark=0.72):
    """輪郭つきの箱：上と左に光、下と右に影"""
    d.rectangle((x0, y0, x1, y1), fill=c, outline=line)
    d.line((x0 + 1, y0 + 1, x1 - 1, y0 + 1), fill=sh(c, light))
    d.line((x0 + 1, y0 + 1, x0 + 1, y1 - 1), fill=sh(c, light * 0.96))
    d.line((x0 + 1, y1 - 1, x1 - 1, y1 - 1), fill=sh(c, dark))
    d.line((x1 - 1, y0 + 1, x1 - 1, y1 - 1), fill=sh(c, dark * 1.05))


def glass(x0, y0, x1, y1, c=(150, 200, 226)):
    """ガラス：上が明るく下が暗い、斜めの反射2本"""
    d.rectangle((x0, y0, x1, y1), fill=c, outline=OUT)
    h = y1 - y0
    for i in range(1, h):
        k = 1.12 - 0.35 * i / h
        d.line((x0 + 1, y0 + i, x1 - 1, y0 + i), fill=sh(c, k))
    for o in (3, 7):
        d.line((x0 + o, y1 - 2, min(x1 - 1, x0 + o + (y1 - y0) // 2), y0 + 2), fill=(236, 246, 252))


def cell(c, r):
    return c * T, r * T


# ---------------- 大物（1×2マス）
def vending(c, r, body, accent):
    x, y = cell(c, r)
    box(x + 4, y + 6, x + 43, y + 93, body)                          # 本体
    d.rectangle((x + 4, y + 6, x + 43, y + 13), fill=accent, outline=OUT)   # 上の看板
    d.line((x + 8, y + 9, x + 30, y + 9), fill=sh(accent, 1.4))
    glass(x + 8, y + 16, x + 31, y + 58)                             # 商品の窓
    for row in range(3):                                             # 並んだ缶
        yy = y + 20 + row * 13
        for k in range(4):
            col = [(220, 60, 60), (60, 140, 220), (240, 200, 60), (90, 190, 110)][(k + row) % 4]
            d.rectangle((x + 10 + k * 5, yy, x + 13 + k * 5, yy + 7), fill=col, outline=sh(col, 0.6))
            d.point((x + 11 + k * 5, yy + 1), fill=(255, 255, 255))
        d.line((x + 9, yy + 9, x + 30, yy + 9), fill=(200, 200, 210))     # 段の棚
    for k in range(4):                                               # 選ぶボタン
        d.rectangle((x + 34, y + 18 + k * 6, x + 39, y + 21 + k * 6), fill=(240, 240, 230), outline=OUT)
        d.point((x + 35, y + 19 + k * 6), fill=(255, 120, 80))
    d.rectangle((x + 34, y + 46, x + 39, y + 56), fill=(40, 40, 46), outline=OUT)   # お金の口
    d.line((x + 36, y + 48, x + 36, y + 53), fill=(150, 150, 160))
    box(x + 8, y + 66, x + 39, y + 80, sh(body, 0.8))                # 取り出し口
    d.rectangle((x + 11, y + 70, x + 36, y + 77), fill=(30, 30, 36))
    d.rectangle((x + 6, y + 88, x + 41, y + 93), fill=sh(body, 0.55), outline=OUT)  # 台座


def showcase(c, r):   # 冷蔵ショーケース（ガラス扉、棚に飲み物）
    x, y = cell(c, r)
    box(x + 4, y + 4, x + 43, y + 93, (186, 190, 198))
    d.rectangle((x + 6, y + 6, x + 41, y + 11), fill=(70, 150, 210), outline=OUT)
    glass(x + 7, y + 14, x + 40, y + 82, (176, 214, 232))
    for k in range(4):
        yy = y + 22 + k * 15
        d.line((x + 8, yy + 8, x + 39, yy + 8), fill=(230, 236, 240))
        for j in range(5):
            col = [(240, 240, 240), (230, 120, 60), (120, 200, 120), (250, 220, 90), (200, 80, 110)][(j + k) % 5]
            d.rectangle((x + 10 + j * 6, yy, x + 13 + j * 6, yy + 7), fill=col, outline=sh(col, 0.6))
    d.line((x + 37, y + 40, x + 37, y + 56), fill=(90, 90, 100), width=2)   # 取っ手
    d.rectangle((x + 6, y + 86, x + 41, y + 93), fill=(90, 92, 100), outline=OUT)


def locker(c, r):     # スチールロッカー（2つの扉、通気口、名札）
    x, y = cell(c, r)
    body = (128, 150, 170)
    box(x + 3, y + 4, x + 44, y + 93, body)
    for k in range(2):
        xx = x + 5 + k * 19
        box(xx, y + 7, xx + 17, y + 90, sh(body, 1.04))
        for v in range(4):
            d.line((xx + 4, y + 12 + v * 3, xx + 13, y + 12 + v * 3), fill=sh(body, 0.6))
        d.rectangle((xx + 4, y + 28, xx + 13, y + 32), fill=(236, 236, 226), outline=OUT)   # 名札
        d.rectangle((xx + 13, y + 48, xx + 15, y + 56), fill=(70, 74, 84))                  # 取っ手
        d.point((xx + 13, y + 49), fill=(220, 224, 230))


def drawers_tall(c, r):   # 木の引き出し棚（4段、金色のつまみ）
    x, y = cell(c, r)
    wood = (150, 100, 60)
    box(x + 4, y + 10, x + 43, y + 93, wood)
    d.rectangle((x + 3, y + 8, x + 44, y + 13), fill=sh(wood, 1.15), outline=OUT)   # 天板
    for k in range(4):
        yy = y + 16 + k * 19
        box(x + 7, yy, x + 40, yy + 16, sh(wood, 1.06))
        d.line((x + 9, yy + 5, x + 30, yy + 5), fill=sh(wood, 0.92))      # 木目
        d.rectangle((x + 21, yy + 7, x + 26, yy + 9), fill=(214, 176, 70), outline=(110, 80, 30))


def file_cabinet(c, r):   # 金属の書類棚（3段、ラベル）
    x, y = cell(c, r)
    body = (170, 172, 176)
    box(x + 6, y + 20, x + 41, y + 93, body)
    for k in range(3):
        yy = y + 23 + k * 23
        box(x + 9, yy, x + 38, yy + 20, sh(body, 1.05))
        d.rectangle((x + 16, yy + 4, x + 31, yy + 8), fill=(244, 244, 236), outline=OUT)
        d.rectangle((x + 19, yy + 12, x + 28, yy + 14), fill=(90, 92, 98))


# ---------------- 2×1マス
def long_desk(c, r):  # 木の長机（脚つき）
    x, y = cell(c, r)
    wood = (176, 124, 76)
    d.rectangle((x + 6, y + 30, x + 9, y + 46), fill=sh(wood, 0.6), outline=OUT)
    d.rectangle((x + 86, y + 30, x + 89, y + 46), fill=sh(wood, 0.6), outline=OUT)
    box(x + 2, y + 10, x + 93, y + 31, wood)
    for yy in (16, 22, 27):
        d.line((x + 6, y + yy, x + 88, y + yy), fill=sh(wood, 0.92))
    d.rectangle((x + 2, y + 31, x + 93, y + 35), fill=sh(wood, 0.7), outline=OUT)   # 天板の厚み


def sofa(c, r):       # 二人がけのソファ
    x, y = cell(c, r)
    col = (96, 122, 150)
    box(x + 4, y + 8, x + 91, y + 24, sh(col, 0.92))                 # 背もたれ
    box(x + 2, y + 18, x + 12, y + 44, col)                          # ひじかけ
    box(x + 83, y + 18, x + 93, y + 44, col)
    box(x + 12, y + 24, x + 47, y + 40, sh(col, 1.08))               # 座面2つ
    box(x + 48, y + 24, x + 83, y + 40, sh(col, 1.08))
    d.rectangle((x + 12, y + 40, x + 83, y + 44), fill=sh(col, 0.6), outline=OUT)


# ---------------- 1×1マス
def chair(c, r, view):
    x, y = cell(c, r)
    wood, seat = (168, 114, 66), (190, 70, 64)
    if view == 'front':
        d.rectangle((x + 15, y + 34, x + 17, y + 44), fill=sh(wood, 0.6), outline=OUT)
        d.rectangle((x + 30, y + 34, x + 32, y + 44), fill=sh(wood, 0.6), outline=OUT)
        box(x + 14, y + 8, x + 33, y + 26, wood)                     # 背もたれ
        d.rectangle((x + 18, y + 12, x + 29, y + 20), fill=sh(wood, 0.85))
        box(x + 12, y + 26, x + 35, y + 35, seat)                    # 座面
    elif view == 'back':
        d.rectangle((x + 15, y + 30, x + 17, y + 44), fill=sh(wood, 0.6), outline=OUT)
        d.rectangle((x + 30, y + 30, x + 32, y + 44), fill=sh(wood, 0.6), outline=OUT)
        box(x + 12, y + 22, x + 35, y + 30, seat)
        box(x + 14, y + 12, x + 33, y + 34, wood)                    # 背もたれの裏
        for k in range(3):
            d.line((x + 17, y + 17 + k * 5, x + 30, y + 17 + k * 5), fill=sh(wood, 0.85))
    else:  # 横向き（左向き）
        d.rectangle((x + 15, y + 32, x + 17, y + 44), fill=sh(wood, 0.6), outline=OUT)
        d.rectangle((x + 29, y + 32, x + 31, y + 44), fill=sh(wood, 0.6), outline=OUT)
        box(x + 28, y + 8, x + 33, y + 34, wood)                     # 背もたれ（横から）
        box(x + 13, y + 26, x + 33, y + 33, seat)


def pipe_chair(c, r):  # パイプ椅子
    x, y = cell(c, r)
    metal, seat = (170, 176, 184), (60, 70, 90)
    for xx in (14, 31):
        d.line((x + xx, y + 10, x + xx, y + 44), fill=OUT, width=3)
        d.line((x + xx, y + 10, x + xx, y + 44), fill=metal, width=1)
    box(x + 13, y + 9, x + 34, y + 21, seat)
    box(x + 12, y + 27, x + 35, y + 34, seat)
    d.line((x + 14, y + 44, x + 33, y + 44), fill=OUT)


def round_table(c, r):  # 白いクロスの丸テーブル
    x, y = cell(c, r)
    d.rectangle((x + 21, y + 30, x + 26, y + 44), fill=(110, 90, 70), outline=OUT)
    d.ellipse((x + 4, y + 8, x + 43, y + 36), fill=(236, 232, 226), outline=OUT)
    d.ellipse((x + 6, y + 10, x + 41, y + 28), fill=(250, 248, 244))
    d.arc((x + 6, y + 10, x + 41, y + 34), 20, 160, fill=(196, 190, 184))
    d.point((x + 14, y + 14), fill=(255, 255, 255))


def low_drawers(c, r):  # 金属の引き出し（キャスターつき、3段）
    x, y = cell(c, r)
    body = (150, 156, 164)
    box(x + 10, y + 8, x + 37, y + 42, body)
    for k in range(3):
        yy = y + 11 + k * 10
        box(x + 12, yy, x + 35, yy + 8, sh(body, 1.06))
        d.line((x + 20, yy + 4, x + 27, yy + 4), fill=(70, 72, 80))
    for xx in (13, 33):
        d.ellipse((x + xx - 2, y + 42, x + xx + 2, y + 46), fill=(40, 40, 44))


def trash(c, r):       # ごみ箱（金属の網目）
    x, y = cell(c, r)
    body = (110, 120, 130)
    d.polygon([(x + 14, y + 18), (x + 33, y + 18), (x + 31, y + 44), (x + 16, y + 44)], fill=body, outline=OUT)
    for k in range(4):
        d.line((x + 17 + k * 4, y + 20, x + 18 + k * 3, y + 42), fill=sh(body, 0.75))
    d.ellipse((x + 13, y + 14, x + 34, y + 22), fill=(60, 64, 70), outline=OUT)
    d.arc((x + 14, y + 15, x + 33, y + 21), 180, 300, fill=(190, 196, 204))
    d.polygon([(x + 20, y + 15), (x + 25, y + 11), (x + 28, y + 16)], fill=(240, 240, 232), outline=OUT)   # 紙くず


def clock(c, r):       # 掛け時計（壁につける）
    x, y = cell(c, r)
    d.ellipse((x + 10, y + 10, x + 37, y + 37), fill=(70, 74, 84), outline=OUT)
    d.ellipse((x + 13, y + 13, x + 34, y + 34), fill=(248, 248, 244))
    for k, (dx, dy) in enumerate(((0, -9), (9, 0), (0, 9), (-9, 0))):
        d.point((x + 23 + dx, y + 23 + dy), fill=OUT)
    d.line((x + 23, y + 23, x + 23, y + 16), fill=OUT, width=1)
    d.line((x + 23, y + 23, x + 28, y + 25), fill=OUT, width=1)
    d.point((x + 17, y + 16), fill=(255, 255, 255))


def board(c, r, cork):   # 掲示板（コルク）／ホワイトボード（2×1、壁につける）
    x, y = cell(c, r)
    frame = (140, 96, 56) if cork else (180, 184, 190)
    box(x + 4, y + 6, x + 91, y + 40, frame)
    if cork:
        d.rectangle((x + 8, y + 10, x + 87, y + 36), fill=(196, 150, 96))
        for i, (xx, yy, col) in enumerate(((12, 12, (250, 250, 240)), (34, 14, (250, 230, 120)), (56, 11, (200, 230, 250)), (72, 18, (250, 250, 240)), (22, 24, (250, 200, 210)))):
            d.rectangle((x + xx, y + yy, x + xx + 12, y + yy + 13), fill=col, outline=sh(col, 0.6))
            d.line((x + xx + 2, y + yy + 4, x + xx + 9, y + yy + 4), fill=(140, 140, 150))
            d.line((x + xx + 2, y + yy + 7, x + xx + 8, y + yy + 7), fill=(140, 140, 150))
            d.point((x + xx + 6, y + yy + 1), fill=(220, 50, 50))     # 画びょう
    else:
        d.rectangle((x + 8, y + 10, x + 87, y + 34), fill=(244, 248, 250))
        d.line((x + 12, y + 16, x + 40, y + 14), fill=(60, 90, 200))
        d.line((x + 12, y + 21, x + 34, y + 21), fill=(60, 90, 200))
        d.line((x + 50, y + 18, x + 66, y + 26, x + 80, y + 15), fill=(210, 60, 60))
        d.line((x + 10, y + 12, x + 30, y + 12), fill=(255, 255, 255))
        d.rectangle((x + 30, y + 36, x + 64, y + 39), fill=(150, 154, 160), outline=OUT)   # ペン置き
        d.rectangle((x + 36, y + 35, x + 42, y + 36), fill=(40, 60, 180))


def cardboard(c, r):   # 段ボール箱
    x, y = cell(c, r)
    col = (196, 156, 100)
    box(x + 8, y + 18, x + 39, y + 44, col)
    d.polygon([(x + 8, y + 18), (x + 14, y + 10), (x + 45, y + 10), (x + 39, y + 18)], fill=sh(col, 1.15), outline=OUT)
    d.line((x + 23, y + 10, x + 23, y + 30), fill=(150, 120, 80))   # ガムテープ
    d.rectangle((x + 21, y + 18, x + 26, y + 30), fill=(210, 180, 130))


def extinguisher(c, r):  # 消火器
    x, y = cell(c, r)
    red = (206, 44, 40)
    d.rounded_rectangle((x + 17, y + 14, x + 30, y + 44), radius=5, fill=red, outline=OUT)
    d.line((x + 19, y + 17, x + 19, y + 40), fill=sh(red, 1.3))
    d.rectangle((x + 20, y + 24, x + 27, y + 32), fill=(250, 250, 240), outline=OUT)
    d.rectangle((x + 21, y + 8, x + 26, y + 14), fill=(50, 50, 56), outline=OUT)
    d.line((x + 26, y + 10, x + 33, y + 14, x + 33, y + 24), fill=OUT, width=2)


# ---------------- 2×2マス
def meeting_table(c, r):  # 会議机（大きな天板、4本脚）
    x, y = cell(c, r)
    wood = (120, 84, 56)
    for xx in (6, 86):
        d.rectangle((x + xx, y + 66, x + xx + 4, y + 92), fill=sh(wood, 0.6), outline=OUT)
    box(x + 2, y + 10, x + 93, y + 68, wood)
    for yy in range(18, 64, 8):
        d.line((x + 6, y + yy, x + 88, y + yy), fill=sh(wood, 0.92))
    d.rectangle((x + 2, y + 68, x + 93, y + 73), fill=sh(wood, 0.65), outline=OUT)
    d.rectangle((x + 20, y + 24, x + 34, y + 42), fill=(250, 250, 244), outline=OUT)   # 資料
    d.rectangle((x + 60, y + 30, x + 68, y + 38), fill=(240, 240, 236), outline=OUT)   # 湯のみ
    d.line((x + 61, y + 32, x + 66, y + 32), fill=(150, 200, 160))


def wide_shelf(c, r):     # 横長の本棚（2段×2マス）
    x, y = cell(c, r)
    wood = (124, 84, 50)
    box(x + 2, y + 6, x + 93, y + 93, wood)
    rnd = __import__('random').Random(7)
    for k in range(3):
        yy = y + 10 + k * 27
        d.rectangle((x + 6, yy, x + 89, yy + 22), fill=sh(wood, 0.5))
        xx = x + 7
        while xx < x + 86:
            w = rnd.randint(3, 6)
            h = rnd.randint(15, 21)
            col = rnd.choice(((180, 60, 60), (60, 100, 170), (70, 140, 90), (220, 190, 90), (230, 230, 220), (120, 80, 150)))
            d.rectangle((xx, yy + 22 - h, xx + w - 1, yy + 21), fill=col, outline=sh(col, 0.55))
            d.line((xx + 1, yy + 24 - h, xx + 1, yy + 19), fill=sh(col, 1.25))
            xx += w
        d.rectangle((x + 4, yy + 22, x + 91, yy + 24), fill=sh(wood, 1.1), outline=OUT)


# ---------------- 配置（列, 段, 幅, 高さ, 名前）
OBJECTS = [
    (0, 0, 1, 2, '自販機（赤）', lambda: vending(0, 0, (200, 56, 52), (240, 220, 210))),
    (1, 0, 1, 2, '自販機（青）', lambda: vending(1, 0, (52, 100, 180), (240, 240, 250))),
    (2, 0, 1, 2, '冷蔵ショーケース', lambda: showcase(2, 0)),
    (3, 0, 1, 2, 'ロッカー', lambda: locker(3, 0)),
    (4, 0, 1, 2, '木の引き出し棚', lambda: drawers_tall(4, 0)),
    (5, 0, 1, 2, '金属の書類棚', lambda: file_cabinet(5, 0)),
    (6, 0, 2, 1, '長机', lambda: long_desk(6, 0)),
    (6, 1, 2, 1, 'ソファ', lambda: sofa(6, 1)),
    (0, 2, 1, 1, '木の椅子（正面）', lambda: chair(0, 2, 'front')),
    (1, 2, 1, 1, '木の椅子（後ろ）', lambda: chair(1, 2, 'back')),
    (2, 2, 1, 1, '木の椅子（横）', lambda: chair(2, 2, 'side')),
    (3, 2, 1, 1, 'パイプ椅子', lambda: pipe_chair(3, 2)),
    (4, 2, 1, 1, '丸テーブル', lambda: round_table(4, 2)),
    (5, 2, 1, 1, '金属の引き出し', lambda: low_drawers(5, 2)),
    (6, 2, 1, 1, 'ごみ箱', lambda: trash(6, 2)),
    (7, 2, 1, 1, '掛け時計', lambda: clock(7, 2)),
    (0, 3, 2, 1, '掲示板', lambda: board(0, 3, True)),
    (2, 3, 2, 1, 'ホワイトボード', lambda: board(2, 3, False)),
    (4, 3, 1, 1, '段ボール箱', lambda: cardboard(4, 3)),
    (5, 3, 1, 1, '消火器', lambda: extinguisher(5, 3)),
    (0, 4, 2, 2, '会議机', lambda: meeting_table(0, 4)),
    (2, 4, 2, 2, '横長の本棚', lambda: wide_shelf(2, 4)),
]

if __name__ == '__main__':
    for *_, fn in OBJECTS:
        fn()
    out = ROOT / 'img' / 'tiles' / 'objects.png'
    im.save(out)
    print(out.relative_to(ROOT))
