---
name:  Quantum Key Distribution
category: crypto
points: 92
solves: 134
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> Generate a key using Quantum Key Distribution (QKD) algorithm and decrypt the flag.


## Time
15 minutes  


# Behavior
> We are simulating a Quantum satellite that can exchange keys using qubits implementing BB84.
> You must POST the qubits and basis of measurement to `/qkd/qubits` and decode our satellite response,
> you can then derive the shared key and decrypt the flag.
> Send 512 qubits and basis to generate enough key bits.

The service runs BB84 protocol, there is a good explaination of the protocol on
[wikipedia](https://en.wikipedia.org/wiki/Quantum_key_distribution#BB84_protocol:_Charles_H._Bennett_and_Gilles_Brassard_%281984%29)


# Solution
## TL;DR
1. Exchange shared secret using BB84 protocol
2. Convert the bit string to char string with correct order
3. XOR the secret and encryped key to decrypt it

Here's a example copied from wikipedia:

Action                           |
---------------------------------|---|---|---|---|---|---|---|---
Alice's random bit               | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 1
Alice's random sending basis     | + | + | x | + | x | x | x | +
Photon polarization Alice sends  | ↑ | → | ↘ | ↑ | ↘ | ↗ | ↗ | →
Bob's random measuring basis     | + | x | x | x | + | x | + | +
Photon polarization Bob measures | ↑ | ↗ | ↘ | ↗ | → | ↗ | → | →
PUBLIC DISCUSSION OF BASIS       |   |   |   |   |   |   |   |
Shared secret key                | 0 |   | 1 |   |   | 0 |   | 1

In this task, we are Alice and the server is Bob.
To establish a shared secret, we have to choose some random bits first:

```python
state = [random.randrange(2) for _ in range(512)]
```

Next, for the simplicity, we set all the basis to `+`

```python
basis = ['+'] * 512
```

And calculate the qubits state based on the basis an the bits

```python
z = [{'real': 1, 'imag': 0}, {'real': 0, 'imag': 1}]
qubits = [z[s] for s in state]
```

Send those qubits to the server to get Bob's basis and encrypted key

```python
res = sess.post(
    'https://cryptoqkd.web.ctfcompetition.com/qkd/qubits',
    json={ 'basis': basis, 'qubits': qubits, }
    ).json()
```

Compare the basis and keep those bits with correct basis

```python
bits = [s for s, b in zip(state, res['basis']) if b == '+'][:128]
```

Convert the bits to string with MSB-first and Left-first order.

```python
shared = int(''.join(map(str, bits)), 2).to_bytes(16, 'big')
```

XOR the secret and encryped key to decrypt it

```python
encrypted = bytes.fromhex(res['announcement'])
key = bytes(a ^ b for a, b in zip(encrypted, shared)).hex()
print(key)
```

Now decrypt the flag using the command provided in the description

```bash
echo "$KEY" > plain.key
xxd -r -p plain.key > enc.key
echo "$FLAG" | openssl enc -d -aes-256-cbc -pbkdf2 -md sha1 -base64 --pass file:enc.key
```
