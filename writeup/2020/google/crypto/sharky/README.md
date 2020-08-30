---
name: SHArky
category: crypto
points: 231
solves: 38
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}

> Can you find the round keys?


## Time
2 hours


# Behavior
We got a modified SHA256 in this task.
The first 8 round constants are replaced by 8 random values,
and our goal is to recover those 8 round constants with only one output hash and its input.


# Solution
## TL;DR
1. Subtract the IV from the output
2. Undo last 56 rounds
3. Recover round constants from 8 to 1 by propagating the error the first round.


## SHA256
The overall structure of SHA256 looks like this:
```python
def sha256(inp):
    padded = pad(inp) # pad to multiple of 64 bytes
    blocks = chunk(padded) # split each 64 bytes blocks
    state = IV
    for block in blocks:
        w = compute_w(block)
        s = compression(state, w, ROUND_KEYS)
        state = [(x + y) & 0xffffffff for x, y in zip(state, s)]
```

In this task, our input has only one block, so the for loop only runs once.
Also, we know what the input is, so we have all those `w`.

The last step can be reversed by subtraction:
```python
state = [(x - y) & 0xffffffff for x, y in zip(state, IV)]
```

Next, the compression function is:
```python
def compression(self, state, w, round_keys):
    for i in range(64):
        state = self.compression_step(state, round_keys[i], w[i])
    return state

def compression_step(self, state, k_i, w_i):
    a, b, c, d, e, f, g, h = state
    s1 = self.rotate_right(e, 6) ^ self.rotate_right(e, 11) ^ self.rotate_right(e, 25)
    ch = (e & f) ^ (~e & g)
    tmp1 = (h + s1 + ch + k_i + w_i) & 0xffffffff
    s0 = self.rotate_right(a, 2) ^ self.rotate_right(a, 13) ^ self.rotate_right(a, 22)
    maj = (a & b) ^ (a & c) ^ (b & c)
    tmp2 = (tmp1 + s0 + maj) & 0xffffffff
    tmp3 = (d + tmp1) & 0xffffffff
    return (tmp2, a, b, c, tmp3, e, f, g)
```

It won't be too hard to write its inverse by changing order of instructions and terms:
```python
def decompression_step(self, state, k_i, w_i):
    tmp2, a, b, c, tmp3, e, f, g = state
    maj = (a & b) ^ (a & c) ^ (b & c)
    s0 = self.rotate_right(a, 2) ^ self.rotate_right(a, 13) ^ self.rotate_right(a, 22)
    tmp1 = (tmp2 - s0 - maj) & 0xffffffff
    d = (tmp3 - tmp1) & 0xffffffff
    s1 = self.rotate_right(e, 6) ^ self.rotate_right(e, 11) ^ self.rotate_right(e, 25)
    ch = (e & f) ^ (~e & g)
    h = (tmp1 - s1 - ch - k_i - w_i) & 0xffffffff
    return a, b, c, d, e, f, g, h
```

The last 56 round constants is same as standard SHA256,
so we can undo those rounds with the inverse function above.

The problem is: how to reveal those secret round keys?


## Linear property of first 8 rounds
In decompression_step, we can notice that `k_i` is only used to calculate `h`.
If we use a wrong round constant in `decompression_step`,
Only `h` will be incorrect.
All values from `a` to `g` is still valid.
Furthermore, the error in `h` is the difference between the real round constant and the constant we use.

Consider the last round (i.e. round 8),
If we use 0 as the round constant to undo this round,
Only `h` is incorrect, and the difference to the real one is the secret constant we want.

Next, consider round 7,
`h` becomes `g` and all values from `a` to `f` is valid.
Values after `h` will be rubbish, but it doesn't matter.

Keep undoing those rounds with round constant 0,
the error will be propagate to `a`,
and the difference between our `a` and `a` in IV will be the last secret constant we want !!!

With this secret constant, we can undo round 8.
And use same tricks again to make the error of round 7's constant propagate to `b` and so on.

You can found the script at [here]([_files/solve.py]).
