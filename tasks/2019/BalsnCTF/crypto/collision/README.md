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
Will be released 72 hours after the end of competition.
