---
name: Relations
category: crypto
points: 205
solves: 73
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}

> Two completely unrelated operations on completely unrelated values, right?

## Time
30 mins  


## Behavior
```
.. nc arcade.fluxfingers.net 1821
------------------------------
Welcome to theory world
------------------------------

------------------------------
Possible Oracles
(XOR) Choose XOR Oracle
(ADD) Choose ADD Oracle
(DEC) For trying to decrypt
-----------------------------*
XOR

Please choose the operand in hex >>> 0
Ciphertext is  LaIED+tNb4H2B3YQi97GNNqndX8BuFh8Al1/z/AIXtiYas5LCK2SvYsO4vJAad2g+2TnJKcrwmSw
YOZo8enlVw==

------------------------------
Possible Oracles
(XOR) Choose XOR Oracle
(ADD) Choose ADD Oracle
(DEC) For trying to decrypt
-----------------------------*
ADD

Please choose the operand in hex >>> 0
Ciphertext is  LaIED+tNb4H2B3YQi97GNNqndX8BuFh8Al1/z/AIXtiYas5LCK2SvYsO4vJAad2g+2TnJKcrwmSw
YOZo8enlVw==

------------------------------
Possible Oracles
(XOR) Choose XOR Oracle
(ADD) Choose ADD Oracle
(DEC) For trying to decrypt
-----------------------------*
DEC

Enter the key base64 encoded >>> 0000
Traceback (most recent call last):
  File "/home/chall/rka.py", line 113, in <module>
    main()
  File "/home/chall/rka.py", line 107, in main
    aes = pyaes.AESModeOfOperationECB(key)
  File "/home/chall/pyaes/aes.py", line 304, in __init__
    self._aes = AES(key)
  File "/home/chall/pyaes/aes.py", line 134, in __init__
    raise ValueError('Invalid key size')
ValueError: Invalid key size
```

# Solution
The server provide three operations:
* Encryption(aeskey ^ operand)
* Encryption(aeskey + operand)
* AESDec(inputkey, AESEnc(aeskey, flag))

When bit $$i$$ in aeskey is 0,
$$
\begin{aligned}
    &
        \text{aeskey} \oplus 2^i
        = \text{aeskey} + 2^i \\
    \implies &
        \text{Encryption}(\text{aeskey} \oplus 2^i)
        = \text{Encryption}(\text{aeskey} + 2^i) \\
\end{aligned}
$$
Otherwise those are not equal.
We can recover the key bit-by-bit to get key for decrypting the flag.
