#
# name: backend/start.py
# Python 3.6
# Description:
#   Receiving packets from the raspberry pi frontend
#
#




import socket
import time
import datetime
import sys
import base64
import numpy as np
import cv2
import _thread

ts = time.gmtime()

IP_Adress = "127.0.0.1"
PORT = 5555
buffer_size = 95000
tickRate = 1/60

dataByte = b''
def serverSetup():
    global dataByte
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((IP_Adress, PORT))
    serverSocket.listen(1)

    conn, addr = serverSocket.accept()


    while True:
            time.sleep(tickRate)
            data = conn.recv(buffer_size)
            if (sys.getsizeof(data) > 35):
                print (time.strftime("%X ", time.gmtime()) + " RECEIVED Message size: " + str(sys.getsizeof(data)) + " from " , addr)
                dataByte = data
    conn.close()


    
def showImg():
    time.sleep(2)
    while True:

        global dataByte

        imgString = dataByte.decode()


        img = base64.b64decode(imgString)
        npimg = np.fromstring(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        cv2.imshow("Stream", source)

        cv2.waitKey(1)
        time.sleep(tickRate)



_thread.start_new_thread(showImg,())
serverSetup()

