# This is the message sender
import os
from socket import *
from fractions import gcd
from random import randrange
from collections import namedtuple
from math import log
from binascii import hexlify, unhexlify


# LWZ Compression
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


KeyPair = namedtuple('KeyPair', 'public private')
Key = namedtuple('Key', 'exponent modulus')


def encode(msg, pubkey, verbose=False):
    chunksize = int(log(pubkey.modulus, 256))
    outchunk = chunksize + 1
    outfmt = '%%0%dx' % (outchunk * 2,)
    bmsg = msg.encode()
    result = []
    for start in range(0, len(bmsg), chunksize):
        chunk = bmsg[start:start + chunksize]
        chunk += b'\x00' * (chunksize - len(chunk))
        plain = int(hexlify(chunk), 16)
        coded = pow(plain, *pubkey)
        bcoded = unhexlify((outfmt % coded).encode())
        if verbose: print('Encode:', chunksize, chunk, plain, coded, bcoded)
        result.append(bcoded)
    return b''.join(result)


if __name__ == '__main__':

    # Set the ip from the receiver
    host = "10.48.219.167"
    port = 13000
    address = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)

    # Listen just one time to receive public keys
    hostTemp = ""
    portTemp = 13000
    bufTemp = 1024
    addressTemp = (host, port)
    UDPSockTemp = socket(AF_INET, SOCK_DGRAM)

    (dataKeyTemp, addressTemp) = UDPSock.recvfrom(bufTemp)
    data2 = dataKeyTemp.decode('utf-8')

    pubKeyReceived = Key(data2)
    # Stops listening

    while True:

        data = input("Enter message to sent or type 'exit': ")
        if data == "exit":
            break
        msgCompressed = compress(data)

        listToString = ""
        for i, item in enumerate(msgCompressed):
            if i:
                listToString = listToString + ','
            listToString = listToString + str(item)

        msgCoded = encode(listToString, pubKeyReceived, 1)

        data2 = bytes(msgCoded, 'utf-8')
        UDPSock.sendto(data2, address)

    UDPSock.close()
    os._exit(0)


## https://rosettacode.org/wiki/LZW_compression#Python
