import pya

import re
import numpy as np
from load_yaml import *
from pathlib import Path


def Serpentine(l_inner: float,
               l_outer: float,
               w_meander: float,
               thick: float,
               pitch: float,
               n: int,
               rot=0) -> pya.DPath:
    print(f"{l_inner + l_outer + (n+1)*pitch} um")

    pts = list()
    pts += [pya.DPoint(0, 0), pya.DPoint(0, l_inner),
            pya.DPoint(-w_meander/2, l_inner)]

    for i in range(1, n+1):
        ring_r = (l_inner + i*pitch)

        if i % 2 == 0:
            x1 = w_meander/2
            x2 = -w_meander/2
        else:
            x1 = -w_meander/2
            x2 = w_meander/2

        y = l_inner + i*pitch
        pts += [pya.DPoint(x1, y), pya.DPoint(x2, y)]

    if i % 2 == 0:
        x1 = -w_meander/2
        x2 = 0
    else:
        x1 = w_meander/2
        x2 = 0

    y1 = l_inner + (n)*pitch
    y2 = l_inner + (n+1)*pitch
    pts += [pya.DPoint(x1, y1), pya.DPoint(x2, y2)]

    pts.append(pya.DPoint(0, l_outer +
                          l_inner + pitch*(n + 1)))

    tt = pya.DCplxTrans(1,  rot, False, 0, 0)
    return tt*pya.DPath(pts, thick)


def Circle(radius: float,) -> pya.DPolygon:

    pts = list()
    pts += [pya.DPoint(radius*np.sin(theta), radius*np.cos(theta))
            for theta in np.linspace(0, 2*np.pi, 360)]

    return pya.DPolygon(pts)


def Donut(inner_r: float, outer_r: float, scaling_factor: float) -> pya.DPolygon:
    inner_circle = Circle(inner_r*scaling_factor)
    outer_circle = Circle(outer_r*scaling_factor)

    R0 = pya.Region()
    R1 = pya.Region()
    R0.insert(outer_circle)
    R1.insert(inner_circle)

    return R0 - R1


layout = pya.Layout()
scaling_factor = int(1/layout.dbu)

si = layout.create_cell("si")
l = layout.layer(1, 0)

for t in thetas:    
    s = Serpentine(l_inner=l_inner,
                    l_outer=l_outer,
                    w_meander=w_meander,
                    thick=thick,
                    pitch=pitch,
                    n=n,
                    rot=t)
    si.shapes(l).insert(s)

ped = Circle(l_inner - 10)
inner_r = l_inner + l_outer + (n+1)*pitch
ring = Donut(inner_r, outer_r, scaling_factor)
si.shapes(l).insert(ped)
si.shapes(l).insert(ring)

gds_dir = Path("layouts")

i = 0
for gds in gds_dir.glob("*.gds"):
    existing_i = int(re.findall(r'[0-9]+', gds.name)[0])
    if existing_i >= i:
        i += 1

# sdisk means serpentine disk
gds_path = gds_dir/Path("sdisk{}.gds".format(i))
yml_path = gds_dir/Path("sdisk{}.yml".format(i))

layout.write(str(gds_path))

with open(yml_path, "w") as out:
    yaml.dump(p, out, default_flow_style=False)
