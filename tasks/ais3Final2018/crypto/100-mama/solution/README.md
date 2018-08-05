# TL;DR
Change a pair to (0, p - 2), swap them, and then undo the change.


# Overview, Concept and Design Criteria
This task is inspired by one of my favorite crypto challenge, 
[primitive from starCTF 2018](https://github.com/sixstars/starctf2018/tree/master/crypto-primitive),
and its [writeup from p4](https://github.com/p4-team/ctf/tree/master/2018-04-21-starctf/primitive).
The original challenge use ARX (add, rotate and xor) to construct arbitary permutation.
I suggest thinking of this challenge before continuing reading (It's very interesting).
I also provide a formulated solution of primitive in appendix at the bottom.

This task, mama, use multiplication and addition instead of ARX,
but the solution are very similar.
I also choose a large p (128 bits), 
so you need to find a way to construct it rather than bruteforce.


# Solution
There are two operations in this task:
* Multiplication in modulo group p, where 0 is mapped to p - 1.
* Addition in modulo group (p - 1).

Both operations are reversible.

As same as the solution of challenge primitive, we can seperate this challenge into three step:
1. Map (x, y) to (a, b).
2. Swap (a, b) and keep the rest of number as it was.
3. Undo the map.

There's no gadgets can swap (0, 1),
but there are two gadgets can swap (0, p - 2) and keep the rest of number as it was,
one of them is `(k / 2 + 1) * 2 - 2`.
Divide by 2 in the formula is actually multiply the multiplicative inverse of 2.
To map arbitary pair (x, y) to (0, p - 2), we can use the gadget `k / (x - y) - y`.

The number operation is limited to 777, and we have 120 constrains,
we can only use 6 operations for each constrain.
Adjacent additions can be merged to one addition,
similarly, adjacent multiplications can be merged too.
Our solution will in the form of `mul, add, mul, add ...`
(and this is where the name of this challenge comes from).


# Appendix - Solution for primitive
Inspired by the solution from p4, where they brute force the parameter of mapping in the form of `add, rol, xor, add`.
I find a way to construct the parameter:
1. If difference `x - y` between the pair `(x, y)` is odd, then
    1. Subtract `(x - y + 1) / 2`, so the pair becomes `(-k-1, k)`
    2. `-k-1` is actually `~k` (2's complement), so xor k turns the pair into `(-1, 0)`.
    3. Add one to turn it into `(0, 1)`.
2. If the difference is even, rotate a bit different between them to LSB.
