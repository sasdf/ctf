---
name: Oracle
category: crypto
points: 340
solves: 13
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> You should probably ask Apollo for help.
> 
> The original server of the challenge didn't match the attachment, so we released one that does:  oracle2.2020.ctfcompetition.com
> If you want to connect to the old server, it's available at oracle.2020.ctfcompetition.com


## Time
10 hours

4 hours is spent on the hard way for solving subtask 2.


# Behavior
The task is composed of two subtask about state reconstruction attack on different AEGIS settings.
The first one is attacking AEGIS128L with encryption oracle and IV reuse.
The second one is attacking AEGIS128 with decryption oracle and a tight query count limitation.


# Solution
## TL;DR
(In subtask 2,
I developed some techniques that reduce the query number down to 170.
See the last part for those tricky optimizations.)

Subtask 1
1. Encrypt one all zero plaintext for the base case
2. Encrypt two different input differences for each blocks
3. Recover all states except S1, S5 with those differences
4. Recover S1, S5 from the ciphertext and states.

Subtask 2
1. Leak 6 blocks of plaintext
2. Same as subtask 1

Subtask 2 in a hard way
1. Reduce the fetches of the base case by using per byte difference
2. Reduce the size of additional checksum


## AEGIS
AEGIS is one of the winner of CAESAR (Competition for Authenticated Encryption: Security, Applicability and Robust-ness).
It use some AES primitives to build the cipher, so we can get pretty good hardware acceleration on almost all modern computers.

The simplest variant of AEGIS is AEGIS128, it has 5 states, S0 ~ S4.
Those states are initialized by the secret key, IV, and AAD.
After initialization, these states are used to generate keystream.
The keystream only directly depends on those states and plaintext, not the key/IV/aad.
So if we get those states, we can encrypt any plaintext without knowing the key.


### Note: All '+' in the equations blocks of AEGIS means XOR

## Subtask 1
In the first subtask, we are asked to recover the states with 7 chosen plaintext queries with a same unknown IV.
The attack is described in this paper: [Under Pressure: Security of Caesar Candidatesbeyond their Guarantees](https://eprint.iacr.org/2017/1147.pdf).
Let's start with AEGIS128 first and port it to AEGIS128L.

In AEGIS128, the plaintext is split into 16-bytes chunks.
The ciphertext of each chunk is
```
C_i = X_i + S1_i + ( S2_i & S3_i ) + S4_i
```
After encryption a chunk `X_i` the state is updated with following equations:
```
S0_{i+1} = S0_i + R(S4_i) + X_i
S1_{i+1} = S1_i + R(S0_i)
S2_{i+1} = S2_i + R(S1_i)
S3_{i+1} = S3_i + R(S2_i)
S4_{i+1} = S0_i + R(S3_i)
```
Where R is one AES round function (i.e. single SubByte, ShiftRow, MixColumn).

If a message with three blocks, say `ABC`. We'll get:
```
C_0  = A + constant
S0_1 = S0_0 + R(S4_0) + A
C_1  = B + constant
S0_2 = A + B + constant
S1_2 = R(S0_0 + R(S4_0) + A) + constant
C_2  = C + S1_2 + constant
     = C + R(S0_0 + R(S4_0) + A) + constant
```
And we can mount a differential attack on first block and get the difference on `C_2`.
For example, if we encrypt `0BC` and `ABC`.
```
Let S0' := S0_0 + R(S4_0)

C_20 = C + R(S0' + 0) + constant
C_2A = C + R(S0' + A) + constant

C_20 + C_2A = R(S0') + R(S0' + A)
```
Moreover, MixColumn and ShiftRow are linear, so we can undo them on the difference too:
```
InvShiftRow(InvMixColumn(C_20 + C_2A)) = SubByte(S0') + SubByte(S0' + A)
```
We can build a lookup table of all possible input difference, corresponding output difference and their values.
But it will give us 2 or 4 candidates of each bytes.
To determine S0', we need to collect two different differences, and find their common candidiate.

Next, we can recover S4 by mounting differential attack on second block and get the difference on `C_3`.
For example, if we encrypt `00BC` and `0ABC`.
```
Let S4' := S0_0 + R(S4_0)

C_20 = C + R(S0' + 0) + constant
C_2A = C + R(S0' + A) + constant

C_20 + C_2A = R(S0') + R(S0' + A)

S0_1 = S0'
S0_2 = A + S0' + R(S4_1)
S1_3 = R(A + S0' + R(S4_1)) + S1_2
C_3  = C + S1_3 + constant
     = C + R(A + S0' + R(S4_1)) + constant
```
We can recover `S0' + R(S4_1)` with same method, and calculate `S4_1` because we already have `S0'`.
Same methods can be used to recover all states.


Now, let's talk about AEGIS128L.
It is very similar to AEGIS128, but it has 8 states and encrypt two 16-bytes blocks at a time:
```
C_iX = X_i + S1_i + ( S2_i & S3_i ) + S6_i
C_iY = Y_i + S5_i + ( S6_i & S7_i ) + S2_i
```
And the state updating function is:
```
S0_{i+1} = S0_i + R(S7_i) + X_i
S1_{i+1} = S1_i + R(S0_i)
S2_{i+1} = S2_i + R(S1_i)
S3_{i+1} = S3_i + R(S2_i)
S4_{i+1} = S4_i + R(S3_i) + Y_i
S5_{i+1} = S5_i + R(S4_i)
S6_{i+1} = S6_i + R(S5_i)
S7_{i+1} = S7_i + R(S6_i)
```
It's similar to two parallel AEGIS instances.
Since the linear property (i.e. S1_i, S5_i) is still vaild,
the same attack works for AEGIS128L too.

In this subtask, we are only allowed to send 7 queries.
The base case (all zeros) takes 1 query.
Differential attack on each state pair needs two differential, costs 2 queries.
We can recover all states except `S1` and `S5`.
To get those states, recall that the ciphertext is:
```
C_iX = X_i + S1_i + ( S2_i & S3_i ) + S6_i
C_iY = Y_i + S5_i + ( S6_i & S7_i ) + S2_i
```
With all other states and plain/ciphertext in hand, we can calculate these values by moving those terms.


## Subtask 2
In this subtask, we are working on simpler AEGIS128 :)
We have a ciphertext of unknown ascii plaintext.
And a decryption oracle that will show following error when decrypted plaintext is not ascii:
```
UnicodeDecodeError: 'ascii' codec can't decode byte 0x80 in position 0: ordinal not in range(128)
```
From the error message, we can get the value of one byte and its position.
And we are only allowed to send 231 queries.
Also, it doesn't check the tag, so we can decrypt any ciphertext without a valid tag.

The goal is to encrypt a predefined plaintext which have 407 bytes long,
so we can use decryption oracle to construct it directly.

As what we said before,
we only need states to encrypt arbitary plaintext since the keystream only depends on the states and plaintext.
Let's see how many queries we need to apply same attack in subtask 1.

In subtask 1 we are using encryption oracle, but we only have decryption oracle here.
Actually, they are the same because the "encrypt" function is just xor the plaintext with the keystream.
The difference is that the value for updating the state is the decrypted plaintext, not our input.
To recover `S4_1` from `R(A + S0' + R(S4_1))`, we need to know the input `A` too.

Leaking the plaintext is easy, we can use the XOR attack on stream ciphers:
```
 C_i      =  X_i      + S1_i + ( S2_i & S3_i ) + S4_i
(C_i + Z) = (X_i + Z) + S1_i + ( S2_i & S3_i ) + S4_i
```
We can turn on the MSB of each bytes one by one to get its value.

We'll need first 6 plaintext blocks, which takes `6 * 16 = 96` queries.

Next, we need two differential inputs.
Leaking non-ascii blocks is a little bit tricker.
Send the query first, and the returned position tell us where the first non-ascii byte is.
Then we use the same method to recover those ascii prefixes, turn off the MSB of non-ascii byte, and move to next segment.

If the last byte is non-ascii, then we can leaking all 16 bytes in 16 query.
Otherwise, one query will fall out of target range, and we need an additional query to leak the last byte.

In total, we need `96 + 16.5 * 2 * 4 = 228` queries.
Great! Mission completed, although I didn't count those queries correctly during the competition :(

The last problem is that we only recover `S0_1`, but there's no way to recover `S0_0`.
To remove the additional block in front of the plaintext, we can move it into aad.
And we can encrypt arbitary plaintext now :)



## Subtask 2 in a hard way
One special property in this subtask is that the limitation is enforced on how many fetch requests we sent, not the queries.
("query" here means a crafted input for encryption, and "fetch" means leaking an output byte).
Actually, we can send maximum 231 different queries if we only need single bytes in each of them !!!

And here is what we have done: send 14 queries and spent 16 fetches on each queries to leak the state.

Can we do better?

### Share the base case in the same column
In the differential attack on AES round (i.e. R(S0') + R(S0' + A)).
Consider first AES column (i.e. the first 4 bytes),
we'll need 4 fetches for the base case (i.e. R(S0')) and 4 fetches for the difference (i.e. R(S0' + A)).

What if we send a one byte difference like:
```
R(S0' + InvShiftRow([X000 0000 0000 0000]))
R(S0' + InvShiftRow([0X00 0000 0000 0000]))
R(S0' + InvShiftRow([00X0 0000 0000 0000]))
R(S0' + InvShiftRow([000X 0000 0000 0000]))
```
The difference we be propagated to all four bytes in the same column in MixColumn step.
It is also invertible given any single byte and its position,
because it is just multiplication in Rijndael's Galois field.

We still need 4 queries for such difference, but we can do better in the base cases.

If we are lucky enough that all four queries return the difference in position 0,
We only need one fetch at position 0 for the base case instead of 4.

If we are unlucky, we'll need 4 fetches for the base case same as before.
It won't become worse. Great!

When all four bytes are ascii,
we have to refetch the output by flipping their MSB.
we can select the position that base case is known,
so we don't have to run additional fetch for base case.

To avoid wasting one query when all four bytes are ascii,
we can pack the requests of all 4 AES columns since they are independent.
Furthermore, we can also pack all independent parts in these requests:
* two different input differences
* fetches of base cases
* refetch of ascii output

In practice, I create 4 priority queues for processing and packing those requests.


### Shorter checksum
In the original attack,
we have to use two different input differences because it will give 2 or 4 candidates.
Let's do some math:
1. One AES column is 4 bytes
2. Each bytes has maximum 4 candidates
3. Each column has 4^4 = 256 = 2^8 candidates
4. We fetch 4 additional bytes = 2^32 bits for deciding which candidate is correct?????

We can reduce 4 additional fetches to one for selecting those 256 candidates.
Although it has some collsion if we only use one byte checksum,
we could just run our attack again if we are unlucky.

The final difference we use for a single column is:
```
R(S0' + InvShiftRow([1000 0000 0000 0000]))
R(S0' + InvShiftRow([0100 0000 0000 0000]))
R(S0' + InvShiftRow([0010 0000 0000 0000]))
R(S0' + InvShiftRow([0001 0000 0000 0000]))
R(S0' + InvShiftRow([2222 0000 0000 0000]))
```

With both optimization above, we can reduce 60 fetches on average.
You can find the full script at [here]([_files/solve.py]).
