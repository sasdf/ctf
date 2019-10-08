---
name: plam
category: reverse
points: 1000
solves: 1
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}

> I tried my best, but it's still a little bit slow.
> It will tell you the result after several years.


# Overview, Concept and Design Criteria
I'm a big fans of lambda calculus. It's pretty beautiful.
Three simple rules but pretty powerful.

Initially, I was trying to wrote this task with python's lambda.
However, I can't construct one of the most mind-blown stuff -- fixed point operator,
and it's also difficult to curry those lambdas.

plam works well before I switched to postfix representation.

Postfix representation looks pretty great,
I have no choice but implement a interpreter by myself to verify the challenge.

## Designed Criteria
The core of this flag checker is a system of GF2 (i.e. boolean) linear equations.
To avoid it to be guessed, I generate product of 4 sums in each run.
So only 1/16 of results will be true, which make blackbox analysis much harder.
And also make the code more complicated 😈 .

Also, I don't want it to be solved with z3 after you convert those things to boolean operations,
so I added some branches to it.
The complexity will explode for z3.


# Solution
Will be released 72 hours after the end of competition.
