"""校舎のマップを生成する：python3 tools/gen_school.py

FLOORS の「部屋の並び（西→東）」から廊下のマップを作り、data/maps/school_*.js に書き出す。
部屋の中は種類ごとの共通の作り（ROOM_TYPES）で、data/maps/school_rooms.js に書き出す。
扉の位置は data/maps/school_doors.js（G.defineDoors）に書き出す。お話のイベントは data/story.js に書く。

部屋の種類
  C       普通教室（教室の型に入る）
  office lab music art pc lecture   それぞれの型の部屋に入る
  map:ID  決まったマップに入る（例：map:room1 は保健室）
  story   扉のイベントを story.js で書く（図書室など）
  WC      トイレ（入れない）
  exit    外への出口（まだ入れない）
  locked  鍵のかかった部屋（入れない）
  ST:名前  階段（同じ名前の階段どうしで上り下りできる）
  LINK:扉の名前  渡り廊下（別の建物の、その名前の扉へつながる）
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'data' / 'maps'

# ---------------- 校舎の部屋の並び（西→東） ----------------
BUILDINGS = {
    'main': {'name': '本館', 'floor': '.', 'floors': {
        1: [('ST:W', ''), ('昇降口', 'exit'), ('用務員室', 'locked'), ('玄関', 'exit'), ('事務室', 'locked'),
            ('校長室', 'locked'), ('応接室', 'locked'), ('ST:M', ''), ('会議室', 'lecture'), ('進路室', 'office'),
            ('渡り廊下', 'LINK:渡り廊下（特別教室棟）'), ('トイレ', 'WC'), ('ST:E', ''), ('談話室', 'lecture'), ('保健室', 'map:room1')],
        2: [('ST:W', ''), ('職員室', 'office'), ('ロッカー', 'locked'), ('印刷室', 'locked'), ('放送室', 'locked'),
            ('学習指導室', 'office'), ('多目的室', 'lecture'), ('ST:M', ''), ('3の7', 'C'), ('3の6', 'C'), ('トイレ', 'WC'),
            ('ST:E', ''), ('3の5', 'C'), ('3の4', 'C')],
        3: [('ST:W', ''), ('2の3', 'C'), ('2の4', 'C'), ('2の5', 'C'), ('第二進路室', 'office'), ('2の6', 'C'),
            ('2の7', 'C'), ('ST:M', ''), ('自習室', 'lecture'), ('3の1', 'C'), ('国語資料室', 'locked'), ('トイレ', 'WC'),
            ('ST:E', ''), ('3の2', 'C'), ('3の3', 'C')],
        4: [('ST:W', ''), ('2の2', 'C'), ('2の1', 'C'), ('1の7', 'C'), ('生徒会室', 'lecture'), ('1の6', 'C'),
            ('1の5', 'C'), ('ST:M', ''), ('1の4', 'C'), ('1の3', 'C'), ('教科資料室', 'locked'), ('トイレ', 'WC'),
            ('ST:E', ''), ('1の2', 'C'), ('1の1', 'C')],
    }},
    'annex': {'name': '特別教室棟', 'floor': ',', 'floors': {
        1: [('ST:W', ''), ('調理室', 'lab'), ('調理準備室', 'locked'), ('被服準備室', 'locked'), ('被服室', 'lecture'),
            ('生化講義室', 'lecture'), ('化学実験室', 'lab'), ('渡り廊下（特別教室棟）', 'LINK:渡り廊下'),
            ('化学準備室', 'locked'), ('生物準備室', 'locked'), ('ST:E', ''), ('生物実験室', 'lab')],
        2: [('ST:W', ''), ('美術室', 'art'), ('美術準備室', 'locked'), ('社会科準備室', 'locked'), ('社会科教室', 'lecture'),
            ('物地講義室', 'lecture'), ('物理実験室', 'lab'), ('物理準備室', 'locked'), ('暗室', 'locked'),
            ('ST:E', ''), ('地学準備室', 'locked'), ('地学実験室', 'lab')],
        3: [('ST:W', ''), ('図書室', 'story'), ('作業室', 'locked'), ('書庫', 'locked'), ('学習室', 'lecture'),
            ('パソコン室', 'pc'), ('映写室', 'locked'), ('視聴覚室', 'lecture'), ('LL準備室', 'locked'),
            ('ST:E', ''), ('スタディルーム', 'lecture')],
        4: [('音楽室', 'music'), ('音楽準備室', 'locked'), ('資料室', 'locked'), ('資料室２', 'locked'), ('ST:E', '')],
    }},
}

WIDTH = {'C': 8, 'office': 8, 'lab': 8, 'music': 8, 'art': 8, 'pc': 8, 'lecture': 6, 'story': 8,
         'map': 6, 'WC': 4, 'exit': 6, 'locked': 4, 'ST': 4, 'LINK': 4}
BIG = {'職員室': 12, '図書室': 10, '会議室': 8, '昇降口': 8}

# 部屋の型：マップID、扉の位置（入ったときは扉の1マス下に立つ）
ROOM_TYPES = {
    'C': ('classroom', 14), 'office': ('room_office', 8), 'lab': ('room_lab', 8), 'music': ('room_music', 8),
    'art': ('room_art', 8), 'pc': ('room_pc', 8), 'lecture': ('room_lecture', 8),
}
FIXED_ROOMS = {'room1': 12}  # 決まったマップの扉の列


def kind_of(k):
    return k.split(':')[0]


def door_ev(eid, x, list_, sensor=False):
    return {'id': eid, 'x': x, 'y': 2, 'pages': [
        {'trigger': 'touch', 'priority': 'same', 'sensor': sensor, 'list': list_}]}


def build_floor(bid, b, fl, slots, stairs_at, doors):
    floor = b['floor']
    cols_top = [[], [], []]
    events, signs = [], []
    x = 1
    for name, kind in slots:
        k = kind_of(name) if name.startswith('ST:') else kind_of(kind)
        w = WIDTH['ST'] if name.startswith('ST:') else BIG.get(name, WIDTH[k])
        if name.startswith('ST:'):
            for i in range(w):
                for r, ch in enumerate('456'):
                    cols_top[r].append(ch)
            signs.append({'x': x + 1, 'y': 0, 'text': '階段'})
            stairs_at[(bid, fl, name)] = x + 1
        else:
            dx = x + w - 2
            for i in range(w):
                for r in range(3):
                    if i == 0:
                        cols_top[r].append('456'[r])
                    elif i == w - 2:
                        cols_top[r].append('789'[r])
                    else:
                        cols_top[r].append('123'[r])
            signs.append({'x': dx, 'y': 0, 'text': name})
            doors[name] = {'map': f'{bid}{fl}f', 'x': dx, 'y': 2}
            eid = f'door{dx}'
            if k in ROOM_TYPES:
                mid, rx = ROOM_TYPES[k]
                events.append(door_ev(eid, dx, [['se', 'door'], ['enter', mid, rx, 3, 'down', name]]))
            elif k == 'map':
                mid = kind.split(':')[1]
                events.append(door_ev(eid, dx, [['se', 'door'], ['enter', mid, FIXED_ROOMS[mid], 3, 'down', name]]))
            elif k == 'WC':
                events.append(door_ev(eid, dx, [['text', '', 'トイレだ。いまは用はない。']]))
            elif k == 'exit':
                events.append(door_ev(eid, dx, [['text', '', '外へ出るのは、また今度にしよう。']]))
            elif k == 'locked':
                events.append(door_ev(eid, dx, [['se', 'buzzer'], ['text', '', f'{name}には鍵がかかっている。']]))
            elif k == 'LINK':
                events.append({'link': kind.split(':', 1)[1], 'id': eid, 'x': dx, 'y': 2})
            # story：扉のイベントは story.js で足す
        x += w
    width = x + 1
    top = [''.join(['#'] + c + ['#']) for c in cols_top]
    rows = top + ['#' + floor * (width - 2) + '#' for _ in range(4)] + ['#' * width]
    # 階段のマス（2×2）
    for (bb, ff, sname), sx in stairs_at.items():
        if bb == bid and ff == fl:
            for yy in (3, 4):
                r = list(rows[yy])
                r[sx] = r[sx + 1] = '^'
                rows[yy] = ''.join(r)
    return rows, events, signs


def stairs_events(bid, fl, floors, stairs_at):
    evs = []
    for (bb, ff, sname), sx in stairs_at.items():
        if bb != bid or ff != fl:
            continue
        up = (bid, fl + 1, sname) in stairs_at
        dn = (bid, fl - 1, sname) in stairs_at
        opts, branches = [], []
        if up:
            tx = stairs_at[(bid, fl + 1, sname)]
            opts.append(f'{fl + 1}階へ上る')
            branches.append([['se', 'door'], ['transfer', f'{bid}{fl + 1}f', tx, 5, 'down']])
        if dn:
            tx = stairs_at[(bid, fl - 1, sname)]
            opts.append(f'{fl - 1}階へ下りる')
            branches.append([['se', 'door'], ['transfer', f'{bid}{fl - 1}f', tx, 5, 'down']])
        opts.append('やめる')
        branches.append([])
        lst = [['choice', opts, branches, {'cancel': len(opts) - 1}]]
        for i, (xx, yy) in enumerate([(sx, 3), (sx + 1, 3), (sx, 4), (sx + 1, 4)]):
            evs.append({'id': f'stairs{sname[3:]}{i}', 'x': xx, 'y': yy,
                        'pages': [{'trigger': 'touch', 'priority': 'below', 'sensor': False, 'list': lst}]})
    return evs


# ---------------- 部屋の型 ----------------
def room_tiles(door_x, wall='456', floor='.'):
    top = []
    for r in range(3):
        top.append('#' + ''.join('789'[r] if x == door_x else wall[r] for x in range(1, 16)) + '#')
    return top + ['#' + floor * 15 + '#' for _ in range(9)] + ['#' * 17]


def grid(tile, xs, ys, **kw):
    return [dict({'tile': tile, 'x': x, 'y': y}, **kw) for y in ys for x in xs]


def make_rooms():
    I = 'school_in'
    rooms = {}
    board = {'tile': [I, 0, 25, 3, 2], 'x': 3, 'y': 0, 'solid': False}
    rooms['classroom'] = ('教室', room_tiles(14), [
        board, {'tile': [I, 0, 25, 3, 2], 'x': 6, 'y': 0, 'solid': False},
        {'tile': [I, 6, 34, 1, 2], 'x': 5, 'y': 3},
        *grid([I, 6, 30, 1, 2], (3, 5, 7, 9, 11, 13), (6, 9)),
        {'tile': [I, 7, 34, 1, 2], 'x': 15, 'y': 10},
    ])
    rooms['room_office'] = ('職員室', room_tiles(8, floor=':'), [
        *grid([I, 0, 39, 3, 2], (2, 6, 11), (5, 9)),
        {'tile': [I, 2, 20, 3, 2], 'x': 1, 'y': 2, 'solid': 'bottom'},
        {'tile': [I, 2, 22, 3, 2], 'x': 12, 'y': 2, 'solid': 'bottom'},
        {'tile': [I, 5, 19], 'x': 5, 'y': 1, 'solid': False},
    ])
    rooms['room_lab'] = ('実験室', room_tiles(8, floor=';'), [
        *grid([I, 0, 42, 3, 2], (2, 7, 12), (5, 9)),
        {'tile': [I, 3, 42, 1, 2], 'x': 15, 'y': 2, 'solid': 'bottom'},
        {'tile': [I, 0, 37, 3, 2], 'x': 1, 'y': 2, 'solid': 'bottom'},
        {'tile': [I, 0, 25, 3, 2], 'x': 11, 'y': 0, 'solid': False},
    ])
    rooms['room_music'] = ('音楽室', room_tiles(8, floor=':'), [
        {'tile': [I, 0, 30, 3, 3], 'x': 2, 'y': 3},
        {'tile': [I, 0, 33, 1, 2], 'x': 6, 'y': 4},
        *grid([I, 4, 30, 1, 1], (8, 10, 12, 14), (7, 9, 11)),
        {'tile': [I, 0, 25, 3, 2], 'x': 11, 'y': 0, 'solid': False},
    ])
    rooms['room_art'] = ('美術室', room_tiles(8), [
        *grid([I, 3, 48, 1, 2], (3, 6, 10, 13), (5, 9)),
        {'tile': [I, 0, 47, 1, 2], 'x': 15, 'y': 6},
        {'tile': [I, 2, 22, 3, 2], 'x': 1, 'y': 2, 'solid': 'bottom'},
    ])
    rooms['room_pc'] = ('パソコン室', room_tiles(8, floor=';'), [
        *grid([I, 3, 39, 3, 2], (2, 7, 12), (5, 9)),
        {'tile': [I, 0, 25, 3, 2], 'x': 11, 'y': 0, 'solid': False},
    ])
    rooms['room_lecture'] = ('講義室', room_tiles(8), [
        {'tile': [I, 0, 25, 3, 2], 'x': 3, 'y': 0, 'solid': False},
        *grid([I, 0, 42, 3, 2], (2, 7, 12), (5, 9)),
        {'tile': [I, 7, 34, 1, 2], 'x': 15, 'y': 10},
    ])
    return rooms


def js_map(mid, name, rows, objects=None, events=None, signs=None, comment=''):
    d = {'name': name, 'tiles': rows}
    if objects:
        d['objects'] = objects
    if signs:
        d['signs'] = signs
    d['events'] = events or []
    body = json.dumps(d, ensure_ascii=False, indent=1)
    return f"// {comment}（tools/gen_school.py で生成。直接書き換えず、生成スクリプトを直す）\nG.defineMap('{mid}', {body});\n"


def main():
    doors, stairs_at, out = {}, {}, {}
    # 1回目：階段の位置を集める
    for bid, b in BUILDINGS.items():
        for fl, slots in b['floors'].items():
            build_floor(bid, b, fl, slots, stairs_at, {})
    # 2回目：マップを作る
    links = []
    for bid, b in BUILDINGS.items():
        for fl, slots in b['floors'].items():
            rows, evs, signs = build_floor(bid, b, fl, slots, stairs_at, doors)
            evs += stairs_events(bid, fl, b['floors'], stairs_at)
            mid = f'{bid}{fl}f'
            out[mid] = [f"{b['name']}{fl}階", rows, evs, signs]
            links += [(mid, e) for e in evs if 'link' in e]
    for mid, e in links:  # 渡り廊下
        to = doors[e.pop('link')]
        e['pages'] = [{'trigger': 'touch', 'priority': 'same', 'sensor': False,
                       'list': [['se', 'door'], ['transfer', to['map'], to['x'], 3, 'down']]}]
    files = []
    for mid, (name, rows, evs, signs) in out.items():
        assert len({len(r) for r in rows}) == 1, mid
        p = OUT / f'school_{mid}.js'
        p.write_text(js_map(mid, name, rows, events=evs, signs=signs, comment=f'{name}の廊下'), encoding='utf-8')
        files.append(p.name)
    rooms_js = ''
    for mid, (name, rows, objs) in make_rooms().items():
        evs = [door_ev('exit', rows[0].index('7'), [['se', 'door'], ['back']])]
        rooms_js += js_map(mid, name, rows, objects=objs, events=evs, comment=f'部屋の型：{name}')
    (OUT / 'school_rooms.js').write_text(rooms_js, encoding='utf-8')
    files.append('school_rooms.js')
    (OUT / 'school_doors.js').write_text(
        '// 扉の位置（tools/gen_school.py で生成）\nG.defineDoors(' + json.dumps(doors, ensure_ascii=False, indent=1) + ');\n',
        encoding='utf-8')
    files.append('school_doors.js')
    for f in files:
        print(f'<script src="data/maps/{f}"></script>')


if __name__ == '__main__':
    main()
