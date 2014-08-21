import PiIO
import maestro
import xbox
import drive
import time

# CONSTANTS
LEFT_MOTORS = 1
RIGHT_MOTORS = 0
THROWER = 2
CAM = 3
THROWER_MAX = 9200
THROWER_STOP = 6000
THROWER_RANGE = 3200
CAM_FWD = 2800
CAM_REV = 9000
CAM_STOP = 6000

# VARIABLES
speedToggle = 2 # 2 = Full Speed; 1 = Slow Mode; 0 = Driving Disabled 
currentThrower = 7600 # Initial thrower set to 50% power

# BOOLEANS
isStarted = False # Press Start to enable the robot
compressorEnabled = False
PressedY = False # Allows Y to be called on rising edge
throwerEnabled = False
pressedA = False # Allows A to be called on rising edge
pressedBack = False # Allows Back to be called on rising edge


j = xbox.Joystick()
motors = maestro.Controller()
drive = drive.DriveTrain(motors, LEFT_MOTORS, RIGHT_MOTORS)

try:
    winch      = PiIO.Spike(1)
    compressor = PiIO.Spike(2)
    cannonl    = PiIO.Spike(3)
    cannonr    = PiIO.Spike(4)
    
    upperLimit = PiIO.Switch(1)
    lowerLimit = PiIO.Switch(2)
    camLimit   = PiIO.Switch(3)
    pressureSw = PiIO.Switch(4)
    
except:
    raise
# **MAINE LOOP**

print "Sasha rises!"
print "Press Start to enable."
try:
    while True:

        if isStarted:

            ### Drive Command ###
            if speedToggle != 0:
                if speedToggle == 2:
                    if abs(j.leftX()) <= .10 and abs(j.leftY()) <= .21:
                        drive.drive(0, 0)
                    else:
                        drive.drive(j.leftX(), j.leftY())
                else:
                    if abs(j.leftX()) <= .15 and abs(j.leftY()) <= .23:
                        drive.drive(0, 0)
                    else:
                        drive.drive(j.leftX(), j.leftY() * .4)    
            else:
                drive.drive(0, 0)

            ### Speed toggle & Drive Control ###
            if j.Back():
                if pressedBack == False:
                    if j.X():
                        #print "FULL SPEED AHEAD!"
                        pressedBack = True
                        speedToggle = 2
                    elif j.B():
                        speedToggle = 1
                        #print "Slow Driving Mode"
                        pressedBack = True
                    else:
                        speedToggle = 0
                        #print "Driving Disabled"
            else:
                pressedBack = False
            
                
            ### Raise and Lower Frisbee Thrower ###
            if j.dpadUp() and upperLimit.open():
                winch.rev()
            elif j.dpadDown() and lowerLimit.open():
                winch.fwd()
            else:
                winch.stop()
                
            ### Speed Of Thrower Motor ###
            if throwerEnabled == False and speedToggle == 2:
                if j.leftTrigger() >= .20 and j.leftTrigger() < .40:
                    motors.setTarget(THROWER, int(THROWER_STOP + (THROWER_RANGE * .50)))
                    currentThrower = int(THROWER_STOP + (THROWER_RANGE * .50))
                    #print "Thrower: 50%"
                elif j.leftTrigger() >= .40 and j.leftTrigger() < .60:
                    motors.setTarget(THROWER, int(THROWER_STOP + (THROWER_RANGE * .65)))
                    currentThrower = int(THROWER_STOP + (THROWER_RANGE * .65))
                    #print "Thrower: 65%"
                elif j.leftTrigger() >= .60 and j.leftTrigger() < .80:
                    motors.setTarget(THROWER, int(THROWER_STOP + (THROWER_RANGE * .80)))
                    currentThrower = int(THROWER_STOP + (THROWER_RANGE * .80))
                    #print "Thrower: 80%"
                elif j.leftTrigger() >= .80:
                    motors.setTarget(THROWER, THROWER_MAX)
                    currentThrower = THROWER_MAX
                    #print "Thrower: MAX POWER!!!"
                else:
                    motors.setTarget(THROWER, THROWER_STOP)

            ### Lock and Recall Thrower Speed ###    
            if j.A():
                if pressedA == False:
                    if throwerEnabled == False:
                        motors.setTarget(THROWER, currentThrower)
                        throwerEnabled = True
                        #print "throwerEnabled = True"
                    else:
                        motors.setTarget(THROWER, THROWER_STOP)
                        throwerEnabled = False
                        #print "throwerEnabled = False"
                    pressedA = True
            else:
                pressedA = False
                
            ### Launch frisbee ###
            if j.rightTrigger() > 0:
                if j.B():
                    motors.setTarget(CAM, CAM_REV)
                else:
                    if throwerEnabled:
                        motors.setTarget(CAM, CAM_FWD)
            elif camLimit.closed():
                motors.setTarget(CAM, CAM_STOP)

            ### Compressor ###
            if j.Y():
                if pressedY == False:
                    if compressorEnabled == False:
                        compressorEnabled = True
                        #print "Compressor Enabled"
                    else:
                        compressorEnabled = False
                        #print "Compressor Disabled"
                    pressedY = True
            else:
                pressedY = False
                
            if compressorEnabled == False or pressureSw.open():
                compressor.stop()
                compressorEnabled = False
                #print "Compressor Stopped"
            else:
                compressor.fwd()
                #print "Compressor Started"
                        
            ### T-Shirt Cannons ###
            if j.rightBumper():
                 cannonr.fwd()
            else:
                cannonr.stop()

            if j.leftBumper():
                cannonl.fwd()
            else:
                cannonl.stop()
                
        ### Robot Start Boolean ###
        if j.Start():
            isStarted = True
            #print "Start"

        # Time interval before next loop begins.
        time.sleep(0.033)
except:
        winch.stop()
        motors.setTarget(CAM, CAM_STOP)
        motors.setTarget(THROWER, THROWER_STOP)
        compressor.stop()
        drive.close()
        motors.close()
        j.close()
        PiIO.close()
        raise
