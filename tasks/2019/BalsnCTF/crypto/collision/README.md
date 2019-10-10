---
name: collision
category: crypto
points: 726
solves: 8
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}

> md5 is broken, sha1 is broken, but our authenticator survives.


# Overview, Concept and Design Criteria
This challenge is inspired by some real world applications that use both sha256 and crc32 for password hashing,
which totally ruined sha256.

Assuming feasible password length for bruteforcing sha256 with personal computation resource is 40 bits (or 5 bytes),
you can crack 72 bits (or 9 bytes) password with "help" from crc32!!!

It's longer than most of the password's minimum length limit.

I kept some of the features when designing this challenge:
* Scare people away with a non crackable hash 😈.
* Require some bruteforce to recover the input.
* Salted hash (i.e. pre/postfix).

## Fun facts
* This is the first solved non-trivial challenge.

# Solution
The task has several files,
Let's take a look at the entrypoint `main.py` first.

## Break md5 with 10000000000 cores ?!?!
After you open `main.py`, you will see something like:
```python
passwd = input('Password: ')

# ...

if hashlib.md5(passwd).hexdigest() != 'cd86c62d1c8d808a96e49511e0b79158':
    print(youShallNotPass)
    exit(255)

print('Enjoy your flag :)')
printflag(passwd)
```
This is the spirit of this challenge :)

Checking md5 hash at the very beginning is scary,
it seems impossible to solve at first glance.

But it's not.

## More hashes
If you look into `printflag`, you'll find that it calls `omnihash` to generate more hashes to check,
including non-cryptographic secure hashes -- CRC family.

BTW, There're some unnecessary encryption before hashing,
Those things are just for adding entropy and pre/postfix (i.e. salt) to the flag.

## CRC
CRC is just polynomial quotient,
A straight forward solution is CRT.

It was the solution for prior version of this challenge,
but it's not powerful enough to solve this one.

Actually, It's a linear operator (i.e. matrix) in $$\mathbf{GF}(2)$$ vector space.

Assuming all input feed into CRC are $$n$$-bits long,
we can express $$k$$-bits CRC function as following in $$\mathbf{GF}(2)$$ polynomial quotient ring:
$$
\begin{aligned}
     s &:= \sum_i^n a_i x^i \\
\text{CRC}(s) &:= s x^k + \text{bias}  \mod \text{poly} \\
\end{aligned}
$$
where $$a_i$$ is bits of input we want to hash.

Bias in the equation is annoying.
Fortunately, we can remove it by simply xoring with $$\text{CRC}(0)$$.

To make our equation cleaner, we assume that all CRC don't have bias below.

## GF(2) Vector Space
Let's reformulate the definition of CRC:
$$
\begin{aligned}
\text{CRC}(s) &= s x^k  &\mod \text{poly} \\
       &= (\sum_i^n a_i x^i) x^k  &\mod \text{poly} \\
       &= \sum_i^n a_i x^i x^k  &\mod \text{poly} \\
       &= \sum_i^n a_i \ \text{CRC}(x^i)  &\mod \text{poly} \\
       &= \sum_i^n a_i \ \text{CRC}(x^i) & \\
       &= M a & \\
\end{aligned}
$$

Those CRC in the equation are all known constants,
So it becomes matrix multiplication, where each column of $$M$$ is the checksum of each bit.

We have many different variant of CRC in this task.
Combine all of them by concatenating the matrix (and result),
and solve that large matrix equation can recover the input.

There's one more thing, remember that we have pre/postfix?
It can be seperated from the variables as a constant,
and we can just subtract them.

The linear system has multiple solution.
Fortunately, we also has some other hashes like md5 that we can check which one is correct.

You can find full exploit [here]([_files/solution/solve.py]).
