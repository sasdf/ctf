#!/usr/bin/env python3

import math
import sys
from telnetlib import Telnet
from phe import paillier


def ot_receiver(t, sigma):
    pk, sk = paillier.generate_paillier_keypair()
    t.write('{}\n'.format(pk.n).encode())
    c = pk.raw_encrypt(sigma)
    t.write('{}\n'.format(c).encode())

    c0 = int(t.read_until(b'\n').decode().strip())
    c1 = int(t.read_until(b'\n').decode().strip())
    print("c0 = {}".format(c0))
    print("c1 = {}".format(c1))
    x_sigma = sk.raw_decrypt([c0, c1][sigma])
    m_sigma = x_sigma.to_bytes(math.ceil(x_sigma.bit_length() / 8), 'big')
    return m_sigma


if __name__ == '__main__':
    t = Telnet('localhost', 1337)
    m_sigma = ot_receiver(t, 0)
    print(m_sigma)
