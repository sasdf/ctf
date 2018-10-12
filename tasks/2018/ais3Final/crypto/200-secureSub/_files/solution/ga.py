#!/usr/bin/python3.6

from encryption import uuencode, encrypt
import random
import json
import functools as fn
import numpy as np
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


@fn.lru_cache(10000)
def fitness(a, notFound=-25):
    plain = encrypt(ciphertext, a)
    tgs = zip(plain, plain[1:], plain[2:])
    score = sum(trigram.get(tg, notFound) for tg in tgs)
    return score


def initialize(size):
    population = []
    for i in range(size):
        mapping = list(range(32, 96))
        random.shuffle(mapping)
        population.append(tuple(mapping))
    return population


def crossover(a, b, prob):
    r = list(a)
    for i in range(len(r)):
        if random.random() < prob and r[i] != b[i]:
            r[i], r[r.index(b[i])] = b[i], r[i]
    return tuple(r)


def mutate(a):
    r = list(a)
    i = j = random.randrange(len(a))
    while j == i:
        j = random.randrange(len(a))
    r[i], r[j] = r[j], r[i]
    return tuple(r)


def select(population, size):
    scores = np.array([fitness(p) for p in population])
    scores = np.exp(scores - scores.max()) + 1e-300
    scores = scores / scores.sum()
    idx = np.random.choice(len(population), size, replace=False, p=scores)
    return [population[i] for i in idx]


def truncate(population, size):
    population = population[:]
    population.sort(key=lambda x: -fitness(x))
    population = population[:size]
    return population


#-- Run Genetic Algorithm --#
population = initialize(1000)
try:
    for iter in range(1000):
        best = population[0]
        plain = encrypt(ciphertext, best)
        score = fitness(best)
        print(f'[Iter {iter:5d}] {score:10.2f}:  {toPrintable(plain[:60])}')
        for p in select(population[1:], 20):
            c = crossover(best, p, 0.5)
            population.append(c)
            for i in range(5):
                m = mutate(c)
                population.append(m)
        population = list(set(population))
        population = truncate(population, 1000)
except KeyboardInterrupt:
    pass
mapping = population[0]


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
