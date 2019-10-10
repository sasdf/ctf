from test import test_with_retry
import codecs


known = codecs.encode(b'Balsn{', 'hex')
flag = list(known) + [0] * 100

totalSZ = 150 // 2


"""
UTF-8 oracle

Invalid continuation
1101xxxx ????xxxx
1101xxxx 10xxxxxx

F5 - FF
1111??xx 101xxxxx 10xxxxxx 10xxxxxx
111100xx 101xxxxx 10xxxxxx 10xxxxxx

C0 / C1
110000?x 101xxxxx
1100001x 101xxxxx

Overlong
1110000? 10000000 10000000
11100001 10000000 10000000

a 0110 0001
b 0110 0010
c 0110 0011
d 0110 0100
e 0110 0101
f 0110 0110

0 0011 0000
1 0011 0001
2 0011 0010
3 0011 0011
4 0011 0100
5 0011 0101
6 0011 0110
7 0011 0111
8 0011 1000
9 0011 1001
"""

# Invalid continuation
# 1101xxxx ????xxxx
for i in range(len(known), totalSZ):
    prefix = [0] * (i - 1)

    key = [0b11010000, 0b10000000]
    key = [a ^ b for a, b in zip(key, flag[i-1:])]

    ret = test_with_retry(prefix + key)
    flag[i] |= 0b00110000 if ret else 0b01100000
    print(bytes(flag).rstrip(b'\0'))
# flag = b'666c61677b0000000`0`'
# flag = list(flag) + [0] * 100


# Invalid code point (F5 - FF)
# 1111??xx 101xxxxx 10xxxxxx 10xxxxxx
for i in range(len(known), totalSZ):
    print(bytes(flag).rstrip(b'\0'))

    prefix = [0] * i

    key = [0b11110000, 0b10100000, 0b10000000, 0b10000000]
    key = [a ^ b for a, b in zip(key, flag[i:])]

    ret = test_with_retry(prefix + key)
    if ret:
        flag[i] |= 0b0000
        continue
    if flag[i] & 0b11110000 == 0b01100000:
        flag[i] |= 0b0100
        continue

    key[-4] |= 0b0100
    ret = test_with_retry(prefix + key)
    flag[i] |= 0b0100 if ret else 0b1000
print(bytes(flag).rstrip(b'\0'))
# flag = b'666c61677b4040404d0`'
# flag = list(flag) + [0] * 100


# Invalid code point (C0 / C1)
# 110000?x 101xxxxx
for i in range(len(known), totalSZ):
    print(bytes(flag).rstrip(b'\0'))
    prefix = [0] * i

    if flag[i] & 0b11111100 == 0b00111000:
        flag[i] |= 0b00
        continue

    key = [0b11000000, 0b10100000]
    key = [a ^ b for a, b in zip(key, flag[i:])]

    ret = test_with_retry(prefix + key)
    flag[i] |= 0b10 if ret else 0b00
print(bytes(flag).rstrip(b'\0'))
# flag = b'666c61677b6062626d0`'
# flag = list(flag) + [0] * 100

# Overlong sequence
# 1110000? 10000000 10000000
for i in range(len(known), totalSZ):
    print(bytes(flag).rstrip(b'\0'))
    prefix = [0] * i

    if flag[i] == 0b01100000:
        flag[i] = 0b01100001
        continue
    if flag[i] == 0b01100110:
        continue

    key = [0b11100000, 0b10000000, 0b10000000]
    key = [a ^ b for a, b in zip(key, flag[i:])]

    ret = test_with_retry(prefix + key)
    flag[i] |= 0b1 if ret else 0b0
print(bytes(flag).rstrip(b'\0'))
print(codecs.decode(bytes(flag).rstrip(b'\0'), 'hex'))


exit(0)
