import numpy as np


def rot13(s):
    x = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    y = b'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
    d = {xi: yi for xi, yi in zip(x,y)}
    return [d.get(c, c) for c in s]


key = b'Welcome to th1s flag checker in vim.'[:16]
key = rot13(key.replace(b' ', b'_'))

key = np.array(key).reshape(4, 4)

key = (key @ key) % 32

"""
# This inverse was calculated by SageMath.
"""
inv = np.array([
    [23, 23,  6, 13],
    [24, 12, 29, 30],
    [17, 23,  7,  8],
    [ 7,  4, 21, 21],
    ])


target = [23, 30, 17, 21, 26, 7, 22, 3, 1, 18, 4, 17, 2, 10, 21, 9]
target = target[:1] + [(a - b) % 32 for a, b in zip(target[1:], target)]

target = np.array(target).reshape(4, 4)

key = (key >> 2) + (key << 3) % 32
target = (target - key) % 32
target = (target >> 3) + (target << 2) % 32

target = (inv @ target) % 32

target = target.reshape(-1) + ord('a') - ord('a') % 32
target[target == 127] = ord('_')

target = bytes(target.tolist())
target = rot13(target)
print((b'Balsn{' + bytes(target) + b'r}').decode('ascii'))
