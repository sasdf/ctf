---
name: harc4
category: crypto
points: 857
solves: 5
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}


> Four is the only number whose name in English has the same number of letters as its value,
> and the name of our favorite cipher, RC4, ends with 4.  
> Coincidence? I don’t think so!

# Overview, Concept and Design Criteria
This challenge is inspired a little bit by task `frank` in FBCTF 2019,
which attack the key of a cipher rather than ciphertext.

I googled for "weak key" and found our target -- RC4.

The first version of this challenge is using DM-like one way compression.

Although I only found some posts said that it's insecure without any proof or PoC,
It won't be too surprised that someone already knew how to forge a key for RC4.

To avoid some participants find an exploit on the lost continent,
I decided to harden it by adding a suffix to it.


# Solution
Will be released 72 hours after the end of competition.
