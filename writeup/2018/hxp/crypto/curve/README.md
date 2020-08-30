---
name: curve12833227
category: crypto
points: 187
solves: 12
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> Apparently curves with numbers in their name are now cool, so I decided to make my own.


## Time
2 hours


# Behavior
We have the flag encrypted by key `x`,
and a point `xG` on the elliptic curve.


# Solution
## TL;DR
1. Recover the equation of the elliptic curve.
2. Map points on the curve to an multiplicative group.
3. Calculate discrete logarithm to find x.

The slope of the curve is
```
3x^2 + 4x+ 1 / 2y
compare to the derivative of y^2 = x^3 + cx^2 + ax + b
3x^2 + 2cx + a / 2y
E: y^2 = x^3 + 2x^2 + x + b
Evaluate on the point (4, 10), we found that b = 0
E: y^2 = x^3 + 2x^2 + x = x (x + 1)^2
```

That is a singular curve,
which is isomorphic to a multiplicative group.

Here's
[a great article](https://crypto.stackexchange.com/questions/61302/how-to-solve-this-ecdlp)
about how to solve discrete log on these curve.

First, we translate the curve to
```
y = x^2 (x - 1)
```
and find the square root of `-1`:
```
z^2 = -1 mod p
z = 189460722536962819362366221450020958767
f(x, y) = (y + zx) / (y - zx)
```
where f is an isomorphism from E to Fp.

And then we can get x by solving the discrete logarithm using sage:
```python
Fp = IntegerModRing(p)
g = Fp(f(Gx, Gy))
t = Fp(f(Tx, Ty))
x = t.log(g)
```
It takes several minutes to solve, and then we can decrypt our flag with `x` :)
