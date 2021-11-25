---
name: Share the flag
category: crypto
points: 520
solves: 1
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> We want to share the flag with you.


# Overview, Concept and Design Criteria
> We need some lattice challenges.

So here it is.

The target of a lattice challenge needs to have some linear structure,
and something secret must be short.
One famous example is the biased ECDSA,
but there are already toooo many challenges about it.

When I preparing a crypto handout,
I found a topic on Wikipedia -- Secret Sharing.

Oh! Polynomial! Sounds like a good target.

There are two key points in the design:
1. Remove part of the variables from the lattice, and this one failed :(
2. Center the target vector to make it short.


# Solution
[The server]([_files/challenge/chall.py]) will create a 32-degree polynomial under Zmod(251).
The first 16 coefficients are static secrets, and the remaining 16 coefficients are random lowercase letters.
And the server will give us 15 (x, y) pairs.

Apparently, we don't get enough information in a single connection.
Since the secret is the same, we can collect the data many times.
Each dataset will add `4.7 * 16 = 75` unknown bits, while we receive `8 * 15 = 120` bits.

We can't solve the system of equations directly because it's underdetermined.
However, we know that many variables have only 26 possibilities (i.e. lowercase letter).
Lattice reduction can find some short vectors (with respect to L2 norm) in a lattice.
There are still two problems in our system:
1. The first 16 coefficients (i.e. flag part) are not short.
2. The value of these random lowercase letters is not small too (i.e. 97 ~ 122).

After constructing the lattice,
we can simply discard the first 16 columns (i.e. flag part).

@rkm0959 reported
[another solution](https://github.com/rkm0959/Inequality_Solving_with_CVP/tree/main/Example%20Challenge%207%20-%20ACSC%20Share%20The%20Flag):
We can rescale each dimension.

To deal with the second issue, we have to center our vector.
Remapping (97 ~ 122) to (-12, 13),
the vector is quite short in our lattice.
We can use a lattice reduction algorithm such as BKZ to find it,
and then solve the linear system to recover the flag.

You can find our full exploit [here]([_files/solution/solve.sage]).


# Previous version
In the first version of this challenge, we let the user choose the threshold in [18, 32].
The server will return at most `threshold - 17` (x, y) pairs.

I thought choosing a smaller threshold only reduce the information we get,
so there is no reason to choose any other threshold than 32.

But @rbtree found a brilliant solution:
By selecting the threshold to be 18, the two random coefficients won't cover all 251 cases.
We won't get certain outcomes from the polynomial.
We can test all possible two random coefficients and recover the evaluation result of the flag part only.

His exploit can be found [here]([_files/v0/v0.py]).
