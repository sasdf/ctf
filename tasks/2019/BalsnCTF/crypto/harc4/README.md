---
name: harc4
category: crypto
points: 857
solves: 5
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
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

## Fun facts
* This task is written during the midterm week. I always become super creative on everything except my midterm when midterm is coming.


# Solution
This task is about crafting a key of RC4 with some suffix that can generate a short keystream we want.

To make it simpler, let's start with a simpler version without suffix first:
Find a key such that first 3 bytes of RC4 keystream is `[42, 13, 37]`.

RC4 has two routines, KSA for initialize state with key, and PRGA for generate keystream.

## Simpler KSA
```python
S = list(range(256))
j = 0
for i in range(256):
    j = (j + S[i] + key[i % len(key)]) % 256
    swap(S[i], S[j])
```
If we can control all 256 bytes of the key, we can control all `j`.

It's trivial to construct a key for a given SBox:
Just swap the value we want to each position.

## PRGA
```python
i, j = 0, 0
while True:
    i = (i + 1) % 256
    j = (j + S[i]) % 256
    k = (S[i] + S[j]) % 256
    swap(S[i], S[j])
    yield S[k]
```
It's more trickly in this part, we can control S[i] and S[j], but we can't use duplicate elements,
which makes `j` increase pretty fast.

Let's construct a solution manually first.
Consider following SBox:
```
Pos:   00 01 02 03 ... 10 11 12 13 ... 22 23 24 ... 30 ...
Val:   ?? 10 01 02 ... 20 21 ?? 22 ... 13 ?? 37 ... 42 ...
Step1:    i            j                            k
Step2:       i            j            k
Step3:          i               j            k
(Numbers are in decimal)
```
It will output the keystream we want.
To construct a SBox for longer keystream, I use DFS to search for a solution without conflict about position or element value.

## Leak IV
Now, let's come back to the final version with suffix.

The suffix is randomly generated, the first thing is to leak it.

Our one way compression function looks like:
```python
state = IV
for i in range(0, len(x), csz):
    # ...
return state.hex()
```
So if we send a empty string to it, it will give us IV.

## KSA with suffix
From first section,
we know that not all position has constraint on its value.
If the suffix doesn't messup those critical points, we can just construct our key as same as before.

To construct the key,
rewind the suffix with all possible `j` first, and check whether we can swap those critical points to the place we want.
If there's no solution, go back to previous part and search for another SBox.

You can find full exploit [here]([_files/solution/solve.py]).
