#
# name:  frontend/start.py
# Python 3.6
# Description:
#   decoding of .jpg files (images/frames) and send them
#   over a webserver (webpy) to the PC to do the heavy lifitng
#

import socket
import numpy as np
import cv2
import base64
import time
import sys
import _thread

vidCap = cv2.VideoCapture(-1);

IP_Adress_Server = "127.0.0.1"
PORT_server = 5555

IP_Adress_Client = "127.0.0.1"
PORT_Client = 5544
buffer_size = 95000
tickRate = 1/30


def sender():
    global senderSock
    senderSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    senderSock.connect((IP_Adress_Server, PORT_server))
    print(time.strftime("%X ", time.gmtime()) +" Connected to server!")
    _thread.start_new_thread(receiver,())
    #receiver()
    while True:
        message = input()
        senderSock.send(str.encode(message))

def receiver():
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiverSocket.bind((IP_Adress_Client, PORT_Client))
    receiverSocket.listen(2)


    print(time.strftime("%X ", time.gmtime()) + " Waiting for server..")
    receiverCon, addr = receiverSocket.accept()

    print(time.strftime("%X ", time.gmtime()) + " Connection accepted; " + str(addr))
    while True:
            time.sleep(tickRate)
            data = receiverCon.recv(buffer_size)

            print (time.strftime("%X ", time.gmtime()) + " RECEIVED Message: " + str(data) + " " , addr)
            #print(str(data))


    receiverCon.close()
    receiverSocket.close()


def cameraStream():
    global clientSock
    while True:

        time.sleep(tickRate)
        #Message = input("Enter your message: ")
        grabbed, frame = vidCap.read()  # grab the current frame
        frame = cv2.resize(frame, (400, 400))  # resize the frame
        retval, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        #print(sys.getsizeof(jpg_as_text))
        print("Sending camera stream to " + IP_Adress_Server + str(PORT_server) )
        #str.encode(str)
        senderSock.send(jpg_as_text)


    senderSock.close()
    senderSock.shutdown()




sender()
receiver()
#cameraStream()
