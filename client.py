# This is the message sender
import os
from socket import *
from fractions import gcd
from random import randrange
from collections import namedtuple
from math import log
from binascii import hexlify, unhexlify
from threading import Thread
import tkinter


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
        # if verbose: print('Encode:', chunksize, chunk, plain, coded, bcoded)
        result.append(bcoded)
    return b''.join(result)


def send(event=None):
    # data = input("Enter message to sent or type 'exit': ")
    data = my_msg.get()
    my_msg.set("")

    if not data:
        data = "Send a correct message"

    if data == "exit":
        UDPSock.close()
        os._exit(0)
    msgCompressed = compress(data)
    print(msgCompressed)

    listToString = ""
    for i, item in enumerate(msgCompressed):
        if i:
            listToString = listToString + ','
        listToString = listToString + str(item)

    msgCoded = encode(listToString, pubKeyReceived, 1)
    print(msgCoded)

    UDPSock.sendto(msgCoded, address)


if __name__ == '__main__':
    # Set the ip from the receiver
    host = "192.168.100.9"
    port = 13007
    address = (host, port)

    # Listen just one time to receive public keys
    hostTemp = ""
    portTemp = 13004
    bufTemp = 1024
    addressTemp = (hostTemp, portTemp)
    UDPSockTemp = socket(AF_INET, SOCK_DGRAM)

    UDPSockTemp.bind(addressTemp)

    (dataKeyTemp, addressTemp) = UDPSockTemp.recvfrom(bufTemp)
    data2 = dataKeyTemp.decode('utf-8')

    exponent, modulus = data2.split(",")
    exponent = int(exponent)
    modulus = int(modulus)

    pubKeyReceived = Key(exponent, modulus)
    print("Key received")
    UDPSockTemp.close()
    # Stops listening

    UDPSock = socket(AF_INET, SOCK_DGRAM)

    top = tkinter.Tk()
    top.title("Jorge Espinosa Lara")
    top.geometry("500x500")

    my_msg = tkinter.StringVar()  # For the messages to be sent.
    my_msg.set("Type your messages here.")

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=send)
    send_button.pack()

    tkinter.mainloop()
