import numpy as np
import pya

def CircularSerpentine(l_inner: float, l_outer: float, thick: float, pitch: float, n: int, theta: float, res=3, rot=0) -> pya.DPath:
    print(f"{l_inner + l_outer + (n+1)*pitch} um")

    pts = list()
    pts += [pya.DPoint(0, 0), pya.DPoint(0, l_inner)]

    # convert to radians
    theta = (theta)*np.pi/180

    dtheta = theta/(2*res)
    for p in range(1, res):
        x = l_inner*np.cos(p*dtheta + np.pi/2)
        y = l_inner*np.sin(p*dtheta + np.pi/2)
        pts.append(pya.DPoint(x, y))

    for i in range(1, n+1):
        dtheta = ((-1)**i)*theta/((i+2)*res)
        if i % 2 == 0:
            shift = np.pi/2 - theta/2
        else:
            shift = theta/2 + np.pi/2

        for p in range(1, (i+2)*res):
            ring_r = (l_inner + i*pitch)
            x = ring_r*np.cos(p*dtheta + shift)
            y = ring_r*np.sin(p*dtheta + shift)
            pts.append(pya.DPoint(x, y))

    if n % 2 == 0:
        dtheta = -1*theta/(2*res*int(n/2))
        shift = theta/2 + np.pi/2
    else:
        dtheta = theta/(2*res*int(n/2))
        shift = np.pi/2 - theta/2

    for p in range(1, res*int(n/2)+1):
        ring_r = (l_inner + (n+1)*pitch)
        x = ring_r*np.cos(p*dtheta + shift)
        y = ring_r*np.sin(p*dtheta + shift)
        pts.append(pya.DPoint(x, y))

    pts.append(pya.DPoint(0, l_outer +
                          l_inner + pitch*(n + 1)))

    tt = pya.DCplxTrans(1,  rot, False, 0, 0)
    return tt*pya.DPath(pts, thick)


layout = pya.Layout()
si = layout.create_cell("si")
l = layout.layer(1, 0)

l_inner = 30
l_outer = 7
thick = 2
pitch = thick + 1
n = 35
theta = 89
res = 4

cs1 = CircularSerpentine(l_inner=l_inner,
                         l_outer=l_outer,
                         thick=thick,
                         pitch=pitch,
                         n=n,
                         theta=theta,
                         res=res,
                         rot=0)

cs2 = CircularSerpentine(l_inner=l_inner,
                         l_outer=l_outer,
                         thick=thick,
                         pitch=pitch,
                         n=n,
                         theta=theta,
                         res=res,
                         rot=90)

cs3 = CircularSerpentine(l_inner=l_inner,
                         l_outer=l_outer,
                         thick=thick,
                         pitch=pitch,
                         n=n,
                         theta=theta,
                         res=res,
                         rot=180)

cs4 = CircularSerpentine(l_inner=l_inner,
                         l_outer=l_outer,
                         thick=thick,
                         pitch=pitch,
                         n=n,
                         theta=theta,
                         res=res,
                         rot=270)

si.shapes(l).insert(cs1)
si.shapes(l).insert(cs2)
si.shapes(l).insert(cs3)
si.shapes(l).insert(cs4)
layout.write("./great.gds")
