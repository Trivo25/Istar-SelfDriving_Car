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
vidCap = cv2.VideoCapture(-1);


IP_Adress = "127.0.0.1"
PORT = 5555

tickRate = 1/30

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSock.connect((IP_Adress, PORT))


while True:
    time.sleep(tickRate)
    #Message = input("Enter your message: ")

    grabbed, frame = vidCap.read()  # grab the current frame
    frame = cv2.resize(frame, (400, 400))  # resize the frame
    retval, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)
    #print(sys.getsizeof(jpg_as_text))
    print("Sending message to " + IP_Adress + str(PORT) )
    #str.encode(str)
    clientSock.send(jpg_as_text)


clientSock.close()
clientSock.shutdown()
