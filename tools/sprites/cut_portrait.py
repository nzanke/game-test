"""立ち絵の画像の白い背景を抜いて、余白を切り詰める。
使い方: python3 -I tools/sprites/cut_portrait.py 元の画像.png img/portraits/名前.png
外側から白に近い色だけをたどって透明にするので、絵の中の白（靴下・肌の明るい所）は残る。縁は白さに応じて半透明にしてなじませる。
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGBA')
a = np.asarray(im).astype(np.float32)
rgb = a[..., :3]
whiteness = rgb.min(axis=2)                      # 3色のうち最も暗い値（白ほど大きい）
near = (whiteness > 236) & (rgb.max(axis=2) - rgb.min(axis=2) < 14)   # 白に近く、色みのない所
lab, n = ndimage.label(near)
edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(edge))
# 背景のすぐ外側の縁（2ドット）は、白さに応じて半透明にする
ring = ndimage.binary_dilation(bg, iterations=2) & ~bg
alpha = np.where(bg, 0, 255).astype(np.float32)
soft = np.clip((255 - whiteness) / (255 - 200) * 255, 0, 255)
alpha[ring] = np.minimum(alpha[ring], soft[ring])
a[..., 3] = np.minimum(a[..., 3], alpha)
res = Image.fromarray(a.astype(np.uint8), 'RGBA')
box = res.getbbox()
res = res.crop((max(0, box[0] - 4), max(0, box[1] - 4), min(res.width, box[2] + 4), box[3]))
res.save(out)
print(out, res.size)
