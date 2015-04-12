import serial
import RPi.GPIO as GPIO
import time

def convertNbTo4Char(nb):
    strNb = str(round(nb))

    l = len(strNb)
    if(l < 4):
        zeros = ""
        for i in range(l, 4):
            zeros += "0"
        strNb = zeros + strNb

    return strNb

def sendCoordsOfObject(blueTSer, objectType, coords):
     for i in range(0, len(coords)):
        msg = objectType + str(i) + convertNbTo4Char(coords[i][0]) + convertNbTo4Char(coords[i][1])
        blueTSer.write(msg)

def sendCoords(blueTSer, tableCoords):
    sendCoordsOfObject(blueTSer, 'c', tableCoords["cylindersYellow"])
    sendCoordsOfObject(blueTSer, 'd', tableCoords["cylindersGreen"])
    sendCoordsOfObject(blueTSer, 't', tableCoords["tennisBall"])
    sendCoordsOfObject(blueTSer, 'r', tableCoords["robots"])
    

def bluetoothInit():
    pinEN = 18
     
    pause = 1
    BlueTSer = serial.Serial( "/dev/ttyAMA0", baudrate=38400,timeout = 5 )
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pinEN, GPIO.OUT)
     
     
    GPIO.output(pinEN, True)
    time.sleep(pause)
     
    print "Configuration"
    BlueTSer.write("AT\r\n")
    time.sleep(pause)
    BlueTSer.write("AT+ORGL\r\n")
    print "ORGL sent"
    time.sleep(pause)
    BlueTSer.write("AT+RMAAD\r\n")
    print "RMAAD sent"
    time.sleep(pause)
    BlueTSer.write("AT+PSWD=6666\r\n")
    print "PSWD sent"
    time.sleep(pause)
    BlueTSer.write("AT+ROLE=0\r\n")
    print "ROLE sent"
    time.sleep(pause)
     
    BlueTSer.write("AT\r\n")
    BlueTSer.write("AT+RESET\r\n")
    print "RESET sent"
     
    print "PinEN false"
    GPIO.output(pinEN, False)
     
    time.sleep(15)     
    
    print "Reading Data Configuration wait 10sec"
    time.sleep(10)
    data_left = BlueTSer.inWaiting()
    sdata = BlueTSer.read(data_left)
    print "Configuration finished"
    print sdata

    return BlueTSer
