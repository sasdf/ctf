---
name: blinder
category: crypto
points: 350
solves: 0
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}

> Please hack.


## Time
8 hours  
Solved after the CTF ended, with @tjbecker (PPP)


# Behavior
Same as blinder, but the order of GF(p) isn't smooth anymore.


# Solution
## TL;DR
1. Search a elliptic curve with smooth order
2. Recover the index of y using Pohlig-hellman.
2. Recover the index of y in each subgroup with naive discrete log.
3. Calculate y.


After the CTF ended,
there's some discussion of this challenge.
```
 00:29    hellmann| for blinder my guess would be to construct an elliptic curve with small factor in the order and perform dlp there,
                    using oracle operations to implement the ecc group
 00:29      _0xbb_| you need to discuss that with y7 later^^
 00:30    hellmann| looking forward :)
 00:42    tjbecker| hellmann: that was my approach, but I couldn't get it down to only 0x4000 queries
 00:43    tjbecker| would love to see what optimizations I was missing, if that was the intended solution
 00:43    hellmann| how close could you get?
 00:44    tjbecker| I needed roughly 0x20000, which is 8x too many
 00:45    hellmann| still sounds cool, how many curves did you use? what were the factors
 00:47    tjbecker| a,b = (242251381217038, 29739910446124)
 00:47    tjbecker| gives a curve of order 2 * 3 * 11 * 13 * 17 * 67 * 71 * 131 * 173 * 179
 00:48    tjbecker| (which is also nice because it's square free)
 00:48    hellmann| nice, I thought about using many curves
 00:48    tjbecker| maybe that's what I was missing
 00:48    hellmann| maybe with montgomery arithmetic it should be good enough?
 00:48    tjbecker| more liekly, I was just bad at optimizing point addition
 00:50    tjbecker| yeah I also thought about using Edwards curves, but got too tired to stay up to try it
 00:50    tjbecker| I was happy enough with a solution which was much better than sqrt(p)
 01:01       sasdf| tjbecker: How do you construct that curve?
 01:02    tjbecker| just try random (a,b) pairs, constructing the curve over GF(p) and take the one with the smoothest order
 01:02    tjbecker| took like 10 minutes to find that curve
```

The method using Elliptic curve sounds promising.
After @tjbecker gave me his script, we work on optimizing the algorithm together.

Here's the summary of our algorithm:
* Let C = EllipticCurve, T = Target y, G = Generator, o = C.cardinality().
* Calculate `P = C.lift_x(T)`.
* Similar to what we do in `blind`, For each factor f in o:
    * Calculate `X = (o / f) G`
    * Calculate `Y = (o / f) P`
    * Find `i` such that `i X = Y`, which means `P.order() % f = i`.
* Reconstruct `P.order()` using Pohlig-Hellman algorithm.
* Calculate T


## Embed integer
We can't encrypt arbitary integer directly.
We need to construct them using 1 and add operation.

First, we calculate a list of power of two (using double and 1),
and we can sum those needed bits to construct arbitary number.


## Offline calculation of operation on G
This is our first optimization.

Operation on the elliptic curve is much more expensive than embedding an integer,
so we calculated all operation about the generator
(i.e. `X = (o / f) G` and `i X`) offline,
and then embed the result using previous algorithm.

For comparsion between `i X` and `Y`,
we only compare their y coordinate.


## NAF form
For square-and-multiply (or double-and-add),
we use
[NAF form](https://en.wikipedia.org/wiki/Non-adjacent_form)
instead of typical binary form to minimize the operation count.


## Merge order
When calculating double-and-add,
we have to sum a list of numbers.
If we sum them sequentially:
```
result = reduce(add, points, zero)
```
We (almost) won't hit the cache in add operation.

Instead, we add up neighbors first:
```
a, b, c, d, e, f, g -> (a+b), (c+d), (e+f), g
```
We will have a better chance that hit the cache at first round.

For Point multiplication (i.e. `Y = (o / f) P`),
we know all the operands in advance.
We use a greedy algorithm: add up most common pair first.
It's not optimal, but much better then merging neighbors first.
```
A = 0, 1, 2
B = 0, 1, 3
C = 0, 1, 4, 5, 6
D = 5, 6
With following order:
Add(0, 1), Add(5, 6), Add(01, 2), Add(01, 3), Add(01, 4), Add(014, 56)
```


## Constant power
There're two operation using constant power:
* `inv = exp(x, p-2)`
* `sqrt = exp(x, (p+1)/4)`
`p-2` is a very bad constant when using square-and-multiply,
because of it's binary representation: `111111111111111111111111111111111110101101001111`.
We have to sum all those 1 and that is a huge amount of operations.

Fortunately, we cat factor `p-2` to `123 * 2288414444759`,
which means we can calculate `exp(exp(x, 123), 2288414444759)` instead.

And we can apply similar techniques to `sqrt` too.


## Linear search v.s. Baby Step Giant Step
tjbecker implemented Baby Step Giant Step too.
The algorithm has lower complexity,
but it needs to run point addition `sqrt(f)` times,
which needs too much operations.

A better curve with linear search works better.


## Search the curve
After we finish our algorithm,
we can estimate the cost of each part:
* `Y = (o / f) P` takes about 2000 operations of each `f`.
* Comparing `iX` and `Y` takes about 24 operation of each test.
* Expectation of the needed tests to find `i` is `f / 2`.
We can use the cost for ranking curves when searching.
Here's the
[script]([_files/curvesearch.sage])
we use to search the curve.


## Flag
Now combining everything together,
It's time for getting our flag :)
Here's the [script]([_files/solve.py]).

It uses about 13000 operations on localhost.

...

So where's the flag?

`TimeoutError`

It seems that I have to find a server in Germany to get the flag...
