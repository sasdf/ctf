---
name: blind
category: crypto
points: 190
solves: 11
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> The deal is simple: I give you an oracle, you give me an oracle in return.


## Time
4 hours


# Behavior
We have the ciphertext of our target y,
and the ciphertext of 1.
We have three operations: add, mul and negate with modulo 0xfffffed83c17.
The service run these operations on plaintext and return the encrypted result to us.
Our goal is to decrypt y.


# Solution
## TL;DR
1. Get the order of y in each subgroup.
2. Recover the order of y using CRT.
3. Calculate y.


The cardinality of integer mod p is p-1,
which is `2 * 3^2 * 7 * 13^4 * 47 * 103 * 107 * 151` in this task.
We can find the order of y in each subgroup and recover order of y,
just like what we do in
[pohlig-hellman](https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm).

To find a generator, we can use sage:
```python
G = IntegerModRing(0xfffffed83c17)
print(G.multiplicative_generator()) # 5
```
so our goal is to find `o = log_5(y)`.

Take the subgroup of cardinality of `7` as an example:
```
Let a = pow(y, (p-1) // 7, p)
Find i such that
pow(5, (p-1) // 7, p) = pow(a, i, p)
which means
o * i % 7 = 1
so o % 7 = inv(i, 7)
```
`i` is in the range of (0, 7),
it takes at most 7 operations to find `i`.

There's one case that we can't find such `i`: `a = 1`,
which actually means `o % 7 = 0`.


For subgroup 9:
```
Let o3 = o % 3
Let a = pow(y, (p-1) // 3, p)
Let b = pow(y, (p-1) // 9 * inv(o3, 3), p)
Find i such that
pow(5, (p-1) // 7, p) = b * pow(a, i + 1, p)
which means
o * i % 9 = 1
so o % 9 = inv(i, 9)
```
In the case that `o % 3 == 0`, try again with different y.

To do the exponentiation efficiently,
we can calculate it by [squaring](Exponentiation_by_squaring).
and cache those squares.

Once we find the order in each subgroups,
we can calculate `o` using [CRT](https://en.wikipedia.org/wiki/Chinese_remainder_theorem).
and `y = pow(5, o, p)`.

Here's the [script]([_files/solve.py]).
