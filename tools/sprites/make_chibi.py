"""ちびキャラ（手本：RPGツクールMVの標準キャラの比率、約1.5頭身）でハルとユイを描く。

使い方：python3 tools/sprites/make_chibi.py
1コマ48×48px、横3コマ（左足・立ち・右足）×縦4段（下・左・右・上）、等倍。
描き方は make_trial.py と同じ「6倍でイラストとして描いて縮める」方式（道具も同じものを使う）。
比率は手本を測った値：頭（髪）y5〜33・横31px、前髪は目のすぐ上まで、大きな目（y25〜29）、首なし、胴 y33〜43、足 y44〜47。
座標は 48×48 のコマの中の位置（x は体の中心からのずれ）。手本の絵は写さない。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_trial as mt  # noqa: E402
from PIL import Image, ImageFilter  # noqa: E402

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


BASE = {
    'skin1': '#fff0e4', 'skin2': '#f4cdb6', 'skinS': '#d99b86', 'skinLine': '#a8685a', 'blush': '#ff8f96',
    'eyeW': '#ffffff', 'lash': '#1a0f1c', 'mouth': '#c85a5e', 'line': '#2a1e2a',
}
CHARS = {
    'yui_chibi': dict(BASE, girl=True, **{
        'hair1': '#343a62', 'hair2': '#16172a', 'hairL': '#7d8fd6', 'hairLine': '#0e0f1c',
        'iris1': '#2a1650', 'iris2': '#8a5ad8', 'iris3': '#d8c2ff',
        'top1': '#f7ecd4', 'top2': '#cdb88f', 'topLine': '#8c7754', 'inner': '#ffffff', 'ribbon1': '#ee4a5e', 'ribbon2': '#9a1f34',
        'low1': '#8e93a6', 'low2': '#4f5366', 'leg': '#2a2730', 'shoe1': '#7a5a4c', 'shoe2': '#2e201c',
    }),
    'haru_chibi': dict(BASE, girl=False, **{
        'hair1': '#3c3f4c', 'hair2': '#16171d', 'hairL': '#8f96b0', 'hairLine': '#0d0d12',
        'iris1': '#1e1614', 'iris2': '#6b4c3a', 'iris3': '#b08a70',
        'top1': '#ffffff', 'top2': '#d6dbe6', 'topLine': '#7d8496', 'inner': '#f1c9b1', 'ribbon1': '#2a2420', 'ribbon2': '#2a2420',
        'low1': '#3d4360', 'low2': '#1b1e2c', 'leg': '#1b1e2c', 'shoe1': '#4a4446', 'shoe2': '#101012',
    }),
}


def colors(ch):
    return {k: (rgb(v) if isinstance(v, str) else v) for k, v in ch.items()}


# ---------------- 体（首なし・胴は短い・足は小さい） ----------------
def body(a, c, side, step, back):
    girl = c['girl']
    lift = {0: (1.2, 0), 1: (0, 0), 2: (0, 1.2)}[step]
    if side == 'left':
        sw = {0: -1.6, 1: 0, 2: 1.6}[step]
        # 足
        if step == 1:
            a.part([('e', -6, 43.2, 3, 47.4)], c['shoe1'], c['shoe2'], line=c['line'], lw=0.7)
        else:
            a.part([('e', 0.5, 42.4, 8, 46.4)], c['shoe2'], c['shoe2'], line=c['line'], lw=0.7)
            a.part([('e', -8.6, 43.2, -1, 47.4)], c['shoe1'], c['shoe2'], line=c['line'], lw=0.7)
        # 下（スカート・ズボン）
        if girl:
            a.part([('p', [(-6.4, 38.5), (6.4, 38.5), (8, 44.4), (-8, 44.4)])], c['low1'], c['low2'], shade=c['low2'], line=c['line'], lw=0.7)
        else:
            a.part([('p', [(-5.6, 39), (5.6, 39), (5.8, 44.4), (-5.8, 44.4)])], c['low1'], c['low2'], shade=c['low2'], line=c['line'], lw=0.7)
        # 胴と手前の腕
        a.part([('p', [(-6.4, 32.6), (6.4, 32.6), (6, 40.4), (-6, 40.4)])], c['top1'], c['top2'], shade=c['top2'], line=c['topLine'], lw=0.7)
        a.part([('p', [(-2.2, 33.4), (2.4, 33.4), (2.4 + sw, 39.8), (-2.2 + sw, 39.8)])], c['top1'], c['top2'], line=c['topLine'], lw=0.6)
        a.part([('e', -2.1 + sw, 38.8, 2.1 + sw, 42.6)], c['skin1'], c['skin2'], line=c['skinLine'], lw=0.5)
        a.part([('p', [(-6.8, 32.6), (-4, 32.6), (-5.2, 35.8)])], c['ribbon1'], c['ribbon2'], lw=0.4)
        return
    la, ra = lift
    for x0, x1, l in ((-7, -0.6, la), (0.6, 7, ra)):  # 足
        a.part([('e', x0, 43.2 - l, x1, 47.2 - l)], c['shoe1'], c['shoe2'], light=(210, 180, 160), line=c['line'], lw=0.7, la=0.6)
    if girl:
        a.part([('p', [(-8, 38.2), (8, 38.2), (9.8, 44.6), (-9.8, 44.6)])], c['low1'], c['low2'], shade=c['low2'], line=c['line'], lw=0.7)
    else:
        for x0, x1, l in ((-6.6, -0.4, la), (0.4, 6.6, ra)):
            a.part([('p', [(x0, 39), (x1, 39), (x1, 44.4 - l), (x0, 44.4 - l)])], c['low1'], c['low2'], shade=c['low2'], line=c['line'], lw=0.7)
    for s in (-1, 1):  # 腕
        a.part([('p', [(s * 8.2, 33), (s * 11.4, 33.8), (s * 12, 40.2), (s * 8.8, 40.6)])], c['top1'], c['top2'], shade=c['top2'], line=c['topLine'], lw=0.6)
        a.part([('e', s * 10.4 - 2, 39, s * 10.4 + 2, 42.8)], c['skin1'], c['skin2'], line=c['skinLine'], lw=0.5)
    m = a.part([('p', [(-8.8, 32.4), (8.8, 32.4), (8, 40.6), (-8, 40.6)])], c['top1'], c['top2'], shade=c['top2'], light=(255, 252, 240), line=c['topLine'], lw=0.7)
    if not back:
        if girl:
            a.clip(m, [('p', [(-1.6, 32.4), (1.6, 32.4), (1.4, 40.4), (-1.4, 40.4)])], c['inner'], 1.0)
        else:
            a.clip(m, [('p', [(-2, 32.4), (2, 32.4), (0, 35.4)])], c['inner'], 1.0)
            a.clip(m, [('r', -0.2, 35.4, 0.2, 40)], c['topLine'], 0.7)
        a.part([('p', [(-2.4, 32.4), (0, 34), (2.4, 32.4), (1.8, 35.8), (0, 34.8), (-1.8, 35.8)])], c['ribbon1'], c['ribbon2'], lw=0.4) if girl else None
    if not girl:
        a.part([('r', -8, 39.4, 8, 40.8)], c['ribbon1'], c['ribbon2'], lw=0.4)  # ベルト


# ---------------- 頭（大きく、前髪は目のすぐ上まで、目は大きく下寄り） ----------------
def eye(a, c, cx, flip=False, side=False):
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


def bangs(a, c, x0, x1, tips, top=12, base=21.6):
    shapes = [('r', x0, top, x1, base)]
    for tx0, tx1, y in tips:
        shapes.append(('p', [(tx0, base - 0.5), (tx1, base - 0.5), ((tx0 + tx1) / 2, y)]))
    return a.part(shapes, c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'], lw=0.7)


def head(a, c, side):
    girl = c['girl']
    if side == 'up':
        if girl:
            a.part([('p', [(-15.6, 18), (15.6, 18), (15, 36), (10, 38.6), (0, 37.4), (-10, 38.6), (-15, 36)])], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
        hm = a.part([('e', -15.6, 5 if girl else 4, 15.6, 33.4)], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
        if not girl:
            a.part([('p', [(x - 3, 30), (x + 3, 30), (x, 34)]) for x in (-8, -3, 3, 8)], c['hair1'], c['hair2'], line=c['hairLine'], lw=0.6)
        a.clip(hm, [('e', -11, 8.4, 1, 11.6)], c['hairL'], 0.45, blur=0.6)
        return
    if side == 'left':
        if girl:
            a.part([('p', [(1, 14), (15.6, 14), (15, 36), (9, 38.6), (3, 33)])], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
        hm = a.part([('e', -14.6, 5 if girl else 4, 15, 33)], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
        fm = a.part([('e', -15.4, 15.6, 3.6, 33.6)], c['skin1'], c['skin2'], shade=c['skinS'], line=c['skinLine'], lw=0.6)
        a.clip(fm, [('r', -16, 20, 4, 24.4)], c['skinS'], 0.5, blur=0.8)
        bangs(a, c, -15.2, 3, [(-15.6, -11.6, 25), (-12.4, -8.4, 24), (-9, -5, 25.2), (-5.6, -1.6, 23.6), (-2, 2.6, 24.4)])
        a.part([('p', [(4.6, 14), (14.4, 14), (14, 28.4), (8.6, 32.4), (5.6, 26)])], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'], lw=0.7)
        a.clip(hm, [('e', -8, 8.4, 6, 11.6)], c['hairL'], 0.45, blur=0.6)
        eye(a, c, -10.4, side=True)
        if girl:
            a.blob(-13.4, 29.8, -10, 31.4, c['blush'], 0.45, 0.6)
        a.stroke([(-13.6, 31.8), (-12.6, 32)], c['mouth'], 0.5)
        if girl:
            a.part([('p', [(6, 9.6), (9.6, 8), (10.4, 9.8), (6.8, 11.4)])], c['ribbon1'], c['ribbon2'], lw=0.4)
        if not girl:
            a.part([('p', [(-4, 6), (-2, 1.6), (2, 5.2)]), ('p', [(3, 5.2), (8, 2), (8, 7)]), ('p', [(10, 8), (15.6, 7), (13, 12)])], c['hair1'], c['hair2'], line=c['hairLine'], lw=0.6)
        return
    # 正面
    if girl:
        a.part([('p', [(-15.8, 16), (-11.4, 16), (-11.2, 36), (-15.2, 38)]), ('p', [(15.8, 16), (11.4, 16), (11.2, 36), (15.2, 38)])], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
    hm = a.part([('e', -15.6, 5 if girl else 4, 15.6, 33)], c['hair1'], c['hair2'], shade=c['hair2'], line=c['hairLine'])
    if not girl:
        a.part([('p', [(-11, 8), (-14, 3), (-6, 6)]), ('p', [(-5, 5.4), (-2.6, 0.8), (2, 5)]), ('p', [(3, 5.2), (8.6, 1.8), (8, 7)]), ('p', [(9, 8), (14.4, 5), (12.6, 11)])], c['hair1'], c['hair2'], line=c['hairLine'], lw=0.6)
    fm = a.part([('e', -10.4, 15.6, 10.4, 33.6)], c['skin1'], c['skin2'], shade=c['skinS'], sh=(1.2, 1.4), sb=1.0, line=c['skinLine'], lw=0.6)
    a.clip(fm, [('r', -11, 20, 11, 24.4)], c['skinS'], 0.5, blur=0.8)
    tips = [(-12, -7.6, 25.4), (-8.4, -4, 24.2), (-4.6, -0.2, 25.6), (-0.8, 3.6, 23.8), (3, 7.4, 25), (6.8, 11.6, 25.8)]
    bm = bangs(a, c, -12.4, 12.4, tips)
    for s in (-1, 1):  # 顔の横の髪
        a.part([('p', [(s * 15.4, 16), (s * 10.6, 16), (s * 10.2, 30), (s * 12.4, 33.4), (s * 15, 26)])], c['hair1'] if s < 0 else c['hair2'], c['hair2'], line=c['hairLine'], lw=0.6)
    a.clip(hm, [('e', -11, 8.4, 1, 11.6)], c['hairL'], 0.45, blur=0.6)
    a.clip(bm, [('e', -11, 8.4, 1, 11.6)], c['hairL'], 0.3, blur=0.6)
    eye(a, c, -5, flip=False)
    eye(a, c, 5, flip=True)
    if girl:
        a.blob(-8.6, 29.8, -4.8, 31.4, c['blush'], 0.45, 0.6)
        a.blob(4.8, 29.8, 8.6, 31.4, c['blush'], 0.45, 0.6)
    a.stroke([(-0.9, 31.6), (0, 31.9), (0.9, 31.6)], c['mouth'], 0.5)
    if girl:
        a.part([('p', [(6.4, 9), (10, 7.4), (10.8, 9.2), (7.2, 10.8)])], c['ribbon1'], c['ribbon2'], lw=0.4)


def frame(ch, d, step):
    c = colors(ch)
    side = 'left' if d in ('left', 'right') else d
    a = Chibi()
    body(a, c, side, step, side == 'up')
    up = Chibi()
    head(up, c, side)
    im = a.im
    bob = 0 if step == 1 else round(0.6 * SS)
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
