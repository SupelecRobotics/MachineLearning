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
    msg = params[1]
    end = params[2]

    while(not end[0]):
        print ser[0].inWaiting()
        if(ser[0].inWaiting() == 0):
            msg[0] = ser[0].readline()

    params[3][0] = True
    

print 'Launching'

ser = [serial.Serial(port=9,baudrate=38400,timeout = 1 )]

print ser[0].isOpen()

table = cv2.imread('schema_table2.png')

end = [False]
point = (0,0)
msg = ['']
threadEnd = [False]

params = (ser,msg,end,threadEnd)

#thread.start_new_thread(coordsRec, ('Rec', params))

cv2.namedWindow('Table')

while(not end[0]):
    print ser[0].inWaiting()
    if(ser[0].inWaiting() == 0):
        msg[0] = ser[0].readline()
    if(params[1][0] != ''):
        point = getPoints(msg)
    tableWithCircles = drawCirclesAndText(table, point)
    cv2.imshow('Table', tableWithCircles)

    key = cv2.waitKey(10) & 0xFF
    if(key == ord('q')):
        end[0] = True

cv2.destroyAllWindows()
while(not threadEnd[0]):
    pass
ser[0].close()
