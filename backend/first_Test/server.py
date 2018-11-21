#
# name: backend/start.py
# Python 3.6
# Description:
#   enconding of .jpg files (images/frames) and processing them
#
#

#import urllib.request

#with urllib.request.urlopen('http://127.0.0.1:8080/') as response:
#   html = response.read()

#   print(html)


import socket
import time
import sys
import base64
import numpy as np
import cv2
import _thread



IP_Adress_Server = "127.0.0.1"
PORT_server = 5555

IP_Adress_Client = "127.0.0.1"
PORT_Client = 5544

buffer_size = 95000
tickRate = 1/60

dataByte = b''


def sender():

    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    senderSocket.connect((IP_Adress_Client, PORT_Client))
    print(time.strftime("%X ", time.gmtime()) + " Connected to client!")

    while True:
        message = input()
        senderSocket.send(str.encode(message))



def receiver():
    global dataByte
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((IP_Adress_Server, PORT_server))
    serverSocket.listen(1)


    print(time.strftime("%X ", time.gmtime()) + " Waiting for client..")
    conn, addr = serverSocket.accept()
    #_thread.start_new_thread(showImg,())
    print(time.strftime("%X ", time.gmtime()) + " Connection accepted; " + str(addr))
    _thread.start_new_thread(sender,())
    while True:

            time.sleep(tickRate)
            data = conn.recv(buffer_size)

            #if (sys.getsizeof(data) > 35):
            #    print (time.strftime("%X ", time.gmtime()) + " RECEIVED Message size: " + str(sys.getsizeof(data)) + " " , addr)
            #    dataByte = data
            print (time.strftime("%X ", time.gmtime()) + " RECEIVED Message: " + str(data) + " " , addr)


    conn.close()
    serverSocket.close()




def showImg():
    time.sleep(0.5)
    while True:
        try:
            global dataByte

            imgString = dataByte.decode()


            img = base64.b64decode(imgString)
            npimg = np.fromstring(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)
            cv2.imshow("Stream", source)

            cv2.waitKey(1)
            time.sleep(tickRate)

        except cv2.error as e:
            print("Error, trying to restart function")
            _thread.start_new_thread(showImg,())


receiver()
