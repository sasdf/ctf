---
name: Escape the Grid
category: crypto
points: 500
solves: 6
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf-tasks-writeup/)
{% endignore %}

> MCP: I've got a little challenge for you, Sark -- a new recruit.
> He's a tough case, but I want him treated in the usual manner.
> Train him for the games...
> let him hope for a while...
> and blow him away.
> 
> End of Line.

## Time
3 hours  


## Behavior
```
.. nc arcade.fluxfingers.net 1820
MCP: It is getting trickier all the time.
Challenge: 0x105ce1925567da883e769718264998a8666d5ad36474e71efc5db6761846f44ac3858d7dfdff17aa497477f1f31b9037a
Round number: 0
Request key stream block i
> 0
0x1fc5665b5135c2b7455563b6c5ec710930323182ef93ba7dd01e9d50f17a33c7d551735360246a5f682c8153190d1a564
Round number: 1
Request key stream block i
> 0
0x1fc5665b5135c2b7455563b6c5ec710930323182ef93ba7dd01e9d50f17a33c7d551735360246a5f682c8153190d1a564
Round number: 2
Request key stream block i
> 1337
0xe8d2d29840204c34c7fe463e1ab092986402b4383aeb602fbdfdb1237ca7d51fd6eeab8462b71baf245eef53cf692fd8
Round number: 3
Request key stream block i
```

First, the server give us a flag encrypted in this way:
```python
key = np.random.randint(0, 2, size=n)

def generate_challenge():
    hex(list_to_num(key) ^ int(hexlify(flag), 16))
```
Then we can ask for keystreams generate by rasta stream cipher:
```python
def generate_keystream_block(inputRound):
    block = rasta_standard(key, rounds=5, n=385, i=inputRound, matrix)
    return hex(list_to_num(block))
```


# Solution
## TL;DR
1. Get the keystream where no permutation is applied.
2. Get the keystream where the only permutation is shift left in last round.
3. Xor those keystream to eliminate the addition of key at last step.
4. Calculate the inverse to recover the key.


### Compress array to integer
```python
def rasta_standard(key, rounds, n, i=inputRound, matrix):
    cnt = i % factorial(n)
    cnt = (cnt + offset) % factorial(n)
    i = i / factorial(n)
    ...
    for _ in range(rounds):
        ...
        cnt += i % factorial(n)
        i = i / factorial(n)
        ...
        
def get_permutation(i=cnt, n):
    ...
    for k in range(n - 1):
        i = i % factorial(n - k)
        e = int(floor(i / factorial(n - k - 1)))
        ...

```
The round `i` of rasta is the permutation indices encoded to an integer.


### Rasta
```python
def rasta_standard(key, rounds, n, i, matrix):
    ... # cnt = decompress(i)[0]
    lin_layer = permutate_matrix(matrix, get_permutation(cnt, n), n)
    state = matrix_mul(key, lin_layer, n)
    for r in range(rounds):
        state = s_layer(state, n)
        ... # cnt = decompress(i)[r+1]
        lin_layer = permutate_matrix(matrix, get_permutation(cnt, n), n)
        state = matrix_mul(state, lin_layer, n)
    state = add_state(state, key, n)
    return state
```
It's a normal rasta cipher,
with a non-secure function for generating the affine transformation.
The [paper of rasta](https://eprint.iacr.org/2018/181.pdf) says:
> We propose to generate the different matrices and round constants
> with the help of an extendable-output function (XOF)
> that is seeded with the number of rounds r, block size n, nonce N, and i.
> 
> To ensure that the permutation is secure,
> we expect the XOF to behave like a random oracle up to a certain security level.
> For instance, it should not be feasible for an attacker to find inputs to the XOF
> for outputs of the attacker's choice except by repeatedly querying the XOF for
> different inputs. Furthermore, the internal state of the XOF should be large
> enough so that internal collisions within its state are prohibited.
> A suitable choice for an XOF would be for most instances SHAKE256.

In this task,
the affine transformation is generate by permutating the columns of a
hardcoded non-singular matrix using our input, and the constant is zero.
It is easily to construct a input `i` which results in our desired permutations.

Affine transformation and s layer (i.e. $$\chi$$-transformation) are invertible,
the only non-invertible operation is the addition of key at last step.


## Eliminate the addition of key
To eliminate the addition,
we can add up two keystreams because it's in $$\textrm{GF}(2)$$.
Furthermore, if the last permutation is the only difference of those two keystream:
$$
\begin{aligned}
    \text{ks}_A
        &= M_A \chi(M_1 \chi(M_2 \chi( \cdots \chi(M_r \text{key}) \cdots ))) \oplus \text{key} \\
    \text{ks}_B
        &= M_B \chi(M_1 \chi(M_2 \chi( \cdots \chi(M_r \text{key}) \cdots ))) \oplus \text{key} \\
    \text{ks}_A \oplus \text{ks}_B
        &= (M_A \oplus M_B) \chi(M_1 \chi(M_2 \chi( \cdots \chi(M_r \text{key}) \cdots ))) \\
\end{aligned}
$$
Then we can invert the operations to recover the key.


## Inverse of M_A + M_B
Unfortunatly, $$(M_A \oplus M_B)$$ is always a singular matrix.
(See the proof in Appendix A)
But we can build a matrix which is almost invertible.
Select permutation of $$M_A$$ as identity,
and permutation of $$M_B$$ as shift left, we get:
```
[1 0 0 0 0 0 0 0 0 1]
[1 1 0 0 0 0 0 0 0 0]
[0 1 1 0 0 0 0 0 0 0]
[0 0 1 1 0 0 0 0 0 0]
[0 0 0 1 1 0 0 0 0 0]
[0 0 0 0 1 1 0 0 0 0]
[0 0 0 0 0 1 1 0 0 0]
[0 0 0 0 0 0 1 1 0 0]
[0 0 0 0 0 0 0 1 1 0]
[0 0 0 0 0 0 0 0 1 1]
```
and the reduced echelon form of the augmented matrix is:
```
[1 0 0 0 0 0 0 0 0 1  |  0 1 1 1 1 1 1 1 1 1]
[0 1 0 0 0 0 0 0 0 1  |  0 0 1 1 1 1 1 1 1 1]
[0 0 1 0 0 0 0 0 0 1  |  0 0 0 1 1 1 1 1 1 1]
[0 0 0 1 0 0 0 0 0 1  |  0 0 0 0 1 1 1 1 1 1]
[0 0 0 0 1 0 0 0 0 1  |  0 0 0 0 0 1 1 1 1 1]
[0 0 0 0 0 1 0 0 0 1  |  0 0 0 0 0 0 1 1 1 1]
[0 0 0 0 0 0 1 0 0 1  |  0 0 0 0 0 0 0 1 1 1]
[0 0 0 0 0 0 0 1 0 1  |  0 0 0 0 0 0 0 0 1 1]
[0 0 0 0 0 0 0 0 1 1  |  0 0 0 0 0 0 0 0 0 1]
[0 0 0 0 0 0 0 0 0 0  |  1 1 1 1 1 1 1 1 1 1]
```
We will get two different input by setting the last bit to 0 and 1.


# Inverse of chi-transformation
The transformation is almost invertible.
We can calculate the inverse in mathematical way (See Appendix B),
but we have a much simpler way.
$$
\begin{aligned}
    &
        \chi(x)_i \coloneqq x_i \oplus x_{i+1}' x_{i+2} \\
    \implies &
        x_i = \chi(x)_i \oplus x_{i+1}' x_{i+2} \\
\end{aligned}
$$
We can try all 4 possibilities of the first two bits,
reconstruct the whole vector,
and check it is consistent to our guess.


# Recover the flag
After we reconstruct two possible keys,
xor with our flag and select the ascii one.

If this is a task that only has one chance to submit the key,
you can run the whole process again with different first permutation,
and find the common one in both runs.


# Appendix A: Prove of singularity
We can write the permutation as matrix $$P_1, P_2$$.
With distributive property:
$$
    M P_1 \oplus M P_2 = M (P_1 \oplus P_2)
$$
Every row in $$P_1, P_2$$ has exactly one 1.
Every row in $$P_1 \oplus P_2$$ has either zero or two 1 since we are in $$\textrm{GF}(2)$$.
Summation of all columns results in 0 which means the matrix is singular.


# Appendix B: Invertibility of chi-transformation
Assume $$n = 5$$
$$
\begin{aligned}
    x_i 
        &= \chi(x)_i \oplus x_{i+1}' x_{i+2} \\
        &= \chi(x)_i \oplus (\chi(x)_{i+1} \oplus x_{i+2}' x_{i+3})' x_{i+2} \\
        &= \chi(x)_i \oplus (\chi(x)_{i+1} \oplus x_{i+2}' x_{i+3} \oplus 1) x_{i+2} \\
        &= \chi(x)_i \oplus \chi(x)_{i+1} x_{i+2} \oplus x_{i+2} \\
        &= \chi(x)_i \oplus \chi(x)_{i+1}' x_{i+2} \\
        &= \chi(x)_i \oplus \chi(x)_{i+1}' \chi(x)_{i+2} \oplus \chi(x)_{i+1}' \chi(x)_{i+3}' x_{i+4} \\
        &= \chi(x)_i \oplus \chi(x)_{i+1}' \chi(x)_{i+2} \oplus \chi(x)_{i+1}' \chi(x)_{i+3}' x_i \\
    (\chi(x)_{i+1}' \chi(x)_{i+3}')' x_i
        &= \chi(x)_i \oplus \chi(x)_{i+1}' \chi(x)_{i+2}
\end{aligned}
$$
One things we can know from this formula is that
it is non-invertible if all odd or even bits are zeros.
For example, `00000...`, `010101...` and `101010...` are all result in zeros.
