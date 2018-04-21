# This is the message receiver

import os
from socket import *

host = ""
port = 13000
buf = 1024
address = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)

UDPSock.bind(address)
print("Receiving messages. Please wait...")

while True:
    (data, address) = UDPSock.recvfrom(buf)
    data2 = data.decode('utf-8')
    print("Received message: " + data2)
    if data == "exit":
        break

UDPSock.close()
os._exit(0)
