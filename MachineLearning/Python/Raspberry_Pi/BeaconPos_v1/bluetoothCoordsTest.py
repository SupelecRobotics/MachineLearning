import serial
import cv2

def drawCircles(table, points):
    if(len(points) == 0):
        return table
    tableWithCircles = table.copy()
    for i in range(0, len(points)):
        cv2.circle(tableWithCircles,(int(points[i][0]),int(points[i][1])),5,(255,255,255),2)
    return tableWithCircles

def getPoints(msg):
    if(len(msg) == 11):
        cutMsg = msg[1:len(msg)-2]
        print cutMsg
        x,y = int(cutMsg[0:4]),int(cutMsg[4:])
        return x,y
    else:
        return None

ser = serial.Serial(port=10,baudrate=38400,timeout = 5 )

print ser.isOpen()

table = cv2.imread('schema_table2.png')


while(True):
    data_left = ser.inWaiting()
    if(data_left != 0):
        print data_left
        print getPoints(ser.read(data_left))

ser.close()
