"""自作のタイルを描いて img/tiles/own.png に書き出す（1マス48px）。

使い方：python3 tools/sprites/make_tiles.py
0列目：階段（上り）　1列目：階段（下り）
"""
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


def main():
    im = Image.new('RGBA', (T * 2, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    stairs(d, 0, True)
    stairs(d, T, False)
    out = ROOT / 'img' / 'tiles'
    out.mkdir(parents=True, exist_ok=True)
    im.save(out / 'own.png')
    print('img/tiles/own.png')


if __name__ == '__main__':
    main()
