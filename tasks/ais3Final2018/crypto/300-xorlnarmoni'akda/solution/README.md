# TL;DR
Send a element in a small group and guess the shared secret.


# Overview, Concept and Design Criteria
The key vulnerability is small subgroup attack under multiplicative DHKE.
By sending a element in that small group,
there won't be too much possible shared secrets.

This is a simple modern crytographic challenge, which may deserve 100 points in normal CTF.
However, this challenge requires you to have some basic knowledge of number theory,
otherwise you won't even notice the existence of subgroup.
I also put some effort to make it more interesting to experienced crypto solvers,
such as introducing a guest account, PBKDF2, using flag as password,
and the most confusing one: obfuscation by a obsecure language.

## About the language
The description and the program of this challenge is written in Lineparine (リパライン語, 理語),
an artificial language created by Fafs F. sashimi.
The vulnerability is not related to the language,
so it is still solvable if you treat the source code as obfustrated.
It just sets the crytographic tone for the whole challenge perfectly :)

If you are interesting to the meanings, there's English translation in `translation.txt`.
I'm not a master of Lineparine, I guess there are many mistakes in this challenge.
If you know how to write in Lineparine fluently, please help me to improve the challenge :)

I spent about 10 hours designing this challenge, where 9 hours are used to translate to Lineparine LOL.


# Solution
You need to know some basic group theory.
* The order of finite field Zp over prime p is p - 1. [[Euler's totient function](https://en.wikipedia.org/wiki/Euler%27s_totient_function)]
* A prime number q dividing the order of G implies the existence of subgroup with order q. [[Cauchy's theorem](https://en.wikipedia.org/wiki/Cauchy%27s_theorem_\(group_theory\))]
* The order of every subgroup of G divides the order of G. [[Lagrange's theorem](https://en.wikipedia.org/wiki/Lagrange%27s_theorem_\(group_theory\))]

First we have to check whether [p is a prime](https://factordb.com/index.php?query=119323609506587624817542304473025422967730209036482647504046017790728908960293724554064575627723583087966477807950465152737206042053937640076702861135447697896288188327782825571921648597451715744592415597875243806851163720993697338643314116892802122805512134607232526059008942367872367039947556052857129781787).
And then find the order of Zp by [factorizing p - 1](https://factordb.com/index.php?query=119323609506587624817542304473025422967730209036482647504046017790728908960293724554064575627723583087966477807950465152737206042053937640076702861135447697896288188327782825571921648597451715744592415597875243806851163720993697338643314116892802122805512134607232526059008942367872367039947556052857129781786), you will get 2, 49391, and a large prime q.
So there's subgroup with order 2, 49391 and q.

The generator of order 2 subgroup is -1, which cannot be used in this challenge.

To find an generator of subgroup with order 49391,
you can select a random number r that is not 1 or -1,
and calculate g by `pow(r, (p - 1) / 49391) mod p`.
Order of g should be 49391 because `pow(r, p - 1) mod p = 1` according to Fermet's little theorem.
This method may output `1` with probability of `1 / 49391`, if you're too lucky to get `1`, try again.

The shared secret have only 49391 possible values.
You can check which one is correct using sha256 MAC inside the message.


# See also
Small subgroup attack is a very old but common mistake in DH/ECDH is not handled correctly,
and it still appears in modern softwares.
One most recently example is [CVE-2018-5383](https://www.cs.technion.ac.il/~biham/BT/) on Bluetooth pairing,
which use a invalid curve of order 2
(Strictly speaking,
it actually using another curve which has exactly same arithmetic operation rather than subgroup).
