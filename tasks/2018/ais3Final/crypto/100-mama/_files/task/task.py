#!/usr/bin/python3.6

import sys
import os
import random
from Crypto.Util.number import getPrime


flag = os.environ['FLAG']
n = None


def mul(x, y):
    x = x if x else n
    y = y if y else n
    r = (x * y) % (n + 1)
    r = r if r != n else 0
    return r


def add(x, y):
    return (x + y) % n


def encrypt(plaintext):
    ciphertext = random.randrange(n)
    return ciphertext


def decrypt(ciphertext, keys):
    for op, arg in keys:
        if op == 0:
            ciphertext = mul(ciphertext, arg)
        elif op == 1:
            ciphertext = add(ciphertext, arg)
    return ciphertext


def readKey():
    key = []
    # Goodluck~
    for i in range(777):
        op = int(sys.stdin.readline(8).strip())
        if op == 2:
            break
        if op != 0 and op != 1:
            raise ValueError('Invalid opcode')
        arg = int(sys.stdin.readline(128).strip(), 16)
        if not 0 <= arg < n:
            raise ValueError('Invalid argument')
        key.append((op, arg))
    return key


def challenge():
    plaintext  = [random.randrange(n) for _ in range(128)]
    ciphertext = [encrypt(p) for p in plaintext]
    print(f'{"plaintext":^34s} => {"ciphertext":^34s}')
    for p, c in zip(plaintext, ciphertext):
        print(f'0x{p:032x} => 0x{c:032x}')
    print('')
    print('Give me the decryption key:')
    sys.stdout.flush()
    keys = readKey()
    decrypted = [decrypt(c, keys) for c in ciphertext]
    return decrypted == plaintext


def main():
    global n
    n = getPrime(128) - 1
    print(f'n = {n:032x}')
    print('')
    try:
        if challenge():
            print("Here's your flag:")
            print(flag)
        else:
            print('Failed')
    except ValueError as e:
        print(str(e))
        print(str(e), file=sys.stderr)


if __name__ == '__main__':
    main()
