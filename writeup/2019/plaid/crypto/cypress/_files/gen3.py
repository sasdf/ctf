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


Secret:

5bb21bec635f142a7d3ff3df00
504b 0102
1e03
1400
0000
0800
8a16
4b4e
1e84 ac74
4f00 0000
5100 0000
1000
1800
0000
0000
0100
0000 a481
0000 0000
666c 6167 2d63 7970 7265 7373 2e74 7874

5554
0500
03
64e3 605c

7578
0b00
01
04
0000 0000
04
0000 0000

504b 0102
1e03
1400
0000
0800
f016
4b4e
f9f2 0041
f220 0000
b721 0000
0900
1800
0000
0000
0000
0000
a481
9900 0000
64616e6e792e6a7067
5554
0500
03
24e4 605c
7578
0b00
01
04
00000000
04
00000000
504b 0506
0000
0000
0200
0200
a500 0000
ce21 0000
0000

Local:
3ad1 bd7a 2dc7 9ff8 8af1 ff0b
504b 0304
1400
0000
0800
2eb4 484e
f71e d12a
742e 0000
e867 0000
0e00
1c00
7370 6c61 6964 2d63 7970 7265 7373

5554
0900
03
b803 5e5c
24e4 605c

7578
0b00
01
04
0000 0000
04
0000 0000

Local Secret:
504b 0304
1409
0809
f016
4b4e
f9f2 0941
f220 0909
b721 0909
001c
0064
616e6e792e6a7067

5554
0900
03
24e4 605c
24e4 605c

7578
0b00
01
04
0000 0000
04
0000 0000
9db77750d441f7e6fb1dc9411464900c926100910c1214244ace39233080e49c4140c941
"""


def gen_tail():
    res = ''
    res += '504b 0102'
    res += '1e03'
    res += '1400'
    res += '0000'
    res += '0800'
    res += '8a16 4b4e'
    res += '1e84 ac74'
    res += '4f00 0000'
    res += '5100 0000'
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
    res += '64e3 605c'
    
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
    res += 'f016 4b4e'
    res += 'f9f2 0041'
    res += 'f220 0000'
    res += 'b721 0000'
    res += '0900'
    res += '1800'
    res += '0000'
    res += '0000'
    res += '0000'
    res += '0000 a481'
    res += '9900 0000'
    res += '6461 6e6e 792e 6a70 67' # danny.jpg

    res += '5554'
    res += '0500'
    res += '03'
    res += '24e4 605c'
    
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
    res += 'ce21 0000'
    res += '0000'

    return bytes.fromhex(res)


def gen_head():
    res = ''

    res += '504b 0304'
    res += '1400'
    res += '0000'
    res += '0800'
    res += '8a16 4b4e'
    res += '1e84 ac74'
    res += '4f00 0000'
    res += '5100 0000'
    res += '1000'
    res += '1c00'
    res += '666c 6167 2d63 7970 7265 7373 2e74 7874'

    res += '5554'
    res += '0900'
    res += '03'
    res += '64e3 605c'
    res += hex(random.getrandbits(16))[2:].rjust(4, '0') + '605c'
    
    res += '7578'
    res += '0b00'
    res += '01'
    res += '04'
    res += '0000 0000'
    res += '04'
    res += '0000 0000'
    
    res += np.random.bytes(0x4f).hex()

    res += '504b 0304'
    res += '1400'
    res += '0000'
    res += '0800'
    res += 'f016 4b4e'
    res += 'f9f2 0041'
    res += 'f220 0000'
    res += 'b721 0000'
    res += '0900'
    res += '1c00'
    res += '6461 6e6e 792e 6a70 67' # danny.jpg

    res += '5554'
    res += '0900'
    res += '03'
    res += '24e4 605c'
    res += '24e4 605c'
    
    res += '7578'
    res += '0b00'
    res += '01'
    res += '04'
    res += '0000 0000'
    res += '04'
    res += '0000 0000'

    return bytes.fromhex(res)


with open('secrets.zip', 'rb') as f:
    sec = f.read()

data = sec[:-len(gen_tail())][-0x20f2:] + gen_tail()

chars = []
bits = []
bar = trange(400)
try:
    for qq in bar:
        head = gen_head()
        cstr, cipher, root = enc(np.random.bytes(1000), head + data)
        cipher = [''.join(map(str, c)) for c in cipher[:-1]]
        bits.append(cipher)
        chars.append(head + data)
finally:
    bar.close()

bits = np.array(bits)
vlen = np.vectorize(len)
bitslen = vlen(bits)
lenMean = bitslen.mean(0)
lenStd = bitslen.std(0)
np.save('bits.npy', bits)
np.save('lenMean.npy', lenMean)
np.save('lenStd.npy', lenStd)

charsh = [c.hex() for c in chars]
charsh = [[c[i:i+2] for i in range(0, len(c), 2)] for c in charsh]
charsnp = np.array(charsh)

msk = np.bitwise_and.reduce(bits == bits[0:1])
pin = [bits[0][i] if m else '' for i, m in enumerate(msk)]
with open('pin.txt', 'w') as f:
    for c in pin:
        f.write(c + '\n')

msk = np.bitwise_and.reduce(charsnp == charsnp[0:1])
pin = [charsnp[0][i] if m else '' for i, m in enumerate(msk)]
with open('chars.txt', 'w') as f:
    for c in pin:
        f.write(c + '\n')
