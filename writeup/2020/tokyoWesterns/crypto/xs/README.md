---
name: XOR and shift encryptor
category: crypto
points: 303
solves: 21
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}


## Time
2 hours


# Behavior
There's a flag "encrypted" by XORShift PRNG.
The seed of the PRNG is hardcoded, but they encrypted the flag using a secret `jump` function.
What we need to do is implement that `jump` function.


# Solution
## TL;DR
1. Build the state transition function is 4096 x 4096 $$GF(2)$$ Matrix.
2. Use double type for better matrix multiplication algorithm.


## State transition function
```
s0 = state[current_position]
current_position = (current_position + 1) % 64
s1 = state[current_position]
return_value = (s0 + s1) & m

s1 = s1 ^ (s1 << a) & m
state[current_position] = (s1 ^ s0 ^ (s1 >> b) ^ (s0 >> c)) & m
```
We can rotate the state array, keeping the position to be always zero.
To model the function as a matrix,
we need to express each 64bits number as bit strings,
and flatten them to 4096 bits.
```
def shift_mat(n, s):
    return np.diag(np.ones(n - abs(s), dtype=np.uint8), k=s)

O = zeros(64)
I = identity(64)
A = shift_mat(64, -a)
B = shift_mat(64, b)
C = shift_mat(64, c)
S1 = ((B+I) @ (A+I)) & 1
S0 = (C+I) & 1

M = np.block([
    [S0,      S1,          zeros(64, 4096-128)], # <- new state
    [zeros(4096-128, 128), identity(4096-128) ], # <- shift numbers
    [I,       zeros(64, 4096-64)              ], # <- rotate numbers
])
```


## Jump
To implement jump function, we can use exponentiation by squaring,
```
E = [M]
for _ in trange(64):
    E.append(matmul(E[-1], E[-1]))
E = np.stack(E)

def jump(n, state):
    R = identity(4096)
    for s in range(64):
        if (n >> s) & 1:
            state = matmul(E[s], state)
    return state
```

However, numpy's matmul on integer runs super slow.
We have to use floating type to use more efficient kernels in BLAS/MKL.
The maximum possible value after matmul of binary matrixes is 4096,
so we don't need to worry about numerical error.
```
def matmul(A, B):
    A = (A & 1).astype(np.double)
    B = (B & 1).astype(np.double)
    C = (A @ B).astype(np.uint64) & 1
    return C
```

Full script can be found at [here]([_files/solve.py]).
