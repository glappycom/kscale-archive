from solid2 import* 
from solid2.extensions.bosl2 import *

from common import RadialHoles

from collections import namedtuple

## Thickness of the face of the motor 
facethick = 15 
basethick = 15
height = 120
width = 220
base = 110




def RS01_cutout(thick=10):
    return RadialHoles(dia=73, count=9, hole=3.5, thick=thick, angle=0) + RadialHoles(0, 1, 44, thick=thick, angle=0)


def RS04_cutout(thick=10):
    return RadialHoles(106, 10, 5, thick, 0) + RadialHoles(0, 1, 52, thick, 0)


def stand(cutout=RS01_cutout, head_dia=100):
    front_face = hull()(
        cyl(d=head_dia, h=facethick),
        xcopies(width-2*basethick)(
            cyl(r=basethick, h=facethick)
        ).back(height)
    ) - cutout(facethick)

    rval = front_face.rotate(-90,0,0).up(height+basethick/2).fwd(base/2-facethick/2)

    rval += cuboid([width, base, basethick])

    rval -= xcopies(180)(
        ycopies(50)(
            cyl(d=6, h=basethick)
        ).fwd(10)
    )

    return rval 


if __name__ == "__main__":
    rval = stand(RS01_cutout).fwd(115)
    # rval += stand(RS04_cutout, 135)

    rval = rval.rotate(90).right(10)
    # rval = RadialHoles()

    print ("$fn=50;")
    print (rval.as_scad())
