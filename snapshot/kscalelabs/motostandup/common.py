from solid2 import* 
from solid2.extensions.bosl2 import *


def RadialHoles(dia=80, count=9, hole=3, thick=10, angle=0):
    return zrot_copies(n=count)(
        cyl(d=hole, h=thick+hole, rounding=hole/2).fwd(dia/2)
    ).rotate(angle)

if __name__ == "__main__":
    rval = cube(5)

    print ("$fn=50;")
    print (rval.as_scad())