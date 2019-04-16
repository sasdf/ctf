import random
import numpy as np
from rec import enc
from tqdm import trange


"""
Sample:

d909 74bd feb7 12e8 83e5 bd83 e558 d3b5  ..t..........X..
fa27 87a8 af7f fe0b

504b 0102 Cent
1e03
0a00
0000
0000
f016
4b4e
5a25 57b3
7c39 0000
7c39 0000
0f00
1800
0000
0000
0000
0000 a481 (or 0000 ed81)
0000 0000
7365 6372 6574 732e 7a69 702e 656e 63

5554 UT
0500
03
24e4 605c

7578 ux
0b00
01
04
0000 0000
04
00 0000 00


Template:

6a79 e8fa 5bb2 1bec 635f 142a 7d3f f3df  jy..[...c_.*}?..

504b 0102
1e03
0a00      // 1400: deflate
0000
0000      // 0800: deflate
b26b      // time
634e      // date
cd81 085e // crc
4200 0000 // comp size: diff if deflate
4200 0000 // size
1000
1800
0000
0000
0100
0000 b481 // should be a481
0000 0000
666c 6167 2d63 7970 7265 7373 2e74 7874 filename

5554 UT
0500
03
3f66 7b5c // unix time

7578 ux
0b00
01
04
e803 0000 // should be 0000 0000
04
e803 0000 // should be 0000 0000

504b 0102 Cent
1e03
1400
0000
0800
b7b2      // time
7a4e      // date
f9f2 0041
f220 0000
b721 0000
0900
1800
0000
0000
0000
0000 b481 // should be a481
8c00 0000 // offset xx00 0000 ~ comp. flagsize
6461 6e6e 792e 6a70 67 danny.jpg

5554 UT
0500
03
7a35 9a5c // unix time

7578 ux
0b00
01
04
e803 0000 // should be 0000 0000
04
e803 0000 // should be 0000 0000

504b 0506 EOCD
0000
0000
0200
0200
a500 0000
c121 0000 // offset xxxx 0000
0000
"""


def gen_tail():
    deflate = random.random() > 0.5
    res = ''
    res += '504b 0102'
    res += '1e03'
    res += '1400' if deflate else '0a00'
    res += '0000'
    res += '0800' if deflate else '0a00'
    res += hex(random.getrandbits(24))[2:].rjust(6, '0') + '4e'
    res += hex(random.getrandbits(32))[2:].rjust(8, '0')
    res += hex(random.getrandbits(8))[2:].rjust(2, '0') + '00 0000'
    res += hex(random.getrandbits(8))[2:].rjust(2, '0') + '00 0000'
    res += '1000'
    res += '1800'
    res += '0000'
    res += '0000'
    res += '0100'
    res += '0000 a481'
    res += '0000 0000'
    res += '666c 6167 2d63 7970 7265 7373 2e74 7874'

    res += '5554'
    res += '0500'
    res += '03'
    res += hex(random.getrandbits(24))[2:].rjust(6, '0') + '5c'
    
    res += '7578'
    res += '0b00'
    res += '01'
    res += '04'
    res += '0000 0000'
    res += '04'
    res += '0000 0000'
    
    res += '504b 0102'
    res += '1e03'
    res += '1400'
    res += '0000'
    res += '0800'
    res += hex(random.getrandbits(24))[2:].rjust(6, '0') + '4e'
    res += 'f9f2 0041'
    res += 'f220 0000'
    res += 'b721 0000'
    res += '0900'
    res += '1800'
    res += '0000'
    res += '0000'
    res += '0000'
    res += '0000 a481'
    res += hex(random.getrandbits(8))[2:].rjust(2, '0') + '00 0000'
    res += '6461 6e6e 792e 6a70 67' # danny.jpg

    res += '5554'
    res += '0500'
    res += '03'
    res += hex(random.getrandbits(24))[2:].rjust(6, '0') + '5c'
    
    res += '7578'
    res += '0b00'
    res += '01'
    res += '04'
    res += '0000 0000'
    res += '04'
    res += '0000 0000'

    res += '504b 0506'
    res += '0000'
    res += '0000'
    res += '0200'
    res += '0200'
    res += 'a500 0000'
    res += hex(random.getrandbits(16))[2:].rjust(4, '0') + '0000'
    res += '0000'

    return bytes.fromhex(res)


with open('secrets.zip', 'rb') as f:
    sec = f.read()

prefix = sec[:-len(gen_tail())][300:]

chars = []
bits = []
bar = trange(400)
try:
    for qq in bar:
        tail = gen_tail()
        cstr, cipher, root = enc(np.random.bytes(1000), prefix + tail)
        cipher = [''.join(map(str, c)) for c in cipher[:-1]]
        bits.append(cipher)
        chars.append(prefix + tail)
finally:
    bar.close()
