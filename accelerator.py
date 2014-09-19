import time
import mraa
import pyupm_lsm303

CAPTURE_TIME = 1

class IntContainer: 
    i = 0

c = IntContainer()
l = pyupm_lsm303.LSM303( 0 )
def toggle(args):
  print "CLICK"
  c.i += 1
  if c.i % 2 == 1:
    capture()

btn = mraa.Gpio( 6 )
btn.dir( mraa.DIR_IN )
btn.isr( mraa.EDGE_BOTH, toggle, toggle )

def capture():
    start = time.time()
    while time.time() - start < CAPTURE_TIME:
        t = l.getAcceleration()
        x = l.getAccelX()
        y = l.getAccelY()
        z = l.getAccelZ()
        print "%03d %03d %03d" % ( x, y, z ) 
        time.sleep( .1 )

while True:
    print "."
    time.sleep( .2 )
