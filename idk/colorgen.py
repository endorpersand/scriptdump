"""
creation: December 22, 2020?

idk
"""

from itertools import product
from colorsys import rgb_to_hls
from fractions import Fraction
divs = 3
MIN = 64
MAX = 192
d = [round(MIN + (MAX - MIN) * i / (divs - 1)) for i in range(divs)]
#rgbs = [*product(d, repeat=3)]
rgbs = [tuple(int(c,16) for c in [rgb[:2], rgb[2:4], rgb[4:]]) for rgb in ['c04040', '4040c0', '40c040', 'c0c040', 'c06b40', '6b40c0', '40c0c0', '6bc040', 'c09640', '9640c0', '4096c0', '40c096', '96c040', 'c040c0', '406bc0', '40c06b', 'c04096', 'c06bc0', '6bc06b', 'c0966b', 'c0406b', 'c06b96', '6b96c0', '96c06b', 'c06b6b', '964040', '6b6bc0', '6bc0c0', 'c0c06b', '966b40', '966bc0', '6bc096', '969640', '406b40', '404096', '40966b', '6b9640', '406b6b', '96406b', '406b96', '409640', '40406b', '6b4040', '964096', '409696', '6b406b', '6b6b40', '6b4096', 'c09696', '404040', '966b6b', '96c0c0', 'c0c096', '6b6b6b', '6b9696', 'c096c0', '96c096', '969696', '6b6b96', '6b966b', '9696c0', 'c0c0c0', '966b96', '96966b']]
rgbss = rgbs.copy()
hlss = (rgb_to_hls(*(c/255 for c in rgb)) for rgb in rgbs)

rgbhlss = {rgb: hls for rgb, hls in zip(rgbs,hlss)}
rgbss.sort(key=lambda a: rgbhlss[a][0])
rgbss.sort(key=lambda a: -rgbhlss[a][2])
print(rgbs)
print(*(rgbss.index(rgb) for rgb in rgbs))
#drgbs = [( int(c * (MAX - MIN) + MIN) for c in rgb) for rgb in rgbs]
print(*('"rgb({},{},{})"'.format(*rgb) for rgb in rgbs),sep=", ")
#print(*product(range(4), repeat=3))
flip = {key:val for val, key in enumerate([0x40, 0x6b, 0x96, 0xc0])}
print([tuple(flip[c] for c in rgb) for rgb in rgbs[:16]])