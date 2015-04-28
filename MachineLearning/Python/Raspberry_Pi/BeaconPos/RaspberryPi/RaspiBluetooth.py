import serial
import RPi.GPIO as GPIO
import time

def convertNbTo4Char(nb):
    strNb = str(int(round(nb)))

    l = len(strNb)
    if(l < 4):
        zeros = ""
        for i in range(l, 4):
            zeros += "0"
        strNb = zeros + strNb

    return strNb

def sendCoordsOfRobot(blueTSer, robType, coords):
    if(coords is not None):
         for i in range(0, len(coords)):
            msg = objectType + str(i) + convertNbTo4Char(coords[i][0]) + convertNbTo4Char(coords[i][1]) + "\r\n"
            print msg
            blueTSer.write(msg)

def sendCommand(btSer,msg):
    btSer.write(msg)
    time.sleep(1)
    data_left = btSer.inWaiting()
    return btSer.read(data_left)
    

def bluetoothInit():
    pinEN = 18
     
    pause = 1
    blueTSer = serial.Serial( "/dev/ttyAMA0", baudrate=38400,timeout = 5 )
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pinEN, GPIO.OUT)
     
     
    GPIO.output(pinEN, True)
     
    print "Configuration"
    print sendCommand(blueTSer, "AT+RESET\r\n")
    print "RESET sent"
    print sendCommand(blueTSer, "AT+ORGL\r\n")
    print "ORGL sent"
    print sendCommand(blueTSer, "AT+RMAAD\r\n")
    print "RMAAD sent"
    print sendCommand(blueTSer, "AT+NAME=sumocam2\r\n")
    print "NAME sent"
    print sendCommand(blueTSer, "AT+INIT\r\n")
    print "INIT sent"
    print sendCommand(blueTSer, "AT+INQ\r\n")
    print "INQ sent"

    GPIO.output(pinEN, False)

    ans = sendCommand(blueTSer, 'AT+STATE?\r\n')

    print ans

    return blueTSer
