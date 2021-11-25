---
name: 1337 pins
category: crypto
points: 422
solves: 5
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> [100 digits pin](https://ctftime.org/task/14035) are still too weak... How about 1337 of them?


# Overview, Concept and Design Criteria
This challenge is based on a real-world application.
In BalsnCTF 2019, we've dealt with PRNG using rejection sampling.
This year, we've covered another common pattern -- PRNG with a mod.

One day, @kevin47 found some vuln and asked us if it is possible to break the MT19937 given its output mod some integer, say 10.
MT19937 is linear under GF2 vector space, but modulo messed up the relationship completely.
The first thing I thought of is modulo power of two, for example, 2^16.
But I rejected this idea instantly because it's too ... CTF, too artificial to be a realistic challenge.

On my way home, I suddenly realized that half of the integers have a factor of 2, even the example he gave us is!
And this challenge borns.


## Fun facts
* This is the first solved crypto challenge.


# Solution
[The code]([_files/deploy/src/server.py]) is very short.
The server generates random digits using `random.getrandbits(32) % 10`.
We can guess 31337 times, and the server will tell us the answer if we send a wrong number.
The goal is to make 1337 correct guesses continuously.

CPython's random use [MT19937](https://en.wikipedia.org/wiki/Mersenne_Twister#Algorithmic_detail) internally,
it is linear under GF2 vector space (i.e. Bit vector with xor and shift).

The modular operation messed up the linearity.
Fortunately, modular arithmetic has the following property:

$$
\begin{aligned}
    & (a \mod mn) \mod n\ =\ a \mod n \\
\implies
    & (a \mod 10) \mod 2\ =\ a \mod 2
\end{aligned}
$$
That is, we get the last element in the output GF2 vector.

We can reconstruct the state by solving the linear equations.
There are 19937 equations and 19968 variables.
The matrix is quite large and you might run out of time.
We have three possible ways to make it faster:
1. I simply take the solver from [BalsnCTF 2019]([_files/solution/mt/]), it use gaussian elimination and implemented in C++.
2. @Utaha [has reported](https://utaha1228.github.io/ctf-note/2021/11/21/BalsnCTF-2021/) that using python's large number is also possible.
3. Our verifier, @jwang, use a pre-computed inverse matrix since the relation is always the same.

You can find our full exploit [here]([_files/solution/solve.py]).
