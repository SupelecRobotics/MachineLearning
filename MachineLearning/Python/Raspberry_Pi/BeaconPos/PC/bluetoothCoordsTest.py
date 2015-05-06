import serial
import thread
import cv2
import time

TABLE_W = 2000
TABLE_H = 3000

def drawCirclesAndText(table, point):
    if(point is None or len(point) == 0):
        return table
    tableWithCircles = table.copy()
    h,w = tableWithCircles.shape[:2]

    x = int(point[0]*w/TABLE_W)
    y = int(point[1]*h/TABLE_H)
    cv2.circle(tableWithCircles,(x,y),5,(255,255,255),2)
    cv2.putText(tableWithCircles, str(int(point[0])) + ' ' + str(int(point[1])), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    
    return tableWithCircles

def getPoints(msg):
    if(len(msg) == 12):
        cutMsg = msg[2:len(msg)-2]
        x,y = int(cutMsg[0:4]),int(cutMsg[4:])
        return x,y
    else:
        return []

def coordsRec(threadName, params):

    ser = params[0]

    if(ser.inWaiting() == 0):
        params = (params[0],ser.readline())
    

print 'Launching'

ser = serial.Serial(port=9,baudrate=38400,timeout = 1 )

print ser.isOpen()

table = cv2.imread('schema_table2.png')

end = False
point = (0,0)
msg = ''

params = (ser,msg)

thread.start_new_thread(coordsRec, ('Rec', params))

while(not end):
    print 'Reading'
    if(params[1] != ''):
        point = getPoints(msg)
    tableWithCircles = drawCirclesAndText(table, point)
    cv2.imshow('Table', tableWithCircles)

    key = cv2.waitKey(1) & 0xFF
    if(key == ord('q')):
        end = False

cv2.destroyAllWindows()
ser.close()
