---
name: aeshash
category: crypto
points: 1000
solves: 0
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> Golang, the c++ in the 21st century, has a new built-in hash called aeshash. It must be super secure.


# Overview, Concept and Design Criteria
One day, I was inspecting the implementation of the map in Golang.
It is a hash table using `aeshash`.

Hmm..., AES? Sounds powerful.

AEShash is a new hash function they made.
It doesn't use full AES, just hardware AES instruction to accelerate it.

There are many cryptanalyses on reduced round AES.
So how about this aeshash? it only uses three rounds.

It turns out the hash is not one way, and we can reconstruct the seed using differential attack.

## Does that mean Golang's map is bad?
No.

The hash is designed for internal use,
and the hash value should never be exposed.
We can't recover the seed without accessing the hash value,
so it is still safe so far.


# Solution
Golang's aeshash uses two seeds: A global seed `aeskeysched` and a per table seed.
The server set the per table seed to be `0xdeadbeef`,
and the global seed is initialized randomly at the program startup.

Without knowing the seed, it is impossible to control the output.
Fortunately, it is possible to recover the seed from the output.


## Scramble
The main building block of AEShash is Scramble: `AESENC X1, X1`.
[AESENC](https://www.felixcloutier.com/x86/aesenc) performs one round AES.

```c
// AESENC state, RoundKey
state = ShiftRows(state);
state = SubBytes(state);
state = MixColumns(state);
return XOR(state, RoundKey);
```

And golang uses 3 scramble combo to make the state random.


## Unscramble
Since it uses the initial state as the round key,
we can't use `AESDEC` to unscramble.

The MixColumns function operates on one column (4 bytes) at a time.
It is feasible to search over all possible 4 bytes RoundKey for each column.

Since the ShiftRows function won't move the first row,
we can test if the first byte of our guessed RoundKey is the same as the first byte after InvMixColumns and InvSubBytes.
This results in `2^32 / 2^8 = 2^24` candidates for each column.

ShiftRows introduce 2 conditions between each column pair.
For example, column 1 has one element shifted to column 2 at row 2, and column 2 also has one element shifted to column 1 at row 3.
We can sort the candidates of column 2 using the second and third elements for fast indexing.

Each candidate of column 1 will have `2^24 / 2^16 = 2^8` candidates in column 2 satisfying the conditions.
Walking through all the candidate pairs will take `2^24 * 2^8 = 2^32` iterations.

After column 1 and column 2 are decided, we have 4 conditions.
There will be `2^24 / 2^32 = 1/256` candidates in column 3 on average.
And then we only need to check we have a valid candidate in column 4.

The whole algorithm has complexity `2^32`.

You can find the implementation [here]([_files/solution/tools/rev.c]),


## Hash seed
The last step of AEShash is truncating to 8 bytes.
So we can use unscramble to recover the seed directly.

We have to recover the full 16 bytes state first.

When the input is 16 bytes, our input xor with the seed and then is scrambled 3 times.

If we change the first byte of the input.
1. The first scramble will propagate the difference to the first column,
and the difference depends on one byte (first byte).
2. The second scramble will propagate the difference to all bytes,
and the difference depends on four bytes (first column).
3. The third scramble mixed up everything, and the difference depends on all inputs.

However, MixColumns is a multiplication of a constant poly `a(x)` in Rijndael's finite field.

$$
\begin{aligned}
   & \text{MixColumns}(u) - \text{MixColumns}(v) \\
=\ & (u \times a) - (v \times a) \\
=\ & (u - v) \times a \\
=\ & \text{MixColumns}(u - v) \\
\end{aligned}
$$
where `-` is xor in the field.

Using this property, we can remove the last MixColumns,
and find the corresponding 4 bytes to perform our differential attack.

> The differential attack is straightforward, and is left as an exercise to the reader :)

Or you can find it in the [solution code]([_files/solution/tools/rec.c]).


## Full exploit
To construct the input of the target hash,
we can pad the state with random 8 bytes, unscramble three times,
and xor the seed.

The full script is [here]([_files/solution/solve.py]),
combining all the tools we build above and also network I/O.


## Alternative approach (not tested)
It might be possible to solve this challenge without unscrambling.

AEShash uses XOR to combine different blocks.
Since the hash is only 64 bits,
it is possible to use the Meet-in-the-Middle approach for searching a collision.

For the seed recovery part, I recover the state after one scramble and unscramble it to get the seed.
But it is possible to recover the initial state using differential.
