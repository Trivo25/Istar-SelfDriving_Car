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

vidCap = cv2.VideoCapture("test.mp4");
UDP_IP_Adress = "127.0.0.1"
UDP_PORT = 5555


clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



while True:
    time.sleep(1/2)
    #Message = input("Enter your message: ")
    #if Message == 'exit':
    #    break
    grabbed, frame = vidCap.read()  # grab the current frame
    frame = cv2.resize(frame, (400, 400))  # resize the frame
    retval, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b16encode(buffer)

    Message = jpg_as_text

    clientSock.sendto(Message, (UDP_IP_Adress,UDP_PORT))
