---
name: Lost Modulus
category: crypto
points: 230
solves: 42
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf-tasks-writeup/)
{% endignore %}

> I lost my modulus. Can you find it for me?

## Time
2 hours  
First blood

## Behavior
The server implement paillier cryptosystem.
It gives us a encrypted flag at start.

There are two operations, A and B,
Operation A return the ciphertext of our input.
Operation B gives us the last byte of plaintext.
We can run atmost 2048 operations.

Unfortunately, we know nothing about $$n, p, q, g$$.


# Solution
## TL;DR
1. Leak 8 ~ 1024 bits of n bit-by-bit (1008 OPs).
2. Last byte is `-ret` (0 OPs).
3. Leak 16 bytes of flag (16 OPs).
4. Repeat with a new connection.

We can calculate $$m\ \mod n$$ by encrypting it and then decrypting,
If $$m < n$$, we get the last byte of $m$.
However, if $$m \ge n$$, we get the last byte of $$m\ \mod n$$.
We can leak $$n$$ bit-by-bit by select $$2^b$$ as $$m$$.
Moreover, the return value is $$-n \ \mod 256$$ if $$m \ge n$$,
which means we have 16 operations left for leaking 16 bytes of flag.

For example, Let $$n \coloneqq 233 * 263 = 61279 = 0b01110 \cdots$$
$$
\begin{aligned}
    2^{16}\ \mod n &= 161 \\
    2^{15}\ \mod n &= 0 \\
    2^{15} + 2^{14}\ \mod n &= 0 \\
    2^{15} + 2^{14} + 2^{13}\ \mod n &= 0 \\
    2^{15} + 2^{14} + 2^{13} + 2^{12}\ \mod n &= 161 \\
    & \cdots \\
    -n \mod 256 &= 161 \\
\end{aligned}
$$

To decrypt the flag,
we can use the homomorphic property of paillier:
$$
\begin{aligned}
    c_1 \times c_2\ \mod n^2 &= \text{Enc}(m_1 + m_2\ \mod n) \\
    c_1^{m_2}\ \mod n^2 &= \text{Enc}(m_1 * m_2\ \mod n) \\
\end{aligned}
$$
Decrypt it with following recursive equation:
$$
\begin{aligned}
    c_t &= (c_{t-1} / \text{Enc}(m_{t-1}))^{1/256}\ \mod n^2 \\
    m_t &= \text{Dec}(c_t)\ \mod 256 \\
\end{aligned}
$$
