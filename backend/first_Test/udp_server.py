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
import datetime


ts = time.gmtime()
timeStamp = time.strftime("%X ", ts)

UDP_IP_Adress = "127.0.0.1"
UDP_PORT = 5555

buffer_size = 4096


serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_Adress, UDP_PORT))

while True:
    try:
        data, addr = serverSock.recvfrom(buffer_size)
        print (timeStamp + " RECEIVED   " , data.decode(), addr)
    except KeyboardInterrupt:
        raise Exception
        break

serverSock.close()
