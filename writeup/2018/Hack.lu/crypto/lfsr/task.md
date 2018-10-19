---
name: LFSR StreamCipher
category: crypto
points: 500
solves: 3
---

# Description

I was told you know something about crazy crypto?

Maybe you can help us out then. We are looking into these arcade machines from our rivaeehm friend. Eeh.. He 'lost' his programming machines and his backups (of course he had backups) and asked us, if we can help him with reversing the code from his game machine. We were also already able to dump everything from the machine, but it is encrypted with some custom stream cipher, build in the hardware of the machine.

Our friend was able to.. remember some details of this stream cipher (after some longer 'interview' we had). Apparently it is a filter generator with the following details:
```
Characteristic Polynomial: x^256 + x^10 + x^5 + x^2 + 1
Filter Function:
      x0*x64*x96*x128*x192*x255
    + x0*x64*x96*x128*x192
    + x0*x64*x96*x128
    + x0*x64*x96*x192
    + x0*x64*x128*x192*x255
    + x0*x64*x192*x255
    + x0*x64*x192
    + x0*x64*x255
    + x0*x96*x128*x192
    + x0*x96*x128*x255
    + x0*x96*x128
    + x0*x96*x192
    + x0*x128*x192*x255
    + x0*x128*x192
    + x0*x128*x255
    + x0*x128
    + x0*x192
    + x0*x255
    + x0
    + x64*x96*x128*x192*x255
    + x64*x96*x128*x192
    + x64*x96*x192
    + x64*x96*x255
    + x64*x128
    + x64*x192*x255
    + x64*x192
    + x64*x255
    + x64
    + x96*x128*x192*x255
    + x96*x128*x255
    + x96*x128
    + x96*x192*x255
    + x96*x192
    + x96*x255
    + x96
    + x128*x192*x255
```

(crazy guy that he is able to remember this nice filter function!)
Luckily we were also able to extract the first keystream bits, because of the fileformat details our friend gave us:

First 1001 Output Key-Bits (LSB = 0th output, MSB = 1000th output):

```
0x131018c85020813093200c6ae4822e400261853722f054a1e0
80560034008605080380810640342825506829c0209a04134010
1b54f1848425aa208035d40510068044597575a02b115a900243
6958884d110a2515022240aec060e0a0200c4296081062829a00
328250210001533404b206301482800234000501d0104
```
    	

But now we are stuck and need your help. Find the secret seed of the stream cipher so that we can decrypt the remaining game code and get our friend out of the jam.

# Announcements for LFSR StreamCipher
(Published on 2018-10-18 00:14:00)

Thanks to a real friend of us, we found some more info about this strange LFSR. Its somewhat wiredly clocked:
```
new_x0 = old_x1
new_x1 = old_x2
...
new_x254 = old_x255
new_x255 = old_x0 + old_x2 + old_x5 + old_x10
```

And these output bits were also wrong. The right ones for seed 0x1 are (without filter function):
```
0x5c960484000000000000000000000000000000000000000000
0000000000000110401000000000000000000000000000000000
0000000000000000000000000148400000000000000000000000
0000000000000000000000000000000000000100000000000000
00000000000000000000000000000000000000000000000001
```

(Published on 2018-10-17 16:38:52)

To avoid guesswork and confusion: The first 512 output bits of the LFSR seeded with 0x1 (lsb) without filtering in the same format as in the challenge are:
```
0x48400000000000014840000148400000000000000000000000
0000000000000100000000000000010000000100000000000000
00000000000000000000000001
```

