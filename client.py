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
    host = "10.48.219.167"
    port = 13000
    address = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)

    while True:

        data = input("Enter message to sent or type 'exit': ")
        if data == "exit":
            break
        data = compress(data)

        listToString = ""
        for i, item in enumerate(data):
            if i:
                listToString = listToString + ','
            listToString = listToString + str(item)

        data2 = bytes(listToString, 'utf-8')
        UDPSock.sendto(data2, address)

    UDPSock.close()
    os._exit(0)


## https://rosettacode.org/wiki/LZW_compression#Python