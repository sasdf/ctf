---
name: big maffs
category: rev
points: 250
solves: 28
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}

> Do you have enough memory?


## Time
5 hours+  
Most of the reversing work is done by my teammate @terrynini.


# Behavior
It's a binary that will calculate the flag.
But it needs enormous memory and time.


# Solution
## TL;DR
1. Reverse the binary
2. Find a isomorphism between that strange numeral system and $$\mathbb{Z}$$.
3. Calculate modular Ackermann function.
4. Reduce the exponent using euler's totient.

## Numeral system
The binary do some calculation of big integer with a strange numeral system,
When add two numbers,
the operation is similar to adding two binary integers.
However, the carry is `-1` instead of `1`.

The operation looks isomorphic to normal Interger Ring $$\mathbb{Z}$$,
$$
\begin{aligned}
X &= X + 1 - 1 \\
X &= X + 1 + 1 - 1 - 1 \\
X &= 1 + X - 1 \\
0 &= X - X = 1 - 1 \\
\end{aligned}
$$

Our teammate @qazwsxedcrfvtg14 generate a mapping of 0-256 in that numeral system,
And he figure out that we can transform the number to 256-based using that mapping.
```python
[
   0,    1,   -2,   -1,    4,    5,    2,    3,   -8,   -7,  -10,   -9,   -4,   -3,   -6,   -5,
  16,   17,   14,   15,   20,   21,   18,   19,    8,    9,    6,    7,   12,   13,   10,   11,
 -32,  -31,  -34,  -33,  -28,  -27,  -30,  -29,  -40,  -39,  -42,  -41,  -36,  -35,  -38,  -37,
 -16,  -15,  -18,  -17,  -12,  -11,  -14,  -13,  -24,  -23,  -26,  -25,  -20,  -19,  -22,  -21,
  64,   65,   62,   63,   68,   69,   66,   67,   56,   57,   54,   55,   60,   61,   58,   59,
  80,   81,   78,   79,   84,   85,   82,   83,   72,   73,   70,   71,   76,   77,   74,   75,
  32,   33,   30,   31,   36,   37,   34,   35,   24,   25,   22,   23,   28,   29,   26,   27,
  48,   49,   46,   47,   52,   53,   50,   51,   40,   41,   38,   39,   44,   45,   42,   43,
-128, -127, -130, -129, -124, -123, -126, -125, -136, -135, -138, -137, -132, -131, -134, -133,
-112, -111, -114, -113, -108, -107, -110, -109, -120, -119, -122, -121, -116, -115, -118, -117,
-160, -159, -162, -161, -156, -155, -158, -157, -168, -167, -170, -169, -164, -163, -166, -165,
-144, -143, -146, -145, -140, -139, -142, -141, -152, -151, -154, -153, -148, -147, -150, -149,
 -64,  -63,  -66,  -65,  -60,  -59,  -62,  -61,  -72,  -71,  -74,  -73,  -68,  -67,  -70,  -69,
 -48,  -47,  -50,  -49,  -44,  -43,  -46,  -45,  -56,  -55,  -58,  -57,  -52,  -51,  -54,  -53,
 -96,  -95,  -98,  -97,  -92,  -91,  -94,  -93, -104, -103, -106, -105, -100,  -99, -102, -101,
 -80,  -79,  -82,  -81,  -76,  -75,  -78,  -77,  -88,  -87,  -90,  -89,  -84,  -83,  -86,  -85,
]
```

For example, $$[171, 87]$$ becomes $$[-169, 83]$$ and 
$$
-169 + 83*256 = 21079
$$
We can verify that
$$
[171, 87] - 1 - 1 \cdots (21079) \cdots -1 = 0
$$

Here's the python util [script]([_file/code.py]) for that numeral system.

After the end of CTF,
the admin told us it is [base (-2)](https://en.wikipedia.org/wiki/Negative_base).

## Ackermann function
Now, we can calculate the flag with python's big interger than the strange and slow implementation in that binary.
However, it seems it will run forever.

The function is:
$$
A(m, n) = \begin{cases}
    n + 1 & \text{if } m = 0 \\
    A(m - 1, 1) & \text{if } m > 0 \text{ and } n = 0 \\
    A(m - 1, A(m, n - 1)) & \text{if } m > 0 \text{ and } n = 0 \\
\end{cases}
$$

When we evaluate the function at $$(m, 0)$$, it generate a sequence
$$
\{ 1, 2, 3, 5, 13, \cdots \}
$$
Searching it on [OEIS](https://oeis.org/A126333),
it turns out to be [Ackermann function](https://en.wikipedia.org/wiki/Ackermann_function).

There's a general form on the wiki, it's $$2 \uparrow^{(m-2)}(n+3) - 3$$.
We need the result of $$A(10, 10)$$, but it would be an enormous number.

Looking the binary again,
There's a mod operation before generate the flag.
So all we need to do is calculate
$$
A(10, 10) \mod 87582797363973712706510077042909217030082081478550617
$$

But how?


## Reduce with euler's totient
Euler totient has a property that:
$$
x^y \equiv x^{y + \phi(N)} \mod N \text{ (if x, y are coprimes)}
$$
Moreover, if $$y$$ is larger than $$\phi(N)$$, the congruence holds even if $$x, y$$ are not coprimes.

Next,
[Knuth's up-arrow notation](https://en.wikipedia.org/wiki/Knuth%27s_up-arrow_notation)
is defined as:
$$
a \uparrow^{n} b = \begin{cases}
    a ^ b & \text{if } n = 1 \\
    1 & \text{if } n \ge 1 \text{ and } b = 0 \\
    a \uparrow^{(n-1)} (a \uparrow^{n} (b - 1)) & \text{otherwise}\\
\end{cases}
$$

We can expand the notation as:
$$
a \uparrow^{n} b = a \uparrow ( a \uparrow^2 ( a \uparrow^3 \cdots - 1))
$$
Let $$B = a \uparrow^3 \cdots$$, B would be an enormous number.
$$
\begin{aligned}
a \uparrow^{n} b \mod N &= a \uparrow (a \uparrow^2 (B - 1)) \mod N \\
                        &= \text{pow}(a, a \uparrow^2 (B - 1)) \mod N \\
                        &= \text{pow}(a, a \uparrow^2 (B - 1) \mod \phi(N)) \mod N \\
                        &= \text{pow}(a, \text{pow}(a, a \uparrow^2 (B - 2) \mod \phi(\phi(N))) \mod \phi(N)) \mod N \\
                        &= \cdots \\
                        &= \text{pow}(a, \cdots \text{pow}(a, a \uparrow^2 (B - K) \mod 1) \cdots \mod \phi(N)) \mod N \\
\end{aligned}
$$
It gives us a interesting fact that when $$n$$ is large enough, the result only depends on the modulo, but not $$m, n$$.

With this expression, we can calculate those modulo using sagemath:
```python
from code import p
pp = p
mods = [p]
while True:
    pp = euler_phi(pp)
    mods.append(pp)
    print(pp)
    if pp == 1:
        break
# 87582797363973712706510077042909217030082081478550616
# 28482210524866574701450421812119154736221903390440960
# 5514075056689821860024092072671777577565348167680000
# ...
# 4
# 2
# 1
```

Then do the exponentiation.
```python
e = 0
rmods = mods[::-1]
for phi, m in zip(rmods, rmods[1:]):
    assert pow(2, phi + e, m) == pow(2, phi * 2 + e, m)
    e = int(pow(2, phi + e, m))
    print(e)
# 0
# 0
# ...
# 87279303242287529651724194363333093534246025526284328
# 6841904303386685743535095739352445371875467071891544
```

And don't forget to minus 3 for the final result :D
```python
from code import fromInt, flag
bytes(ai ^ bi for ai, bi in zip(fromInt(e-3), flag))
# b'PCTF{u_r_a_H4CKERMANN}\x02'
```
