import serial
import numpy as np
import cv2

BUF_SIZE = 128

ser = serial.Serial(port=9,baudrate=1382400,timeout = 5 )

print ser.isOpen()

end = False
msg = ''

prevLen = 0

ser.read(ser.inWaiting())

while(not end):
    data_left = ser.inWaiting()
    if(data_left > 0):
        if(data_left >= BUF_SIZE):
            newMsg = ser.read(BUF_SIZE)
        else:
            newMsg = ser.read(data_left)

        if(newMsg.find('#END') != -1):
            end = True
        
        msg = msg + newMsg
        l = len(msg)
        if(l - prevLen > 10000):
            print str(l) + '/2853324'
            prevLen = l

cutMsg = msg[:-6]
pic = np.array(eval(cutMsg), dtype=np.uint8)

decPic = cv2.imdecode(pic,cv2.CV_LOAD_IMAGE_COLOR)
cv2.imwrite('Pic.png',decPic)
    

ser.close()
cv2.destroyAllWindows()
