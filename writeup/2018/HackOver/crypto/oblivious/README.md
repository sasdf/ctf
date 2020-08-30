---
name: oblivious transfer
category: crypto
points: 500
solves: 1
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> We do not do parties, we do multi-parties!
> One of the most important ingredients for these is (next to mate) oblivious transfers.

## Time
3 hours  
Solved 1 hour after the ctf end :(

## Behavior
The server use paillier cryptosystem,
we can provide generator $$c$$ and publickey $$n$$,
then the server computes a encrypted flag using following formula.
$$
\begin{aligned}
x_0 &= \text{rand}(\text{sizeof}(\text{flag}))\\
x_1 &= x_0 ^ \text{flag}\\
r_0, r_1 &= \text{rand}(n), \text{rand}(n)\\
c_0 &= \left(\text{enc}(1) \times c^{(n-1)}\right)^{x_0} \times c^{r_0}\\
c_1 &= \left(\text{enc}(1) \times c^{(n-1)}\right)^{r_1} \times c^{x_1}\\
\end{aligned}
$$
and returns ciphertext $$c_0, c_1$$ to us.

# Solution
## TL;DR
1. Generate a safe prime $$q = 2p + 1$$
2. Use $$n = pq$$ as public key
3. Send $$\text{enc}(q)$$ as $$c$$
4. $$x_0 = \text{dec}(c_0) \ \mod\ p$$
5. $$x_1 = \text{dec}(c_1) \ \mod\ q$$

In paillier, multiplication in ciphertext is addition in plaintext,
and power in ciphertext is multiplication in plaintext.
So the decryption result will be:
$$
\begin{aligned}
c   &\coloneqq \text{enc}(z) \\
d_0 &= x_0 - z (x_0 - r_0)\ \mod\ n \\
d_1 &= r_1 - z (r_1 - x_1)\ \mod\ n \\
\end{aligned}
$$

To solve this task, I use a safe prime as $$c$$ and private key, formally:
$$
\begin{aligned}
q &\coloneqq 2p + 1\quad\text{where p, q are both prime} \\
n &\coloneqq p q \\
c &\coloneqq enc(q) \\ \\
\end{aligned}
$$
After decryption, we'll have:
$$
\begin{aligned}
d_0 &= x_0 - q (x_0 - r_0)\ \mod\ pq \\
d_1 &= r_1 - q (r_1 - x_1)\ \mod\ pq \\
\end{aligned}
$$
To get $$x_0$$, simply calculate the remainder over $$q$$:
$$
d_0 = x_0 - q (x_0 - r_0) = x_0\ \mod\ q
$$

$$x_1$$ is more complicated.
Recall that $$q = 2p+1$$, we can derive following formulas:
$$
\begin{aligned}
r_1 &\coloneqq p k + (r_1\mod\ p) \\
d_1 &= r_1 - q (r_1 - x_1)\ \mod\ pq \\
    &= r_1 - q (p k + (r_1\mod\ p) - x_1)\ \mod\ pq \\
    &= r_1 - p q k - q ((r_1\mod\ p) - x_1)\ \mod\ pq \\
    &= r_1 - q ((r_1\mod\ p) - x_1)\ \mod\ pq \\
    &= r_1 - (2p + 1) ((r_1\mod\ p) - x_1)\ \mod\ pq \\
    &:\ \text{\{Under modulo p\}} \\
    &= r_1 - (2p + 1) ((r_1\mod\ p) - x_1)\ \mod\ p \\
    &= r_1 - 1 ((r_1\mod\ p) - x_1)\ \mod\ p \\
    &= r_1 - (r_1\mod\ p) + x_1\ \mod\ p \\
    &= x_1\ \mod\ p \\
\end{aligned}
$$

Now xor those two integer to get the flag.

# Additional Notes
Here's the [solution](https://gist.github.com/qr4/9c2cebc7af7b68908716e516fc5fbfa2) from admin.
It is stronger than my solution which doesn't need the assumption of safe prime on private key.
Here's a proof about how it works:

Using extended gcd to get X, Y, such that:
$$
pX + qY = \text{gcd}(p, q) = 1
$$

Using the equation above,
we have following equation about multiplicative inverse:
$$
\begin{aligned}
&\frac{1}{pX} \times pX = 1 = pX + qY \\
\Rightarrow\ &\frac{1}{pX} = \frac{pX + qY}{pX} = 1 + \frac{qY}{pX} \\
 \\
&\frac{1}{qY} \times qY = 1 = pX + qY \\
\Rightarrow\ &\frac{1}{qY} = \frac{pX + qY}{qY} = 1 + \frac{pX}{qY} \\
\end{aligned}
$$

Select $$c = \text{enc}(\alpha)$$, where
$$
\alpha = pX \mod pq
$$

So that:
$$
\begin{aligned}
d_0 &= \text{dec}(c_0) \\
    &= x_0 - \alpha (x_0 - r_0) \mod pq \\
    &= x_0 - pX (x_0 - r_0) \mod pq \\
    &:\ \text{\{under modulo p\}} \\
    &= x_0 - pX (x_0 - r_0) \mod p \\
    &= x_0 \mod p \\
\end{aligned}
$$

However the script calculate $$x_0$$ using:
$$
x_0 \coloneqq \frac{d_0}{qY} \mod p
$$
which is also true.

$$
\begin{aligned}
\frac{d_0}{qY} &= \frac{x_0}{qY} \mod p \\
               &= x_0 (1 + \frac{pX}{qY}) \mod p \\
               &= x_0 \mod p \\
\end{aligned}
$$


We can calculate $$x_1$$ from $$d_1$$ in the similar way:
$$
\begin{aligned}
d_1 &= \text{dec}(c_1) \\
    &= r_1 - \alpha (r_1 - x_1) \mod pq \\
    &= r_1 - pX (r_1 - x_1) \mod pq \\
 \\
\frac{d_1}{pX} &= \frac{r_1}{pX} - r_1 + x_1 \mod pq \\
               &= r_1 (1 + \frac{qY}{pX}) - r_1 + x_1 \mod pq \\
               &:\ \text{\{under modulo q\}} \\
               &= r_1 (1 + \frac{qY}{pX}) - r_1 + x_1 \mod q \\
               &= r_1 - r_1 + x_1 \mod q \\
               &= x_1 \mod q \\
\end{aligned}
$$
