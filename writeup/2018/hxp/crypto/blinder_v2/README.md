---
name: blinder_v2
category: crypto
points: 350
solves: 0
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> Please hack.


## Time
A day


# Behavior
Same as blinder, but I found a more efficient solution for this particular $$p$$.
It takes about 4500 operations to work (c.f. 13000 operations using elliptic curve).

The previous solution using elliptic curve is more general.
This solution won't work if you select a prime with non-smooth factorization for $$(p^d-1) / (p-1)$$.


# Solution
## TL;DR
1. Work under the polynomial quotient ring of modulo $$x^2 + 1$$.
2. Recover the partial index of $$y$$ using Pohlig-hellman.
3. Calculate $$y$$.

Note: If you haven't read our [previous solution](../blinder/) using elliptic curve,
read it first.
The concepts are similar, and I also applied most of the optimizations here.

After the previous solution is finished,
I try to figure out how elliptic curve punch some holes in that field,
creating a shrinking map to a smaller subgroup which has a smooth order.

Some points not on the curve seems to be the reason,
but I still don't know how these things actually works,
so let's skip this part.

Elliptic curve works really well on cryptography due to the hardness of its DLP.
But clearly, we don't need such thing in this task.
Maybe we can work on another simpler structure than elliptic curve.

Here it is: Polynomial quotient ring !!


## Polynomial Quotient Ring
Let $$f$$ to be an irreducible polynomial over $$\mathbb{F}_p$$.
The order of multiplicative group in the quotient ring
$$(\mathbb{F}_p[x]/\langle f \rangle)^*$$ is $$p^2 - 1$$.
In this task, the order is actually
$$
2^4 \times 3 \times 5 \times 59 \times 281 \times 3037 \times 23293 \times (p-1)
$$
, which is almost smooth except for the last factor.


## Recover part of the index
It won't be too hard to recover the index of a polynomial in each subgroup except last one.
$$3037$$ and $$23293$$ is a little bit large, so we need to use baby step giant step here.
Luckliy, multiplication of polynomial doesn't cost too much operations.


## Reconstruct y
Clearly, there's no efficient way to recover the index in $$(p-1)$$ subgroup using oracle only.
But we don't need to know that, we already have enough information to reveal what $$y$$ is.

Let's think about what that $$(p-1)$$ subgroup is?

It's a group of all constants (i.e. degree 0 polynomials).

So here's how we reveal $$y$$.
$$
\begin{aligned}
 Y      &= yx + 1 \\
 o      &= \log_g(Y) \\
 o'     &= o \mod (p+1) \\
 g^{o'} &= ax + b \\
 Y      &= g^o \\
        &= g^{o' + k(p-1)} \\
        &= g^{o'} \times g^{k(p-1)} \\
        &= (ax + b) \times c^k \\
        &= (a \times c^k) x + (b \times c^k) \\
        &= (a \times b^{-1}) x + 1 \\
        &= yx + 1 \\
\end{aligned}
$$

And here's our new [script]([_files/solve.py]) :)
