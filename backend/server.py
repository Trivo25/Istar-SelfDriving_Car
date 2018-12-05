#
# name: backend/start.py
# Python 3.6
# Description:
#   server side (backend) - all heavy lifting happens here
#
#


import socket
import time
import sys
import base64
import numpy as np
import cv2
import _thread


#>>> DEFINING DEFAULT ADRESSES AND PORT <<<
IP_Adress_Server = "192.168.178.32" #socket.gethostname()
PORT_server = 5555

IP_Adress_Client = "192.168.178.49"
PORT_Client = 5544

#>>> DEFINING SERVER-SIDE SETTINGS <<<
buffer_size = 95000
tickRate = 1/60

#>>> DEFINING SERVER-SIDE COMMANDS (OPCODE) <<<
cmd_turnLeft = b'0x1a1'
cmd_turnRight = b'0x2a2'
cmd_onTrack = b'0x3a3'

#>>> DEFINING TEST VARIABLES <<<
dataByte = b''


def sender():
    global senderSocket
    senderSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    senderSocket.connect((IP_Adress_Client, PORT_Client))
    print(time.strftime("%X ", time.gmtime()) + " Connected to client!")




def receiver():
    global dataByte
    receiverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiverSocket.bind((IP_Adress_Server, PORT_server))
    receiverSocket.listen(1)


    print(time.strftime("%X ", time.gmtime()) + " Waiting for client..")
    conn, addr = receiverSocket.accept()
    print(time.strftime("%X ", time.gmtime()) + " Connection accepted; " + str(addr))
    _thread.start_new_thread(sender,())
    _thread.start_new_thread(laneControl,())
    while True:

            time.sleep(tickRate)
            data = conn.recv(buffer_size)

            if (sys.getsizeof(data) > 500):
                dataByte = data







def laneControl():
    global dataByte
    global senderSocket
    time.sleep(0.8)
    print(time.strftime("%X ", time.gmtime()) + " Receiving video stream from " + str(IP_Adress_Client) + str(PORT_Client))
    while True:
        try:

            time.sleep(tickRate)
            imgString = dataByte.decode()
            img = base64.b64decode(imgString)
            npimg = np.fromstring(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)

            #lane detection


            #crop_img = source[100:300, 100:300]
            crop_img = source
            gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)


            blur = cv2.GaussianBlur(gray,(5,5),0)

            ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)

            _,contours,hierarchy  = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

            if len(contours) > 0:

                c = max(contours, key=cv2.contourArea)

                M = cv2.moments(c)

                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])

                cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
                cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
                cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)


                if cx >= 120:
                    print ("Turn Right!")
                    senderSocket.send(cmd_turnRight)

                if cx < 120 and cx > 50:
                    print ("On Track!")
                    senderSocket.send(cmd_onTrack)

                if cx <= 50:
                    print ("Turn Left!")
                    senderSocket.send(cmd_turnLeft)


        # lane detection end




            #cv2.imshow("Stream", source)
            cv2.imshow("Stream", crop_img)
            cv2.waitKey(1)

        except cv2.error as e:
            print("Error, trying to restart function")
            #laneControl()


receiver()
