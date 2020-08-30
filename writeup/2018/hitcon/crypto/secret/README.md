---
name: Secret Note
category: crypwn
points: 342
solves: 9
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> UPDATE: Running on Ubuntu 18.04
> plz read the note

## Time
6 hours  

## Behavior
The service has two kinds of note:

Type 1 is encrypted by RSA,
i.e. $$m^{217}\ \mod n$$ for our input $$m$$,
where $$n$$ is fixed and known.

Type 2 is encrypted by AES,
where key is fixed but unknown,
and iv is random among each connection.

The service stores the note in plaintext.
When we call `show` command,
it will encrypt the note and return the result.

There are two default notes,
the first one is the flag with AES encryption,
and the second one is AES key with RSA encryption.


# Solution
## TL;DR
1. Overflow to change N.
2. Collect many encrypted AES key with different N.
3. Get $$\text{key}^{217}$$ using CRT.
4. Get the key by calculate its 217-th root.
5. Leak the iv with all zeros plaintext.
6. Decrypt the flag.

After [reversing the binary]([_files/rev.py]),
the encryption algorithm of type 1 turns out to be AES-128-CBC,
which is not breakable under current tech.
So we've tried hard to factorize the N but failed.

Recall that this challenge is crypto + pwn,
I decided to dig into the binary again,
I found that it has 12 bytes heap overflow.
When the length of our plaintext is multiple of 16,
PKCS7 padding will pad one more block at the end,
but it doesn't calloc enough space for the additional block.

Moreover,
there's an unsorted bin in front of the heap chunk of mpz storing N,
so that we can allocate before N and overflow to change it.
With many ciphertext of different N,
we can perform hastad broadcast attack to recover the plaintext.

Before that,
we need to know what is N after overflow.
We can eliminate the effect of iv with following equation:
$$
\text{Enc}_{\text{iv}}(m_1\ ||\ \text{Enc}_{\text{iv}}(m_1) \oplus m_2)
= \text{Enc}_{\text{iv}}(m_1)\ ||\ \text{Enc}_{0}(m_2)
$$

Next,
To perform CRT,
we have to make sure all Ns are coprime first,
we calculate the gcd of all N pairwisely,
and strip off those divisor.
Now, we can recover the key with hastad attack.

To decrypt the flag,
we have to know what iv is.
We can get encrypted iv with plaintext of all zeros:
$$
\text{Enc}_{\text{iv}}(0)
= \text{Enc}_{0}(\text{iv} \oplus 0) = \text{Enc}_{0}(\text{iv})
$$
Then we can decrypt the iv and get the flag.
