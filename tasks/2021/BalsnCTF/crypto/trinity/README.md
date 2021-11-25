---
name: trinity
category: crypto
points: 500
solves: 0
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> Everyone knows birthday paradox. It takes 2^32 to find a collision.
> To find another one, 2^32 * 2^32 == 2^64.
> I know math!! It is infeasible!!


# Overview, Concept and Design Criteria
Inspired by the `Re:Montagy` challenge in Real World CTF 3rd.
It is possible to calculate a 64bits hash collision in time `2^32` using a birthday attack.

I was using a large hash table for my meet-in-the-middle algorithm.
It takes 64G memory, 24 cores, and 15 minutes...

I was wondering if we can do better after the CTF.
I recall Pollard's rho method.
It uses a little memory and even runs faster (memory access is slower than computing),
but it only runs on a single core.
Searching on the net,
I found a parallelized version using distinguished points (aka lambda).
Finally, implementing it on a GPU dramatically reduce the running time,
it finished less than a second for searching 2-collision.

To make things more interesting, I made this task for searching three collisions.

So there are two goals of this challenge:
1. Understand how to implement a birthday attack efficiently.
2. Leverage the superpower of GPUs to search collisions.

We select blake3 as the hash function because it's fast,
and it's unlikely to have a method better than bruteforcing at the time.



# Solution
[The server]([_files/deploy/src/server.py]) requests for 3 collisions of 64bits blake3 hash.

## Birthday paradox
Using [Birthday attack](https://en.wikipedia.org/wiki/Birthday_attack),
we can find a pair of collision in `2^(n/2) = 2^32` attempts.
A naive implementation is creating a table recording all hashes,
and keep evaluating the hash function with random inputs until you find the collision.

When it comes to 3-collision, the complexity becomes `2^(n*2/3) = 2^43`.
It becomes impossible to use a naive approach, it would cost hundreds of TB memory/space for the table.
`2^43` would also take very long on CPU unless you have a huge cluster.

## 2-collision
### Pollard's rho algorithm
[Rho method](https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm)
is an O(1) memory approach. It doesn't use a table. Instead, it finds a collision to the evaluation chain.

Let's define a pseudorandom sequence: `x_{i+1} = hash(x_i)`,
and `x_0` can be anything, for example, all zero `00000000`.

All elements in the sequence only depend on the previous one.
If an element has appeared before, then the sequence will start looping.
It will look like the symbol ρ, a tail starting from `x_0` and a loop.

We will likely enter the loop after `2^(n/2)` evaluations.
Consider the case that first `2^(n/2)` evaluations are all unique,
then each evaluation after that will have 50% of chances collide with the value before.
It is as same as the table approach.

We can use Floyd's cycle-finding algorithm to determine the size of the loop,
derive the position of its collision,
and find the collision input by evaluating again from `x_0`.

But the evaluation is sequential. Can we use multiple cores?

### Lambda algorithm
Instead of finding a loop, parallelized pollard's rho method uses distinguished points.

Distinguished points are a set of points satisfying some condition.
We usually select the points with `k` leading zero bits as the distinguished points.

Our pseudorandom sequences will stop at a distinguished point.
Then we evaluate several sequences with different `x_0`.
When there is a collision, `a_i != b_i, a_{i+1} == b_{i+1}`, they will terminate at the same distinguished points.
These traces look like the symbol λ: two traces merge into one.

So the algorithm is:

1. Evaluate several sequences with different `x_0`.
2. Store their endpoint `x_n`, start point `x_0`, length `n` to a table.
3. When we find two traces have the same endpoint, evaluate again to check if they collide with each other.

The sequences can be evaluated in parallel, and we can leverage the full power of GPU.
The number `k` depends on the number of parallel tasks we can run concurrently.
Smaller `k` results in shorter traces, and we have to collect more traces (i.e. more parallelizable).


## 3-collision
If you know the lambda algorithm, it won't be too hard to adapt it for 3-collisions.
Instead of storing one trace per endpoint, we store a list of traces sharing the same endpoint.
After we collected enough traces, we can check whether three of them collide with each other at the same place.

There is even a paper for this from [Joux, 2009](https://eprint.iacr.org/2009/305).

### Checking collision
To check the collision of traces,
you might use a hash table for checking the states of all traces at each step.
It will work, but it is not friendly for GPU.

We use another approach: binary search.

These traces form a tree with the distinguished points as the root.
We cut the depth of the tree by half repeatedly until:
1. The tree has less than three leaves.
2. We find the 3-collision.

For a trace with length `n`, we will only evaluate the hash at most `n` times.
It has the same complexity as the table method but is more friendly for GPUs.

You can find our collider [here]([_files/solution/main.cu]).
