"""キャラクターの歩行グラフィックを一から描いて img/chars/*.png に書き出す。

使い方：python3 tools/sprites/make_chars.py
1コマ32×32px、横3コマ（左足・立ち・右足）×縦4段（下・左・右・上）。ゲームでは1.5倍で描く。
部品（頭・胴・脚）を文字で描き、色は文字ごとにパレットで決める。'.' は透明。
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
FW = FH = 32

# ---------------- 部品 ----------------
HEAD = {
    'down': [
        '....hhhhhhhh....',
        '..hhHHHHHHHHhh..',
        '.hHHHHHHHHHHHHh.',
        '.hHHHHHHHHHHHHh.',
        'hHHHHHHHHHHHHHHh',
        'hHHHhHHHHHHhHHHh',
        'hHHSSHHSSHHSSHHh',
        'hHSSSSSSSSSSSSHh',
        'hHSSESSSSSSESSHh',
        'hSSSESSSSSSESSSh',
        '.SSSSSSSSSSSSSS.',
        '.sSSSSSSSSSSSSs.',
        '..sSSSSsSSSSSs..',
        '...ssSSSSSSss...',
        '.....ssssss.....',
    ],
    'left': [
        '.....hhhhhhh....',
        '...hhHHHHHHHhh..',
        '..hHHHHHHHHHHHh.',
        '.hHHHHHHHHHHHHHh',
        '.hHHHHHHHHHHHHHh',
        'hHHHHHHHHHHHHHHh',
        'hHHSSHHHHHHHHHHh',
        'hSSSSSSHHHHHHHh.',
        'hSESSSSSHHHHHHh.',
        'SSESSSSSSHHHHHh.',
        'SSSSSSSSSShHHh..',
        '.sSSSSSSSSShh...',
        '..sSSSSSSSs.....',
        '...ssSSSSs......',
        '.....ssss.......',
    ],
    'up': [
        '....hhhhhhhh....',
        '..hhHHHHHHHHhh..',
        '.hHHHHHHHHHHHHh.',
        '.hHHHHHHHHHHHHh.',
        'hHHHHHHHHHHHHHHh',
        'hHHHHHHHHHHHHHHh',
        'hHHHHHHHHHHHHHHh',
        'hHHHHHHHHHHHHHHh',
        'hHHHHHHHHHHHHHHh',
        'hHHHHHHHHHHHHHHh',
        '.hHHHHHHHHHHHHh.',
        '.hhHHHHHHHHHHhh.',
        '..hhhHHHHHHhhh..',
        '...ssSSSSSSss...',
        '.....ssssss.....',
    ],
}

BODY = {
    'blazer': {
        'down': [
            '....CCWWWWCC....',
            '..CCCCWRRWCCCC..',
            '.CCCCCWRRWCCCCC.',
            '.cCCCCCRRCCCCCc.',
            '.cCCCCCRRCCCCCc.',
            '.cCCCCCCCCCCCCc.',
            '.SCCCCCCCCCCCCS.',
            '..CCCCCCCCCCCC..',
            '..PPPPPPPPPPPP..',
        ],
        'left': [
            '.....CWCCC......',
            '....CCWCCCCC....',
            '....CCCCCCCC....',
            '....CCcCCCCC....',
            '....CCcCCCCC....',
            '....CCcCCCCC....',
            '....CCSCCCCC....',
            '....CCCCCCCC....',
            '....PPPPPPPP....',
        ],
        'up': [
            '....CCCCCCCC....',
            '..CCCCCCCCCCCC..',
            '.CCCCCCCCCCCCCC.',
            '.cCCCCCCCCCCCCc.',
            '.cCCCCCCCCCCCCc.',
            '.cCCCCCCCCCCCCc.',
            '.SCCCCCCCCCCCCS.',
            '..CCCCCCCCCCCC..',
            '..PPPPPPPPPPPP..',
        ],
    },
    'sailor': {
        'down': [
            '....NNWWWWNN....',
            '..NNNNWRRWNNNN..',
            '.CNNNNNRRNNNNNC.',
            '.cCCCCCRRCCCCCc.',
            '.cCCCCCCCCCCCCc.',
            '.cCCCCCCCCCCCCc.',
            '.SCCCCCCCCCCCCS.',
            '..KKKKKKKKKKKK..',
            '.KKkKKkKKkKKkKK.',
        ],
        'left': [
            '.....NWCCC......',
            '....NNRCCCCC....',
            '....NNCCCCCC....',
            '....CCcCCCCC....',
            '....CCcCCCCC....',
            '....CCcCCCCC....',
            '....CCSCCCCC....',
            '....KKKKKKKK....',
            '...KKkKKkKKkK...',
        ],
        'up': [
            '....NNNNNNNN....',
            '..NNNNNNNNNNNN..',
            '.CNNNNNNNNNNNNC.',
            '.cNNNNNNNNNNNNc.',
            '.cCCCCCCCCCCCCc.',
            '.cCCCCCCCCCCCCc.',
            '.SCCCCCCCCCCCCS.',
            '..KKKKKKKKKKKK..',
            '.KKkKKkKKkKKkKK.',
        ],
    },
}

# 脚：[左足, 立ち, 右足]
LEGS = {
    'pants': {
        'down': [
            ['...PPPP..PPPP...', '...PPPP..PPPP...', '...BBBB..pPPp...', '.........BBBB...'],
            ['...PPPP..PPPP...', '...PPPP..PPPP...', '...pPPp..pPPp...', '...BBBB..BBBB...'],
            ['...PPPP..PPPP...', '...PPPP..PPPP...', '...pPPp..BBBB...', '...BBBB.........'],
        ],
        'left': [
            ['....PPP..PPP....', '...PPP....PPP...', '...pp......pp...', '..BBB......BBB..'],
            ['.....PPPPP......', '.....PPPPP......', '.....pPPPp......', '....BBBBB.......'],
            ['....PPP..PPP....', '...PPP....pPP...', '..BBp.....pp....', '..........BBB...'],
        ],
    },
    'skirt': {
        'down': [
            ['....SS....SS....', '....SS....SS....', '....BB....WW....', '..........BB....'],
            ['....SS....SS....', '....SS....SS....', '....WW....WW....', '....BB....BB....'],
            ['....SS....SS....', '....SS....SS....', '....WW....BB....', '....BB..........'],
        ],
        'left': [
            ['.....SS..SS.....', '....SS....SS....', '....WW....WW....', '...BB......BB...'],
            ['......SSS.......', '......SSS.......', '......WWW.......', '.....BBBB.......'],
            ['.....SS..SS.....', '....SS....SS....', '...BBW....WW....', '...........BB...'],
        ],
    },
}

# 髪を足す（長い髪・ポニーテール）。頭の左上を(0,0)とした座標に H/h を置く
def hair_long(d):
    pts = []
    if d == 'down':
        for y in range(9, 19):
            pts += [(0, y, 'h'), (1, y, 'H'), (14, y, 'H'), (15, y, 'h')]
    elif d == 'up':
        for y in range(12, 19):
            for x in range(1, 15):
                pts.append((x, y, 'h' if x in (1, 14) or y == 18 else 'H'))
    elif d == 'left':
        for y in range(7, 18):
            for x in range(11, 15):
                pts.append((x, y, 'h' if x in (11, 14) or y == 17 else 'H'))
    return pts


CHARS = {
    'haru': {
        'body': 'blazer', 'legs': 'pants', 'hair': None,
        'pal': {
            'H': '#3d2e29', 'h': '#261b18', 'S': '#f7dcc4', 's': '#e2b597', 'E': '#2b1f1f',
            'C': '#34446f', 'c': '#232f52', 'W': '#f3f2ec', 'R': '#b8323a',
            'P': '#5c606c', 'p': '#41444e', 'B': '#3b2b22',
        },
    },
    'yui': {
        'body': 'sailor', 'legs': 'skirt', 'hair': hair_long,
        'pal': {
            'H': '#94593a', 'h': '#663922', 'S': '#f8ddc6', 's': '#e4b89b', 'E': '#3a2420',
            'C': '#f2f0e8', 'c': '#d2d0c7', 'N': '#2f3e68', 'W': '#f6f6f6', 'R': '#c8343f',
            'K': '#2f3e68', 'k': '#222d4f', 'B': '#4a3226',
        },
    },
}

OUTLINE = (40, 28, 26, 255)


def hexc(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def frame(ch, d, step):
    """1コマ分の文字の格子（32×32）を作る"""
    g = [['.'] * FW for _ in range(FH)]
    side = 'left' if d in ('left', 'right') else d
    legs_d = 'left' if side == 'left' else 'down'
    head = HEAD[side]
    body = BODY[ch['body']][side]
    legs = LEGS[ch['legs']][legs_d][step]
    ox, oy = 8, 2
    bob = 0 if step == 1 else 1  # 歩くときに少し沈む
    parts = [(head, oy + bob), (body, oy + 15 + bob), (legs, oy + 24)]
    for rows, y0 in parts:
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c != '.':
                    g[y0 + y][ox + x] = c
    if ch['hair']:
        for x, y, c in ch['hair'](side):
            yy = oy + bob + y
            if not 0 <= yy < FH:
                continue
            if side != 'up' and y < 15 and g[yy][ox + x] in 'SsE':  # 顔の上には描かない
                continue
            g[yy][ox + x] = c
    if d == 'right':
        g = [row[::-1] for row in g]
    return g


def render(ch):
    pal = {k: hexc(v) for k, v in ch['pal'].items()}
    sheet = Image.new('RGBA', (FW * 3, FH * 4), (0, 0, 0, 0))
    for r, d in enumerate(['down', 'left', 'right', 'up']):
        for s in range(3):
            g = frame(ch, d, s)
            im = Image.new('RGBA', (FW, FH), (0, 0, 0, 0))
            px = im.load()
            for y in range(FH):
                for x in range(FW):
                    if g[y][x] != '.':
                        px[x, y] = pal[g[y][x]]
            # 輪郭：色のあるマスに接する透明なマスを濃い色で塗る
            out = im.copy()
            op = out.load()
            for y in range(FH):
                for x in range(FW):
                    if px[x, y][3]:
                        continue
                    if any(0 <= x + dx < FW and 0 <= y + dy < FH and px[x + dx, y + dy][3]
                           for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                        op[x, y] = OUTLINE
            sheet.paste(out, (s * FW, r * FH))
    return sheet


def check():
    for name, rows in HEAD.items():
        assert all(len(r) == 16 for r in rows) and len(rows) == 15, ('HEAD', name)
    for b, ds in BODY.items():
        for d, rows in ds.items():
            assert all(len(r) == 16 for r in rows) and len(rows) == 9, ('BODY', b, d)
    for l, ds in LEGS.items():
        for d, fr in ds.items():
            for f in fr:
                assert all(len(r) == 16 for r in f) and len(f) == 4, ('LEGS', l, d)


if __name__ == '__main__':
    check()
    out = ROOT / 'img' / 'chars'
    out.mkdir(parents=True, exist_ok=True)
    for name, ch in CHARS.items():
        render(ch).save(out / f'{name}.png')
        print(f'img/chars/{name}.png')
