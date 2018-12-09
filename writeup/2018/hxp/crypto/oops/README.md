---
name: oops2
category: crypto
points: 206
solves: 4
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}

> Provable security just gives you this warm fuzzy feeling of cryptography you can rely on.


## Time
4 hours


# Behavior
We have the flag encrypted by ECB mode,
and the service provide us an encryption/decryption oracle in OCB mode.


# Solution
## TL;DR
1. Construct some plain/ciphertext pair.
2. Forge last block and tag.
3. Decrypt the flag.


The task download code of ocb from
[here](http://web.cs.ucdavis.edu/~rogaway/ocb/ocb.c)
But the download link in
[their website](http://web.cs.ucdavis.edu/~rogaway/ocb/)
is not the same.
Also, the algorithm in the code is different from what their FAQ says.

So, what's wrong?

It turns out that the code is actually OCB2,
and an 
[attack](https://en.wikipedia.org/wiki/OCB_mode#Attacks)
on it was just published recently.

Using the method in the paper,
we can decrypt the flag.

Here's the [script]([_files/solve.py]).
