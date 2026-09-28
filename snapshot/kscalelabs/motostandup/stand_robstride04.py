from solid2 import* 
from solid2.extensions.bosl2 import *


from stand import stand, RS04_cutout

if __name__ == "__main__":
    rval = stand(RS04_cutout, 135)

    print ("$fn=50;")
    print (rval.as_scad())
