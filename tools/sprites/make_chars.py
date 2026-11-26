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
        '..hhHHHLLHHHhh..',
        '.hHHHLLLLHHHHHh.',
        '.hHHHHHHHHHHHHh.',
        'hHHHHHHHHHHHHHHh',
        'hHHhHHHHHHHhHHHh',
        'hHhSSHhSShHSSHHh',
        'hHSSSSSSSSSSSSHh',
        'hHSEESSSSSSEESHh',
        'hSSeISSSSSSeISSh',
        'hSSIISSSSSSIISSh',
        '.sSpSSSSSSSSpSs.',
        '..sSSSSmmSSSSs..',
        '...ssSSSSSSss...',
        '.....ssssss.....',
    ],
    'left': [
        '.....hhhhhhh....',
        '...hhHHLLHHHhh..',
        '..hHHLLLHHHHHHh.',
        '.hHHHHHHHHHHHHHh',
        '.hHHHHHHHHHHHHHh',
        'hHHHHHHHHHHHHHHh',
        'hHhSSHHHHHHHHHHh',
        'hSSSSSSHHHHHHHh.',
        'hSEESSSSHHHHHHh.',
        'SSeISSSSSHHHHHh.',
        'SSIISSSSSShHHh..',
        '.SpSSSSSSSShh...',
        '..smSSSSSSs.....',
        '...ssSSSSs......',
        '.....ssss.......',
    ],
    'up': [
        '....hhhhhhhh....',
        '..hhHHHLLHHHhh..',
        '.hHHHLLLLHHHHHh.',
        '.hHHHHLLHHHHHHh.',
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

# 胴（夏服）
BODY = {
    'shirt': {
        'down': [
            '.....wWWWWw.....',
            '..wWWWWwWWWWWw..',
            '.wWWWWWwWWWWWWw.',
            '.SwWWWWwWWWWWwS.',
            '.SwWWWWWWWWWWwS.',
            '.SwWWWWWWWWWWwS.',
            '.sSWWWWWWWWWWSs.',
            '..PPPPPPPPPPPP..',
            '..PPPPPPPPPPPP..',
        ],
        'left': [
            '.....wWWWw......',
            '....wWWWWWWw....',
            '....wWWWWWWw....',
            '....wWSWWWWw....',
            '....wWSWWWWw....',
            '....wWSWWWWw....',
            '....wWsWWWWw....',
            '....PPPPPPPP....',
            '....PPPPPPPP....',
        ],
        'up': [
            '.....wWWWWw.....',
            '..wWWWWWWWWWWw..',
            '.wWWWWWWWWWWWWw.',
            '.SwWWWWWWWWWWwS.',
            '.SwWWWWWWWWWWwS.',
            '.SwWWWWWWWWWWwS.',
            '.sSWWWWWWWWWWSs.',
            '..PPPPPPPPPPPP..',
            '..PPPPPPPPPPPP..',
        ],
    },
    'sailor': {
        'down': [
            '....NNWWWWNN....',
            '..NNNNWRRWNNNN..',
            '.wNNNNNRRNNNNNw.',
            '.SwWWWWRRWWWWwS.',
            '.SwWWWWWWWWWWwS.',
            '.SwWWWWWWWWWWwS.',
            '.sSKKKKKKKKKKSs.',
            '..KKKKKKKKKKKK..',
            '.KKkKKkKKkKKkKK.',
        ],
        'left': [
            '.....NwWWW......',
            '....NNRWWWWw....',
            '....NNWWWWWw....',
            '....wWSWWWWw....',
            '....wWSWWWWw....',
            '....wWSWWWWw....',
            '....KKsKKKKK....',
            '....KKKKKKKK....',
            '...KKkKKkKKkK...',
        ],
        'up': [
            '....NNNNNNNN....',
            '..NNNNNNNNNNNN..',
            '.wNNNNNNNNNNNNw.',
            '.SNNNNNNNNNNNNS.',
            '.SwWWWWWWWWWWwS.',
            '.SwWWWWWWWWWWwS.',
            '.sSKKKKKKKKKKSs.',
            '..KKKKKKKKKKKK..',
            '.KKkKKkKKkKKkKK.',
        ],
    },
}

# 脚：[左足, 立ち, 右足]
LEGS = {
    'pants': {
        'down': [
            ['...PPPP..PPPP...', '...PPPP..PPPP...', '...BBBB..qPPq...', '.........BBBB...'],
            ['...PPPP..PPPP...', '...PPPP..PPPP...', '...qPPq..qPPq...', '...BBBB..BBBB...'],
            ['...PPPP..PPPP...', '...PPPP..PPPP...', '...qPPq..BBBB...', '...BBBB.........'],
        ],
        'left': [
            ['....PPP..PPP....', '...PPP....PPP...', '...qq......qq...', '..BBB......BBB..'],
            ['.....PPPPP......', '.....PPPPP......', '.....qPPPq......', '....BBBBB.......'],
            ['....PPP..PPP....', '...PPP....qPP...', '..BBq.....qq....', '..........BBB...'],
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
        'body': 'shirt', 'legs': 'pants', 'hair': None,
        'pal': {
            'H': '#3a3c44', 'h': '#212329', 'L': '#646874',
            'S': '#f7dcc4', 's': '#e2b597', 'p': '#f2b8a8', 'm': '#c9826e',
            'E': '#2a1f1d', 'I': '#4a3a33', 'e': '#ffffff',
            'W': '#f6f6f2', 'w': '#cfd2d8',
            'P': '#2f3242', 'q': '#1f2130', 'B': '#2a2220',
        },
    },
    'yui': {
        'body': 'sailor', 'legs': 'skirt', 'hair': hair_long,
        'pal': {
            'H': '#94593a', 'h': '#663922', 'L': '#c08560',
            'S': '#f8ddc6', 's': '#e4b89b', 'p': '#f4b2a6', 'm': '#c9806c',
            'E': '#2e1d1a', 'I': '#7a4430', 'e': '#ffffff',
            'W': '#f7f7f3', 'w': '#d3d5da', 'N': '#2f3e68', 'R': '#c8343f',
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
            if c == 'H' and side != 'up' and (x + y) % 5 == 0:
                c = 'L'  # 長い髪にもつやを入れる
            yy = oy + bob + y
            if not 0 <= yy < FH:
                continue
            if side != 'up' and y < 15 and g[yy][ox + x] in 'SsEIepm':  # 顔の上には描かない
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
