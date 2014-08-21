"""
Methods to work specifcally with the custom made board that attaches atop the
RPi to provide 4 Spike Relays outputs and 6 input switches.  

Example usage  (GPIO requires you run code with 'sudo python'):
    import io

    try:
        winch = io.Spike(1)
        upperLimit = io.Switch(1)
        lowerLimit = io.Switch(2)
        
        # Run winch to upper limit
        while upperLimit.Open():
            winch.fwd()
        winch.stop()
        
        # Run winch to lower limit
        while lowerLimit.Open():
            winch.rev()
        winch.stop()
        
    except:
        raise

    finally:
    # Release IO lines
    io.close()

"""

import RPi.GPIO as IO

# INITIALIZE HARDWARE
 
# Setup GPIO to map to physical board pin numbers (Model B V2)
IO.setmode(IO.BOARD)

# Setup output pins for Spike relays
SPIKES_FWD=[5,11,15,21]
SPIKES_REV=[3, 7,13,19]
for pin in SPIKES_FWD:
    IO.setup(pin,IO.OUT)
    IO.output(pin,False)
for pin in SPIKES_REV:
    IO.setup(pin,IO.OUT)
    IO.output(pin,False)
    
# Setup input pins for Switches
SWITCHES=[12,16,18,22,24,26]
for pin in SWITCHES:
    # Inputs will be held high (1) unless shorted to ground (0)
    IO.setup(pin,IO.IN,pull_up_down=IO.PUD_UP)


def close():
    IO.cleanup()



# CLASSES

# There are 4 spike relays, each capable of forward, reverse and off states.
#
class Spike():

    # Init a Spike relay.  Pass number 1 to 4.
    # Reverse relay control, reverses polarity of motor output.
    def __init__(self,spike):
        if spike >= 1 and spike <= 4:
            self.pinFwd = SPIKES_FWD[spike-1]
            self.pinRev = SPIKES_REV[spike-1]
        else:
            raise ValueError("Spike relay number must be between 1 and 4")
        
    def stop(self):
        IO.output(self.pinFwd,False)
        IO.output(self.pinRev,False)
           
    def fwd(self):
        IO.output(self.pinFwd,True)
        IO.output(self.pinRev,False)
        
    def rev(self):
        IO.output(self.pinFwd,False)
        IO.output(self.pinRev,True)
        
    def off(self):
        self.stop()

    def on(self):
        self.fwd()



# Switch class provides open/closed state for switch inputs.
# Pass switch number to  either the 'open' or 'closed' method to get logical state.
#
class Switch():

    # Init a switch for input.  Pass #1 to 6.
    def __init__(self,switch):
        if switch >= 1 and switch <= 6:
            self.pin = SWITCHES[switch-1]
        else:
            raise ValueError("Switch number must be between 1 and 6")

    def open(self):
        if IO.input(self.pin) == 1:
            return True
        else:
            return False

    def closed(self):
        if IO.input(self.pin) == 0:
            return True
        else:
            return False


"""
import time
sp1=Spike(1)   
sp2=Spike(2)
sp3=Spike(3)
sp4=Spike(4)
sw6=Switch(6)

try:
    while sw6.open():
        sp1.fwd()
        print sw6.open()
        time.sleep(1)
        sp1.rev()
        print sw6.open()
        time.sleep(1)
        sp1.stop()
        print sw6.open()
        time.sleep(1)

except:
    raise

finally:
    sp1.off()
    sp2.off()
    sp3.off()
    sp4.off()
    IO.cleanup()
"""
    
    
