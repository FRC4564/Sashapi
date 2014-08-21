import PiIO
import time

try:
    sp1 = PiIO.Spike(1)
    sp2 = PiIO.Spike(2)
    sp3 = PiIO.Spike(3)
    sw1 = PiIO.Switch(1)
    sw2 = PiIO.Switch(2)
    sw3 = PiIO.Switch(3)
    sw4 = PiIO.Switch(4)

    cycle = 0  #0=stop, 1=fwd, 2=rev
    
    while sw4.open():
	# sw1 is upper limit - will fire right canon
	if sw1.closed():
	    sp2.fwd()
	else:
	    sp2.stop()
	# sw2 is lower limit - will fire left canon
	if sw2.closed():
            sp3.fwd()
        else:
            sp3.stop()
        # sw3 is the compressor - it is closed when pressure is low
	if sw3.closed():
	    sp1.fwd()
	else:
            sp1.stop() 
        print sw1.closed(),sw2.closed(),sw3.closed(),sw4.closed()

except:
    PiIO.close()
    raise

finally:
# Release IO lines
    PiIO.close()
