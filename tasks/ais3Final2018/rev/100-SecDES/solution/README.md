# TL;DR
Feed the encrypted flag to the checker, it will tell you what the plaintext is.


# Overview, Concept and Design Criteria
The challenge name, SecDES, stands for both Secure DES and SHA256 DES.

This challenge is for simplest reverse 100, so symbols are not stripped, and no obfuscation is applied.
It won't be too hard to reverse the encryption algorithm as I've already told you it's DES.

In order to make this challenge more interesting,
I choose a special encryption key,
resulting in two intended solutions for this challenge.


# Reversish solution
This is a modified DES cipher, where the concept of bit is replaced by byte.
For example, original DES works on 64 bits data, and our SecDES works on 64 bytes data.
All the permutations and key schedule, with the exception of the sbox, are same as original DES.
For the sbox in the feistel function, I use SHA256 to reduce 48 bytes expanded data to 32 bytes.

The program reads 64 bytes of data, encrypt with a hard coded key,
and then compare with a encrypted flag.
You can solve this challenge by implement a decryption function,
extract the key, data, and then decrypt it.


# Cryptographic solution
DES has 4 [weak keys](https://en.wikipedia.org/wiki/Weak_key)
that make encryption function identical to decryption function.
That is, `E(E(data)) = data`. For more details and the underlying reasons,
see the wikipedia page above.
If the implementation ignore those 8 parity bits, there are 4 times 2 to the 8 different weak keys.

The key I chose is one of the weak keys, 0xE1E1E1E1F0F0F0F0.
Bit 1 is actually char `Y`, bit 0 is actually char `E`,
and the parity bits are replaced with `AIS3{__}`.

So there's no need to implement decryption routine by yourself,
just feed the encrypted flag to the checker, it will decrypt it for you.
