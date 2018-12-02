---
name: Back to Bletchley Park
category: cryrev
points: 474
solves: 1
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf-tasks-writeup/)
{% endignore %}

> We have gone quantum.
> A collaborator of ours built this quantum circuit to compute the
> factorization of a Bavs RSA key and took note of the results.
> They are now stored in her server (https://qc.pwn2.win)
> inside the `/a/N` path,
> where a is the group generator and N is the modulus.
> Unfortunately we could not get in touch with her lately,
> so we need your help understanding what she did.
> Once you figure out how the circuit works
> and discover what are the values of a and N,
> we can see the results from her calculations and use them to decrypt the message.
> 
> Note: We know that the message was originally encrypted with the following commands:
> 
> openssl rsautl -encrypt -oaep -pubin -inkey public.pem -in aes256.key -out aes256.key.enc
> openssl aes-256-cbc -base64 -in secret_message.txt -out secret_message.enc -k $(cat aes256.key)


## Time
5 hours

# Solution
## TL;DR
1. Split the qasm file
2. Extract N
3. Plot the calling graph
4. Extract the classical part
5. Simulate it to get a
6. Get the period and public key from the server
7. Factorize N

We have gone quantum.

In this chal,
we have a crazy 10GB (40GB in 1024bits ver.) qasm file describing a enormous quantum circuit.
As the description says, the circuit is built for factoring RSA key.
It may be an implementation of
[Shor's algorithm](https://en.wikipedia.org/wiki/Shor%27s_algorithm).

The following writeup is for 640bits version,
it should be similar in 1024bits,
but gate/reg name will be different.


## Basic qasm
1. qreg: a quantum register (e.g. qubit), initialized to $$|0\rangle$$.
2. creg: a classical register, e.g. bit, initialized to $$0$$.
3. x: `NOT` in quantum.
4. h: Hadamard gate, a gate for creating superposition or some crazy quantum things.
5. cx: `XOR` in quantum, `cx a,o` equals `o ^= a` in classic.
6. ccx: `AND` in quantum, `cx a,b,o` equals `o ^= (a & b)` in classic.
7. swap: Swap two input qubits.


## Tear the monster
To dealing with the qasm file,
I split each gate to seperate file,
outputing 3881 files. ([Script]([_files/split.py]))

The most interesting file is [main]([_files/splits/main]),
which is the part not enclosed in `gate xxx { ... }`.
It looks like:
```
qreg af[642];
qreg a[642];
qreg n[642];
qreg kk[643];
qreg aa[1];
qreg ab[1];
qreg an[642];
qreg ac[642];
qreg yv[642];

creg c[642];

creg cr0[1];
creg cr1[1];
...
creg cr640[1];
creg cr641[1];

x n[0];
x n[3];
x n[6];
x n[7];
...
x n[633];
x n[635];
x n[638];
x n[639];

sqgate_3858 a,af,n,ac,an,yv,kk,aa,ab;

h yv;

sqgate_3850 af,a,n,kk,an,ac,yv

measure an -> c;
h yv[0];
measure yv[0]->cr0[0];
if(cr0==1) u1(pi/2) yv[1];
h yv[1];
measure yv[1]->cr1[0];
if(cr0==1) u1(pi/4) yv[2];
if(cr1==1) u1(pi/2) yv[2];
h yv[2];
measure yv[2]->cr2[0];
if(cr0==1) u1(pi/8) yv[3];
if(cr1==1) u1(pi/4) yv[3];
if(cr2==1) u1(pi/2) yv[3];
h yv[3];
...
```

The part `x n[...];` seems to be an constructor of variable `n`.
According to its name, it might be $$N$$ which is one of our target.

There's also an interesting variable `a`,
but it isn't initialized directly.

After init `n`, it calls `sqgate_3858`, applies hadamard gate on `yv`,
calls `sqgate_3850`, and then extracts the output by measuring.

Note that although `yv` is passed to `sqgate_3858`,
there isn't any reference to it in `sqgate_3858`.


## Find the generator
According to the wikipedia, Shor's algorithm is composed of these steps:
1. Classical parts: Generate a random number $$a$$, which is coprime to $$N$$.
2. Prepare initial state: Apply hadamard gate to zero state.
3. Apply $$f(x)$$: Change initial state to $$|x\rangle\ |f(x)\rangle$$.
4. Apply QFT.
5. Measuring output to find period.

Compare to the code in last part,
`sqgate_3858` seems to be the classical part,
`h yv` is preparing the initial state,
`sqgate_3850` applied `f(x)` and `QFT`.

When I plot the [calling graph]([_files/graph.gv.svg])
([Script1]([_files/callingGraph.py]) and [Script2]([_files/plot.py])),
I can confirm that `sqgate_3858` is actually a classical circuit.
There isn't any call to hadamard gate or any gate that will create superposition.
The primitive gates it called are: `x, cx, ccx, swap`.

We can simulate this part and extract the state of those register.
Here's the [script]([_files/sim.py]),
and the output is:
```
a: 140...565
su: 0
n: 362...081
o: 1
x: 1
y: 0
sc: 0
aa: 0
ab: 0
```
We got $$a$$ and $$N$$ now.


## Factorize N
Opening the webpage `https://qc.pwn2.win/140...565/362...081` as the challenge description said,
it gave us the period $$r$$ and $$e$$.

According to the algorithm:
$$
\begin{aligned}
& a^r = 1 \mod N \\
\implies & a^r - 1 = 0 \mod N \\
\implies & (a^{r/2} - 1) (a^{r/2} + 1) = 0 \mod N \\
\end{aligned}
$$

There are three possibilities:
$$N$$ divides $$(a^{r/2} - 1)$$,
$$N$$ divides $$(a^{r/2} + 1)$$,
or $$p$$ divides $$(a^{r/2} - 1)$$,

To check this, we can calculate
$$
p = \text{gcd}(a^{r/2} - 1, N) = \text{gcd}((a^{r/2} - 1 \mod N), N)
$$
And then we found $$p$$ is not equals to $$N$$.
It means that is a factor of $$N$$ !!!

Next step is to construct the private key with `RsaCtfTool`, and decrypt the flag with `openssl`.
