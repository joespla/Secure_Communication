# This is the message receiver

import os

# LWZ Decompression


from socket import *


def decompress(compressed):
    """Decompress a list of output ks to a string."""
    from io import StringIO

    # Build the dictionary.
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}

    result = StringIO()
    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry
    return result.getvalue()

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

    c = []
    for x in data2.split(','):
        c.append(int(x))

    data2 = decompress(c)
    print("Received message: " + data2)
    if data == "exit":
        break

UDPSock.close()
os._exit(0)
