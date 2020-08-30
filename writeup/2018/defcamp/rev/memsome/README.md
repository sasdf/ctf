---
name: memsome
category: rev
points: 110
solves: 67
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> I can not find my license file. Can you help me?

## Time
30 minutes

# Solution
## TL;DR
1. Extract target hashs from the binary
2. Bruteforce the flag

A tip for reversing c++ binary is to ignore anything you don't understand to preserve sanity.
The binary read the input for a file, apply ROT13 to it, and compare the hash of each byte.
The hash function is `base64 . md5hex . md5hex`
To recover the flag, just [bruteforce]([_files/solve.py]) it.

