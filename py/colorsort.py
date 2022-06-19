"""
creation: unknown

Attempt to sort colors in a way that tries to make colors next to each other in the sequence distinguished
Used for UHC team coloring
"""

import colorsys
clrs  = ["#404040","#40406b","#404096","#4040c0","#406b40","#406b6b","#406b96","#406bc0","#409640","#40966b","#409696","#4096c0","#40c040","#40c06b","#40c096","#40c0c0","#6b4040","#6b406b","#6b4096","#6b40c0","#6b6b40","#6b6b6b","#6b6b96","#6b6bc0","#6b9640","#6b966b","#6b9696","#6b96c0","#6bc040","#6bc06b","#6bc096","#6bc0c0","#964040","#96406b","#964096","#9640c0","#966b40","#966b6b","#966b96","#966bc0","#969640","#96966b","#969696","#9696c0","#96c040","#96c06b","#96c096","#96c0c0","#c04040","#c0406b","#c04096","#c040c0","#c06b40","#c06b6b","#c06b96","#c06bc0","#c09640","#c0966b","#c09696","#c096c0","#c0c040","#c0c06b","#c0c096","#c0c0c0"]
rs = [int(clr[1:3], base=16) / 255 for clr in clrs]
gs = [int(clr[3:5], base=16) / 255 for clr in clrs]
bs = [int(clr[5:7], base=16) / 255 for clr in clrs]

clrs = [colorsys.rgb_to_hls(*rgb) for rgb in zip(rs,gs,bs)]
clrs.sort(key=lambda a: a[0])
clrs.sort(key=lambda a: a[2], reverse=True)

sat_group = [*zip(clrs[0:16], clrs[16:32], clrs[32:48], clrs[48:64])]
select = [0+0, 12+0, 4+2, 0+3, 0+1, 12+1, 8+1, 4+1, 0+2, 12+2, 8+2, 8+0, 4+0, 12+3, 8+3, 4+3]
sorted_sg = [sat_group[select[i]] for i in range(len(sat_group))]
clrs = [hls for snuplet in zip(*sorted_sg) for hls in snuplet]

clrs = [tuple(round(e*255) for e in colorsys.hls_to_rgb(*hls)) for hls in clrs]
clrs = [clr for clr in clrs if not all(c == clr[0] for c in clr)]
clrs = [''.join(hex(c)[2:] for c in rgb) for rgb in clrs]
print(clrs)