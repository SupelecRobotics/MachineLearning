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

def sendCoordsOfRobot(blueTSer, robType, coord, lastMsg):
    if(coord is not None):
        msg = '#' + str(robType) + convertNbTo4Char(coord[0]) + convertNbTo4Char(coord[1]) +'\r\n'
        if(msg != lastMsg):
            #print msg + ' ' + str(time.time())
            #print blueTSer.write(msg)
            lastMsg = msg
    return lastMsg

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

    print sendCommand(blueTSer, "AT\r\n")
    
    print sendCommand(blueTSer, "AT+ORGL\r\n")
    print "ORGL sent"
    print sendCommand(blueTSer, "AT+RMAAD\r\n")
    print "RMAAD sent"
    print sendCommand(blueTSer, "AT+NAME=sumocam2\r\n")
    print "NAME sent"
    print sendCommand(blueTSer, "AT+PSWD=6789\r\n")
    print "PSWD sent"
    print sendCommand(blueTSer, "AT+INIT\r\n")
    print "INIT sent"
    print sendCommand(blueTSer, "AT+ROLE=0\r\n")
    print "ROLE sent"
    #print sendCommand(blueTSer, "AT+INQ\r\n")
    #print "INQ sent"

    print sendCommand(blueTSer, 'AT+STATE?\r\n')

    GPIO.output(pinEN, False)

    return blueTSer
