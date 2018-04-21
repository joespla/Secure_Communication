# This is the message sender
import os
from socket import *


def keyGenerator():
    print("Hola")


if __name__ == '__main__':

    # Set the ip from the receiver
    host = "192.168.100.16"
    port = 13000
    address = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)

    while True:
        data = input("Enter message to sent or type 'exit': ")
        data2 = bytes(data, 'utf-8')
        UDPSock.sendto(data2, address)
        if data == "exit":
            break

    UDPSock.close()
    os._exit(0)