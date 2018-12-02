---
name: LFSR StreamCipher
category: crypto
points: 500
solves: 3
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}

> [Task Description](./task.md)

## Time
Solved after the CTF with a lot of help from the admin (@asante).


# Solution
In this challenge,
we have a LFSR, a non-linear filter of algebraic degree 6, and its first 1001 outputs.
Our goal is to recover its initial seed.

For LFSR clock $$L$$ and filter $$f$$, the outputs $$b_i$$ are:
$$
\begin{aligned}
f(s) &= b_0\\
f(L(s)) &= b_1\\
f(L^2(s)) &= b_2\\
& \cdots \\
f(L^n(s)) &= b_n\\
\end{aligned}
$$
Degree of these equations are too large, it is infeasible to solve $$s$$ directly.
We need to lower the degree to solve $$s$$,
and here comes the idea of annihilators:
annihilator $$g$$ of $$f$$ with is:
$$
\begin{aligned}
&
    \forall x: f(x)g(x) = 0 \\
\implies&
    \forall x \in \{z\ |\ f(z) = 1\}: g(x) = 0 \\
\end{aligned}
$$

If we can find a function g with lower degree,
we can solve for following system of equations instead:
$$
    g(L^i(s)) = 0 \quad \forall i: b_i = 1
$$

We can find such function using sage:
```python
from sage.crypto.boolean_function import BooleanFunction
B = BooleanPolynomialRing(6, ['x0', 'x64', 'x96', 'x128', 'x192', 'x255'])
x0, x64, x96, x128, x192, x255 = B.gens()
p = x0*x64*x96*x128*x192*x255 + ... + x128*x192*x255
f = BooleanFunction(p)
print(f.annihilator(f.algebraic_immunity()))
# output x0 + x1 + x2 + x3 + x4 + x5 + 1
# which means x0 + x64 + x96 + x128 + x192 + x255 + 1
```
Now we have a great linear annihilator.

For more about annihilator, algebraic immunity, and algebraic attack on LFSR,
see [this awesome slide](https://pdfs.semanticscholar.org/a787/7b314149d4c70f9c53f60967c20683f6625a.pdf).

To solve the system of equations,
we can express the LFSR in [matrix form](https://en.wikipedia.org/wiki/Linear-feedback_shift_register#Matrix_forms),
apply our annihilator $$g$$ on the matrix,
and solve for $$s$$, formally:
$$
\begin{aligned}
\text{Let}\ 
    h &= x^{0} + x^{64} + x^{96} + x^{128} + x^{192} + x^{255}\\
    L &= \left(\begin{matrix}
      0      & 1      & 0      & \cdots & 0   \\
      0      & 0      & 1      & \cdots & 0   \\
      \vdots & \vdots & \vdots & \ddots &     \\
      0      & 0      & 0      & \cdots & 1   \\
      c_0    & c_1    & c_2    & \cdots & c_n \\
    \end{matrix}\right) \\
\end{aligned}
$$
$$
\begin{aligned}
&
    g(L^i(s)) = 0 \quad & \forall i: b_i = 1 \\
\implies&
    h(L^i(s)) + 1 = 0 \quad & \forall i: b_i = 1 \\
\implies&
    h(L^i(s)) = 1 \quad & \forall i: b_i = 1 \\
\implies&
    (hL^i)s = 1 \quad & \forall i: b_i = 1 \\
\implies&
    \left(\begin{matrix}
      hL^{i_0} \\
      hL^{i_1} \\
      hL^{i_2} \\
      \vdots \\
      hL^{i_n} \\
    \end{matrix}\right) s 
    =
    \left(\begin{matrix}
      1 \\
      1 \\
      1 \\
      \vdots \\
      1 \\
    \end{matrix}\right)
    \\
\end{aligned}
$$

[Solving]([_files/solve.sage]) for $$s$$ yields 4 solutions:
```
[+] Generated 293 equations
[+] Solution 0: ')A\x17U\xaf\x9d\x18\xbcn[\xed\x8aj\x00\xbc\xd4\xb39\xe1ef\xe7~/\xaa\xf2\xd7\x9e\x99\xdf\xc6j'
[+] Solution 1: 's\xf0Z\xea\x07\xa2\xc5H\xba\x1c*\xa5\x82_X\xf2\x1c\xfe\xd5\xb3\x11A%\xf0\x92\x0c\x8c\xbawa\x83w'
[+] Solution 2: '<\xdd,\xd8\xd3l\xa9\xa6\xe7s\xaap\xabn\xb4N\x9c\x95k\x97\x19\xc82\xb7\t\x92:P\xdd\xfad`'
[+] Solution 3: 'flag{StR34m_C1Ph3R_Annih1lat3D!}'
```
