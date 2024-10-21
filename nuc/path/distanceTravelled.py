import math

def distTravelled(vmax, a, d, t1):
    # v = a * t
    # b = math.sqrt(a^2-vmax^2)
    triangle_base = vmax/a
    rectangle_base = d/vmax - triangle_base
    if triangle_base*vmax >= d:
        v = math.sqrt(d*a)
        triangle_base = v/a
        if t1 <= triangle_base:
            return a*t1**2/2
        if t1 > triangle_base and t1 <= v*triangle_base:
            return v*triangle_base/2 + (vmax+(vmax-a*(t1-triangle_base)))*(t1-triangle_base)/2
        return d
    else:
        rectangle_base = d/vmax - triangle_base
        if t1 <= triangle_base:
            return a*t1**2/2
        if t1 > triangle_base and t1 < triangle_base+rectangle_base:
            return vmax*triangle_base/2 + vmax*(t1-triangle_base)
        if t1 >= triangle_base + rectangle_base and t1 <= triangle_base*2+rectangle_base:
            return vmax*triangle_base/2 + vmax*rectangle_base + (vmax+(vmax-a*(t1-triangle_base-rectangle_base)))*(t1-triangle_base-rectangle_base)/2
        return d
