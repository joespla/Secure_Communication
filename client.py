# This is the message sender
import os
from socket import *


#LWZ Compression
def compress(uncompressed):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dict_size = 256

    dictionary = {chr(i): i for i in range(dict_size)}

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result


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