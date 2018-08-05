#!/usr/bin/python3.6

from encryption import uuencode, encrypt
import random
import math
import json
import readline


print("""
It may converge to local optima, Run it several times until
the plaintext is clear enough to recover manually.
""")

def getEncoded(data):
    encoded = uuencode(data)
    encoded = encoded.split(b'\n')
    data = encoded[1: -3]
    return b''.join(line[1:] for line in data)


def toPrintable(data):
    ul = ord('_')
    data = bytes(c if 32 <= c < 127 else ul for c in data)
    return data.decode('ascii')


# -- Loading data -- #
with open('../task/ciphertext', 'rb') as f:
    ciphertext = f.read()

with open('trigram.json') as f:
    trigram = json.load(f)
    trigram = {tuple(k.encode('ascii')): v for k, v in trigram.items()}


# -- Hill climbing -- #
chars = [c - 32 for c in set(getEncoded(ciphertext))]
mapping = bestMapping = list(range(32, 96))
current = best = -10000000
bestPlain = ''
for iter in range(30000):
    guess = mapping[:]
    idx2 = idx1 = random.choice(chars)
    while idx2 == idx1:
        idx2 = random.randrange(64)
    guess[idx1], guess[idx2] = guess[idx2], guess[idx1]
    plain = encrypt(ciphertext, guess)
    tgs = zip(plain, plain[1:], plain[2:])
    score = sum(trigram.get(tg, -25) for tg in tgs)
    if (current - score) * random.random() < 1000 / math.sqrt(iter+1):
    # if best < score or random.random() < 1 / math.sqrt(iter+1):
        current = score
        mapping = guess
        print(f'[Iter {iter:5d}] {score:10.2f}:  {toPrintable(plain[:60])}')
        if best < score:
            best = score
            bestPlain = plain
            bestMapping = mapping
plain = bestPlain
mapping = bestMapping


# -- Manually fix -- #
print('')
print('Manually fix')
print('n: next, b: back, p: print current plaintext')
print('or enter the correct plaintext')
off = 0
while True:
    line = plain[off:off+60]
    print(f'{off}: |{toPrintable(line)}|')
    cmd = input('> ').encode('ascii')
    if cmd == b'n':
        if off + 60 < len(plain):
            off += 60
    elif cmd == b'b':
        if off - 60 >= 0:
            off -= 60
    elif cmd == b'p':
        print(toPrintable(plain))
    elif len(cmd) == len(line):
        encCorrect = getEncoded(cmd)
        encCipher = getEncoded(ciphertext[off:off+60])
        for a, b in zip(encCorrect, encCipher):
            mapping[b-32] = a
        plain = encrypt(ciphertext, mapping)
    else:
        print('Incorrect input')
