from solid2 import* 
from solid2.extensions.bosl2 import *

from collections import namedtuple
from common import RadialHoles

from rotor import rotor_robstride04

rval = rotor_robstride04()

print ("$fn=50;")
print (rval.as_scad())
