# This is the message receiver

import os
from socket import *
from fractions import gcd
from random import randrange
from collections import namedtuple
from math import log
from binascii import hexlify, unhexlify


# LWZ Decompression
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


def is_prime(n, k=30):
    # http://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
    if n <= 3:
        return n == 2 or n == 3
    neg_one = n - 1

    # write n-1 as 2^s*d where d is odd
    s, d = 0, neg_one
    while not d & 1:
        s, d = s + 1, d >> 1
    assert 2 ** s * d == neg_one and d & 1

    for i in range(k):
        a = randrange(2, neg_one)
        x = pow(a, d, n)
        if x in (1, neg_one):
            continue
        for r in range(1, s):
            x = x ** 2 % n
            if x == 1:
                return False
            if x == neg_one:
                break
        else:
            return False
    return True


def randprime(N=10 ** 8):
    p = 1
    while not is_prime(p):
        p = randrange(N)
    return p


def multinv(modulus, value):
    '''Multiplicative inverse in a given modulus

        >>> multinv(191, 138)
        18
        >>> multinv(191, 38)
        186
        >>> multinv(120, 23)
        47

    '''
    # http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    x, lastx = 0, 1
    a, b = modulus, value
    while b:
        a, q, b = b, a // b, a % b
        x, lastx = lastx - q * x, x
    result = (1 - lastx * modulus) // value
    if result < 0:
        result += modulus
    assert 0 <= result < modulus and value * result % modulus == 1
    return result


KeyPair = namedtuple('KeyPair', 'public private')
Key = namedtuple('Key', 'exponent modulus')


def keygen(N, public=None):
    ''' Generate public and private keys from primes up to N.

    Optionally, specify the public key exponent (65537 is popular choice).

        >>> pubkey, privkey = keygen(2**64)
        >>> msg = 123456789012345
        >>> coded = pow(msg, *pubkey)
        >>> plain = pow(coded, *privkey)
        >>> assert msg == plain

    '''
    # http://en.wikipedia.org/wiki/RSA
    prime1 = randprime(N)
    prime2 = randprime(N)
    composite = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)
    if public is None:
        while True:
            private = randrange(totient)
            if gcd(private, totient) == 1:
                break
        public = multinv(totient, private)
    else:
        private = multinv(totient, public)
    assert public * private % totient == gcd(public, totient) == gcd(private, totient) == 1
    assert pow(pow(1234567, public, composite), private, composite) == 1234567
    return KeyPair(Key(public, composite), Key(private, composite))


def decode(bcipher, privkey, verbose=False):
    chunksize = int(log(pubkey.modulus, 256))
    outchunk = chunksize + 1
    outfmt = '%%0%dx' % (chunksize * 2,)
    result = []
    for start in range(0, len(bcipher), outchunk):
        bcoded = bcipher[start: start + outchunk]
        coded = int(hexlify(bcoded), 16)
        plain = pow(coded, *privkey)
        chunk = unhexlify((outfmt % plain).encode())
        if verbose: print('Decode:', chunksize, chunk, plain, coded, bcoded)
        result.append(chunk)
    return b''.join(result).rstrip(b'\x00').decode()


host = ""
port = 13000
buf = 1024
address = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)

# Generate keys
pubkey, privkey = keygen(2 ** 64)

# It will send just one time to send public key
hostTemp = "10.48.219.167"
portTemp = 13000
addressTemp = (host, port)
UDPSockTemp = socket(AF_INET, SOCK_DGRAM)

dataKeyTemp = pubkey
dataKeyTemp = bytes(str(dataKeyTemp), 'utf-8')
UDPSock.sendto(dataKeyTemp, addressTemp)
# Stops sending

UDPSock.bind(address)
print("Receiving messages. Please wait...")

while True:
    (data, address) = UDPSock.recvfrom(buf)
    data2 = data.decode('utf-8')

    msgDecoded = decode(data2, privkey, 1)

    stringToList = []
    for x in msgDecoded.split(','):
        stringToList.append(int(x))

    msgDecompressed = decompress(stringToList)
    print("Received message: " + msgDecompressed)
    if data == "exit":
        break

UDPSock.close()
os._exit(0)

'''
    import doctest
    print(doctest.testmod())

    pubkey, privkey = keygen(2 ** 64)
    msg = 'the quick brown fox jumped over the lazy dog'
    h = encode(msg, pubkey, 1)
    p = decode(h, privkey, 1)
    print('-' * 20)
    print(repr(msg))
    print("El mensaje encriptado es: " + str(h))
    print("El mensaje desencriptado es: " + str(repr(p)))
'''
