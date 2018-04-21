# This is the message sender
import os
from socket import *


def keyGenerator():
    print("Hola")


if __name__ == '__main__':

    # Set the ip from the receiver
    host = "0.0.0.0"
    port = 13000
    address = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)

    while True:
        data = input("Enter message to sent or type 'exit': ")
        UDPSock.sendto(data, address)
        if data == "exit":
            break

    UDPSock.close()
    os._exit(0)