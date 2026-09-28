from solid2 import* 
from solid2.extensions.bosl2 import *

from collections import namedtuple
from common import RadialHoles

rim_dia = 255
rim_h = 2
ring_dia = 250
ring_h = 8

def ring(rval, ring_dia=250, ring_h=10, rim_extra=5, rim_h=3): 
    rim_dia = ring_dia+rim_extra

    rval = rval.up(rim_h)
    rval += cylinder(d=rim_dia, h=rim_h)

    rval = rval.up(ring_h)
    rval += cylinder(d=ring_dia, h=ring_h)

    rval = rval.up(rim_h)
    rval += cylinder(d=rim_dia, h=rim_h)


    ## Score line

    rval -= cylinder(d=2, h=rim_dia).rotate(0,90,0).rotate(0,0,60)
    rval -= cylinder(d=2, h=rim_dia).rotate(0,90,0).rotate(0,0,60).up(ring_h+2*rim_h)


    ## Rope hole. 

    rval -= cyl(d=5, h=rim_dia).rotate(0,90,0).rotate(0,0,0).up(ring_h/2+rim_h)

    ## Rope ring

    rval -= RadialHoles(
        dia=ring_dia-2,
        count=13, 
        hole=5,
        thick=ring_h,
        angle=0
    )

    ## Material Savings. .

    rval -= RadialHoles(
        dia=ring_dia*0.4,
        count=6, 
        hole=ring_dia*0.15,
        thick=4*ring_h,
        angle=0
    )


    rval -= RadialHoles(
        dia=ring_dia*0.69,
        count=6, 
        hole=ring_dia*0.15,
        thick=4*ring_h,
        angle=30
    )

    rval -= RadialHoles(
        dia=ring_dia*0.8,
        count=6, 
        hole=ring_dia*0.15,
        thick=4*ring_h,
        angle=0
    )

    return rval 

## Stem Holes


def rotor_robstride01():
        
    stem_dia = 40
    stem_h = 30

    rval = cylinder(d=stem_dia, h=stem_h)

    rval = ring(rval) 

    rval -= RadialHoles(
        dia=24,
        count=6, 
        hole=4.6,
        thick=200,
        angle=0
    )

    rval -= RadialHoles(
        dia=24,
        count=3, 
        hole=5.5,
        thick=200,
        angle=30
    )

    return rval

def rotor_robstride04():
        
    stem_dia = 50
    stem_h = 30

    rval = cylinder(d=stem_dia, h=stem_h)

    rval = ring(rval) 

    rval -= RadialHoles(
        dia=32,
        count=12, 
        hole=5.6,
        thick=200,
        angle=0
    )

    rval -= RadialHoles(
        dia=32,
        count=3, 
        hole=6,
        thick=200,
    )

    return rval 

if __name__ == "__main__":
    rval = rotor_robstride01()

    print ("$fn=50;")
    print (rval.as_scad())
