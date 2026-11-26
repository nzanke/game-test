"""タイル素材を、そのままでは画像として開けない形にして data/tilesets/ID.js に書き出す。

使い方：python3 tools/encode_tileset.py 元の画像.png ID [マスの大きさ（既定32）]

元の画像はリポジトリに入れないこと（素材の二次配布になるため）。
"""
import base64
import struct
import sys
from pathlib import Path

KEY = b'game-test-tileset'  # engine/core.js の TILE_KEY と同じにする


def png_size(data):
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        sys.exit('PNG画像ではありません')
    return struct.unpack('>II', data[16:24])


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, tid = Path(sys.argv[1]), sys.argv[2]
    size = int(sys.argv[3]) if len(sys.argv) > 3 else 32
    data = src.read_bytes()
    w, h = png_size(data)
    enc = bytes(b ^ KEY[i % len(KEY)] for i, b in enumerate(data))
    out = Path(__file__).resolve().parent.parent / 'data' / 'tilesets' / f'{tid}.js'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"// {tid} — タイル素材（{w // size}列×{h // size}行、{size}px）。tools/encode_tileset.py で作ったもの\n"
        f"G.defineTileset('{tid}', {{ size: {size}, cols: {w // size}, rows: {h // size}, data:\n"
        f"'{base64.b64encode(enc).decode()}' }});\n",
        encoding='utf-8')
    print(f'{out} を書き出しました（{w // size}列×{h // size}行）')


if __name__ == '__main__':
    main()
