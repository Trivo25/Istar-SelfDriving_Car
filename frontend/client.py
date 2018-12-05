#
# name:  frontend/start.py
# Python 3.6
# Description:
#   client side (frontend) - receives and sends data to the server
#   

import socket
import numpy as np
import cv2
import base64
import time
import sys
import thread as _thread
import RPi.GPIO as GPIO


#>>> DEFINING CLIENT SENSOR AND CAMERA <<<
vidCap = cv2.VideoCapture(0);
vidCap.set(3,400);
vidCap.set(4,400);

#>>> DEFINING DEFAULT ADRESSES AND PORT <<<
IP_Adress_Server = "192.168.178.32"#socket.gethostname()
PORT_server = 5555

IP_Adress_Client = "192.168.178.37"#socket.gethostname()#"127.0.0.1"
PORT_Client = 5544

#>>> DEFINING SERVER-SIDE SETTINGS <<<
buffer_size = 95000


#>>> DEFINING SERVER-SIDE COMMANDS (OPCODE) <<<
cmd_turnLeft = b'0x1a1'
cmd_turnRight = b'0x2a2'
cmd_onTrack = b'0x3a3'

#>>> DEFINING TEST VARIABLES <<<
global dataByte
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
GPIO.setup(13, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

def sender():
    global senderSocket
    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    senderSocket.connect((IP_Adress_Server, PORT_server))
    print(time.strftime("%X ", time.gmtime()) +" Connected to server!")
    _thread.start_new_thread(receiver,())
    cameraStream()


def receiver():
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiverSocket.bind((IP_Adress_Client, PORT_Client))
    receiverSocket.listen(1)


    print(time.strftime("%X ", time.gmtime()) + " Waiting for server..")
    receiverCon, addr = receiverSocket.accept()

    print(time.strftime("%X ", time.gmtime()) + " Connection accepted; " + str(addr))
    while True:
            time.sleep(1/60)
            data = receiverCon.recv(buffer_size)


            if data == b'':
                return
            elif data == cmd_turnLeft:
                print("TURNING LEFT")
                GPIO.output(11, GPIO.LOW)
                GPIO.output(13, GPIO.HIGH)


            elif data == cmd_turnRight:
                print("TURNING RIGHT")
                GPIO.output(13, GPIO.LOW)
                GPIO.output(11, GPIO.HIGH)



            elif data == cmd_onTrack:
                print("ON TRACK")
                GPIO.output(11, GPIO.HIGH)
                GPIO.output(13, GPIO.HIGH)



    receiverCon.close()
    receiverSocket.close()


def cameraStream():
    global senderSocket
    print(time.strftime("%X ", time.gmtime()) + " Sending stream to " + str(IP_Adress_Server) + str(PORT_server))
    while True:
        time.sleep(1/60)

        grabbed, frame = vidCap.read()
        crop_img = frame[100:300, 100:300]
        retval, buffer = cv2.imencode('.jpg', crop_img)
        jpg_as_text = base64.b64encode(buffer)
        senderSocket.send(jpg_as_text)






sender()
#cameraStream()
