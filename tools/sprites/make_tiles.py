"""自作のタイルを描いて書き出す（1マス48px）。見本の絵は写さず、種類だけ参考にして描いたもの。

使い方：python3 -I tools/sprites/make_tiles.py
  img/tiles/own.png   … 0列：階段（上り）　1列：階段（下り）
  img/tiles/floor.png … 床タイル 8列×3段（並べても継ぎ目が出ないように描く。記号は system.js の legend の A〜P）
    1段目：市松 石 レンガ 大理石 赤じゅうたん 人工芝 体育館の床 コンクリート
    2段目：縞鋼板 グレーチング 点字ブロック（線） 点字ブロック（点） 濃い木の床 青じゅうたん 土 ゴムマット
    3段目：灰色のPタイル タイルカーペット ベージュのPタイル（記号 Q〜S）、教室の壁（上・中・下の3段で1枚。記号 U〜W）
"""
import random
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
T = 48


def stairs(d, x0, up):
    base = (196, 196, 188) if up else (150, 150, 146)
    edge = (110, 108, 104)
    light = (226, 226, 220)
    d.rectangle((x0, 0, x0 + T - 1, T - 1), fill=edge)
    n = 6
    for i in range(n):
        y = i * T // n
        k = (n - i) if up else (i + 1)  # 上りは奥ほど明るく、下りは奥ほど暗く
        c = tuple(min(255, int(v * (0.80 + 0.04 * k))) for v in base)
        d.rectangle((x0 + 2, y + 1, x0 + T - 3, y + T // n - 2), fill=c)
        d.line((x0 + 2, y + 1, x0 + T - 3, y + 1), fill=light)
    # 手すり
    d.rectangle((x0, 0, x0 + 2, T - 1), fill=(120, 90, 60))
    d.rectangle((x0 + T - 3, 0, x0 + T - 1, T - 1), fill=(120, 90, 60))


# ---------------- 床タイル
def shade(c, k):
    return tuple(max(0, min(255, round(v * k))) for v in c[:3]) + (255,)


def noise(im, amount, seed, step=1):
    """色を少しずつ明暗させて質感を出す（step ごとのかたまりで）"""
    rnd = random.Random(seed)
    px = im.load()
    for y in range(0, T, step):
        for x in range(0, T, step):
            k = 1 + rnd.uniform(-amount, amount)
            for yy in range(y, min(T, y + step)):
                for xx in range(x, min(T, x + step)):
                    px[xx, yy] = shade(px[xx, yy], k)


def tile(base):
    im = Image.new('RGBA', (T, T), base + (255,))
    return im, ImageDraw.Draw(im)


def checker():   # 白黒の市松（目地つき）
    im, d = tile((60, 60, 70))
    for i in range(2):
        for j in range(2):
            c = (236, 236, 240) if (i + j) % 2 == 0 else (64, 66, 82)
            d.rectangle((i * 24 + 1, j * 24 + 1, i * 24 + 22, j * 24 + 22), fill=c)
            d.line((i * 24 + 1, j * 24 + 1, i * 24 + 22, j * 24 + 1), fill=shade(c, 1.12))
    noise(im, 0.03, 1)
    return im


def stone():     # 灰色の石の床（大小の板石）
    im, d = tile((90, 92, 98))
    rnd = random.Random(2)
    for x0, y0, x1, y1 in ((0, 0, 23, 15), (24, 0, 47, 23), (0, 16, 23, 31), (24, 24, 47, 39), (0, 32, 23, 47), (24, 40, 47, 47)):
        c = tuple(150 + rnd.randint(-12, 12) for _ in range(3))
        d.rectangle((x0 + 1, y0 + 1, x1 - 1, y1 - 1), fill=c)
        d.line((x0 + 1, y0 + 1, x1 - 1, y0 + 1), fill=shade(c, 1.15))
        d.line((x0 + 1, y1 - 1, x1 - 1, y1 - 1), fill=shade(c, 0.82))
    noise(im, 0.06, 3, 2)
    return im


def brick():     # 赤レンガ（互い違い）
    im, d = tile((120, 96, 84))
    for row in range(4):
        y = row * 12
        off = 0 if row % 2 == 0 else 12
        for k in range(-1, 3):
            x = k * 24 + off
            c = (176, 86, 66) if (row + k) % 3 else (160, 74, 58)
            d.rectangle((x + 1, y + 1, x + 22, y + 10), fill=c)
            d.line((x + 1, y + 1, x + 22, y + 1), fill=shade(c, 1.15))
    noise(im, 0.06, 4, 2)
    return im


def marble():    # クリーム色の大理石風タイル（4枚、薄い筋）
    im, d = tile((196, 186, 168))
    for i in range(2):
        for j in range(2):
            d.rectangle((i * 24 + 1, j * 24 + 1, i * 24 + 22, j * 24 + 22), fill=(234, 226, 210))
    rnd = random.Random(5)
    for _ in range(6):
        x, y = rnd.randint(2, 45), rnd.randint(2, 45)
        for s in range(8):
            x2, y2 = x + rnd.choice((-1, 0, 1)), y + 1
            if 0 <= x2 < T and y2 < T and (x2 % 24) not in (0, 23) and (y2 % 24) not in (0, 23):
                d.point((x2, y2), fill=(210, 200, 182))
            x, y = x2, y2
    noise(im, 0.02, 6)
    return im


def carpet(c1, c2, seed):   # じゅうたん（細かい織り目）
    im, d = tile(c1)
    px = im.load()
    for y in range(T):
        for x in range(T):
            if (x + y) % 4 == 0 or (x - y) % 8 == 0:
                px[x, y] = c2 + (255,)
    noise(im, 0.05, seed)
    return im


def turf():      # 緑の人工芝
    im, d = tile((74, 150, 66))
    rnd = random.Random(8)
    px = im.load()
    for _ in range(420):
        x, y = rnd.randrange(T), rnd.randrange(T)
        px[x, y] = rnd.choice(((96, 178, 82, 255), (58, 124, 52, 255), (110, 190, 92, 255)))
    return im


def gym():       # 体育館の床（明るい細い板、ニスの光）
    im, d = tile((206, 158, 92))
    for i in range(4):
        x = i * 12
        c = (214, 166, 98) if i % 2 else (200, 150, 86)
        d.rectangle((x + 1, 0, x + 11, T - 1), fill=c)
        d.line((x, 0, x, T - 1), fill=(160, 114, 60))
        d.line((x + 2, 0, x + 2, T - 1), fill=shade(c, 1.1))
        yj = (i * 17) % T     # 板の継ぎ目
        d.line((x + 1, yj, x + 11, yj), fill=(170, 124, 70))
    noise(im, 0.03, 9)
    return im


def concrete():  # コンクリート（ざらつきと小さなひび）
    im, d = tile((150, 150, 148))
    noise(im, 0.07, 10)
    d.line((8, 30, 13, 27, 18, 29, 22, 25), fill=(108, 108, 106))
    d.line((34, 8, 37, 12, 36, 15), fill=(112, 112, 110))
    return im


def checkered_plate():   # 縞鋼板（金属の床、斜めの突起）
    im, d = tile((138, 144, 152))
    for y in range(0, T, 8):
        for x in range(0, T, 8):
            if (x // 8 + y // 8) % 2:
                d.line((x + 1, y + 5, x + 5, y + 1), fill=(186, 192, 200))
                d.line((x + 2, y + 6, x + 6, y + 2), fill=(96, 100, 108))
            else:
                d.line((x + 1, y + 1, x + 5, y + 5), fill=(186, 192, 200))
                d.line((x + 2, y + 2, x + 6, y + 6), fill=(96, 100, 108))
    noise(im, 0.03, 11)
    return im


def grating():   # グレーチング（側溝のふた）
    im, d = tile((40, 42, 46))
    for x in range(0, T, 6):
        d.rectangle((x, 0, x + 1, T - 1), fill=(150, 154, 160))
        d.line((x, 0, x, T - 1), fill=(186, 190, 196))
    for y in (0, 23, 24, 47):
        d.line((0, y, T - 1, y), fill=(120, 124, 130))
    return im


def tactile(dots):   # 点字ブロック（黄色）
    im, d = tile((232, 186, 40))
    d.rectangle((0, 0, T - 1, T - 1), outline=(196, 150, 24))
    if dots:
        for y in range(6, T, 12):
            for x in range(6, T, 12):
                d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(248, 210, 76), outline=(190, 146, 22))
    else:
        for x in (8, 20, 32, 44):
            d.rounded_rectangle((x - 3, 4, x + 2, T - 5), radius=2, fill=(248, 210, 76), outline=(190, 146, 22))
    return im


def dark_wood():  # 濃い木の床（板の継ぎ目）
    im, d = tile((96, 62, 40))
    for j in range(4):
        y = j * 12
        c = (112, 72, 46) if j % 2 else (102, 66, 42)
        d.rectangle((0, y + 1, T - 1, y + 11), fill=c)
        d.line((0, y, T - 1, y), fill=(60, 38, 24))
        xj = (j * 19 + 7) % T
        d.line((xj, y + 1, xj, y + 11), fill=(70, 44, 28))
    noise(im, 0.05, 12, 2)
    return im


def soil():      # 土・砂
    im, d = tile((176, 146, 104))
    rnd = random.Random(13)
    px = im.load()
    for _ in range(300):
        x, y = rnd.randrange(T), rnd.randrange(T)
        px[x, y] = rnd.choice(((150, 122, 84, 255), (196, 168, 124, 255), (138, 110, 76, 255)))
    return im


def rubber():    # 黒いゴムマット（横じま）
    im, d = tile((54, 54, 58))
    for y in range(0, T, 6):
        d.line((0, y + 2, T - 1, y + 2), fill=(78, 78, 84))
        d.line((0, y + 3, T - 1, y + 3), fill=(40, 40, 44))
    noise(im, 0.03, 14)
    return im


def ptile(base, seed):   # 大学の教室・廊下のPタイル（30cm角を半マスに4枚、まだらの模様、目地は上と左だけで継ぎ目が出ない）
    im, d = tile(base)
    rnd = random.Random(seed)
    px = im.load()
    for i in range(2):
        for j in range(2):
            k0 = 1 + rnd.uniform(-0.025, 0.025)
            for y in range(24):
                for x in range(24):
                    px[j * 24 + x, i * 24 + y] = shade(base, k0)
    for _ in range(110):   # まだらの小さな斑点（明るい・暗い）
        x, y = rnd.randrange(T), rnd.randrange(T)
        k = rnd.choice((0.92, 0.95, 1.05, 1.07))
        px[x, y] = shade(px[x, y], k)
        if rnd.random() < 0.4 and x + 1 < T:
            px[x + 1, y] = shade(px[x + 1, y], (k + 1) / 2)
    for i in range(2):     # 目地と、タイルの縁の光
        d.line((0, i * 24, T - 1, i * 24), fill=shade(base, 0.8))
        d.line((i * 24, 0, i * 24, T - 1), fill=shade(base, 0.8))
        d.line((1, i * 24 + 1, T - 1, i * 24 + 1), fill=shade(base, 1.05))
    for (x, y) in ((6, 9), (31, 35)):   # ワックスの光
        d.line((x, y, x + 4, y), fill=shade(base, 1.1))
    return im


def tile_carpet(seed):   # タイルカーペット（50cm角、毛の流れを1枚ごとに縦横で交互に）
    base = (104, 110, 120)
    im, d = tile(base)
    rnd = random.Random(seed)
    px = im.load()
    for i in range(2):
        for j in range(2):
            vert = (i + j) % 2 == 0
            for y in range(24):
                for x in range(24):
                    q = (x if vert else y) % 2
                    k = (0.97 if q else 1.03) + rnd.uniform(-0.04, 0.04)
                    px[j * 24 + x, i * 24 + y] = shade(base, k)
    for i in range(2):
        d.line((0, i * 24, T - 1, i * 24), fill=shade(base, 0.86))
        d.line((i * 24, 0, i * 24, T - 1), fill=shade(base, 0.86))
    return im


WALL = (230, 226, 214)


def wall(part):   # 大学の教室の壁（3段で1枚の壁）：0＝天井の見切りと上の壁、1＝壁、2＝腰見切り・腰壁・幅木
    im, d = tile(WALL)
    px = im.load()
    for y in range(T):   # 上ほどわずかに暗い（天井の陰）
        k = {0: 0.93 + 0.05 * y / T, 1: 0.98 + 0.02 * y / T, 2: 1.0}[part]
        for x in range(T):
            px[x, y] = shade(WALL, k)
    noise(im, 0.012, 30 + part, 2)
    if part == 0:
        d.rectangle((0, 0, T - 1, 4), fill=(168, 166, 160))          # 天井
        d.line((0, 5, T - 1, 5), fill=(120, 118, 114))
        d.rectangle((0, 6, T - 1, 9), fill=(240, 238, 230))          # 廻り縁
        d.line((0, 6, T - 1, 6), fill=(252, 252, 248))
        d.line((0, 10, T - 1, 10), fill=shade(WALL, 0.78))
        d.line((0, 11, T - 1, 11), fill=shade(WALL, 0.88))
    if part == 2:
        d.line((0, 19, T - 1, 19), fill=shade(WALL, 0.84))           # 腰見切りの上の影
        d.rectangle((0, 20, T - 1, 22), fill=(176, 180, 188))       # 腰見切り（スチール）
        d.line((0, 20, T - 1, 20), fill=(236, 240, 246))
        d.line((0, 22, T - 1, 22), fill=(112, 116, 124))
        base = (194, 186, 170)
        for y in range(23, 43):                                      # 腰壁（下ほど暗い）
            k = 1.02 - 0.08 * (y - 23) / 20
            for x in range(T):
                px[x, y] = shade(base, k)
        for x0 in (0, 24):                                           # 板の継ぎ目
            d.line((x0, 23, x0, 42), fill=shade(base, 0.78))
            d.line((x0 + 1, 23, x0 + 1, 42), fill=shade(base, 1.08))
        d.line((0, 23, T - 1, 23), fill=shade(base, 0.8))
        d.rectangle((0, 43, T - 1, 47), fill=(86, 86, 94))          # 幅木
        d.line((0, 43, T - 1, 43), fill=(150, 152, 160))
        d.line((0, 47, T - 1, 47), fill=(50, 50, 58))
    return im


FLOORS = [
    checker, stone, brick, marble, lambda: carpet((150, 40, 46), (124, 30, 36), 6), turf, gym, concrete,
    checkered_plate, grating, lambda: tactile(False), lambda: tactile(True), dark_wood,
    lambda: carpet((52, 74, 140), (40, 58, 116), 7), soil, rubber,
    lambda: ptile((196, 198, 192), 21), lambda: tile_carpet(22), lambda: ptile((214, 204, 184), 23),
    lambda: wall(0), lambda: wall(1), lambda: wall(2),
]


def main():
    out = ROOT / 'img' / 'tiles'
    out.mkdir(parents=True, exist_ok=True)
    im = Image.new('RGBA', (T * 2, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    stairs(d, 0, True)
    stairs(d, T, False)
    im.save(out / 'own.png')
    sheet = Image.new('RGBA', (T * 8, T * 3), (0, 0, 0, 0))
    for i, fn in enumerate(FLOORS):
        sheet.paste(fn(), ((i % 8) * T, (i // 8) * T))
    sheet.save(out / 'floor.png')
    print('img/tiles/own.png img/tiles/floor.png')


if __name__ == '__main__':
    main()
