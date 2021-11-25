---
name: dlog
category: crypto
points: 477
solves: 2
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> If you have never heard of discrete logarithm, [let me google that for you.](https://www.google.com/search?q=discrete+logarithm)


# Overview, Concept and Design Criteria
The main idea of this challenge is timing attacks.
Observability is very useful and become more popular,
We have a bunch of tools available, such as ELT stack, Prometheus + Grafana, Splunk, Cloudwatch...
They provide useful metrics / logs for debugging and improving your application.
However, these metrics are actually as sensitive as your password.

Skip to the next solution part if you aren't interested in the story behind this challenge :)

## Motivation
In the PQC lecture I took, the professor keeps emphasizing the importance of the constant time algorithm in cryptography.
It is definitely true in theory, but I was wondering how much impact it will have in a real application.
There are some papers about timing attacks on TLS, and they look promising.
I started searching for other vulnerable targets.

## Target
The first target I tried is golang's built-in crypto module.
The elliptic module uses a double-and-add approach. (p224 and p256 has a better implementation)
The running time depends on the secret, but it uses the jacobian coordinate,
and I have no idea how to control its internal state.
Golang uses karatsuba for multiplication,
it might leak time information, but I didn't find a good cryptosystem to exploit this feature.
Golang and GMP use Montgomery reduction for modular exponentiation,
they pad the input to the same length and I can't observe any time difference.
The running time depends on its exponent, but that would be our secret and the user shouldn't control it.
Some papers are suggesting the last reduction in Montgomery might be vulnerable, but I didn't try it.

Finally, I found something suitable.
CPython uses plain modular multiplication for its exponentiation by squaring algorithm,
The running time depends on both base and exponent!!
It also uses a sliding window but is disabled when the exponent is less than 128 bits.

We are ready to build our challenge, but how can we measure the time?

## Measure timing
The first version of the challenge will return the running time in the HTTP header.
It works fine, but the vuln is too obvious.
I started searching for other things that provide the same functionality.

Apache and Nginx can set the request duration in the header,
but it doesn't provide enough timing resolution (milliseconds).

[Timeless timing](https://www.usenix.org/conference/usenixsecurity20/presentation/van-goethem)
of HTTP/2 hides the vuln perfectly, but it isn't stable enough.

Then I recall that Balsn uses Prometheus before to monitor our CTF infra.
Hmm, it provides nanosecond measurements :/

One main disadvantage of Prometheus is that the metrics are global.
Players will affect each other,
but don't think we will see a lot of players poking the server at the same time.
![(Img: metrics)]({_files/dlog.png})
Seems we only have 6 players poke our server ;)


## Fun facts
* Using Prometheus actually makes some players think it is not about timing attack :>


# Solution
[The server]([_files/deploy/src/server.py]) has two endpoints:
* `/oracle`: return `pow(input, secret, p)`.
* `/flag`: test `pow(input, secret, p) == 1337`.
where `secret < 2^128` and `p` is a prime.

The intended solution is using timing attack.
I spent a long time thinking about pure math solutions but with no luck.
The problem is weaker than static Diffie–Hellman because we have `/oracle`,
and weaker than discrete log because we don't need to recover `secret`.
Also, `secret` is much smaller than `p`.
Unfortunately, I can't find any way to use these features.
Let me know if you solve it using pure math.


## Recover p
I calculate gcd of `pow(2^i, secret, p)*pow(2, secret, p) - pow(2^(i+1), secret, p)` to recover p.

After the CTF, @grhkm told me that `pow(-1, secret, p) + 1 == p`.
Ohh... Good job!


## Recover s
CPython uses exponentiation by squaring, from MSB to LSB.

```c
for (; bit != 0; bit >>= 1) {
    MULT(z, z, z);
    if (bi & bit) {
        MULT(z, a, z);
    }
}
```
where `MULT` uses karatsuba multiplication and long division for modulo.
If `z` is small, it will run faster.

Assuming we know the first `k` bits of the secret is `s_k`,
`z` in step `k+1` with input `x ^ -(s_k*2+1)` will be `x` if the `k+1` bit is 1.
By choosing a small `x` we can make the exponentiation runs faster.

Starting from the beginning, we can recover the secret bit by bit. (We have to guess the first two bits.)


## Measurements
Measurements of side-channel attacks are usually noisy.
We have to aggregate multiple measurements to recover the bias.

We collect a pair of measurement: `group0(k+1) = x ^ -(s_k*2+0)` and `group1(k+1) = x ^ -(s_k*2+1)` with `x < 2^20`.

Here is the method I use for denoising:
1. Collect 180 pairs of queries per bit with different `x`.
2. Remove the largest 25% and smallest 25% measurements.
3. Find the median of every 3 consecutive measurements.
4. Calculate the ratio that group 1 is larger than group 0.
5. Keep retry until the ratio is larger than 0.75 or smaller than 0.25.

If we found the ratio is close to 0.5, it means we have an incorrect `s_k`.


## Sending Requests
The HTTP server has the keep-alive feature.
You can send all your requests at once using a raw TCP socket.
We achieve about 180 requests per second regardless of the server's location.

Also, `/flag` won't return the number, which could be slightly faster than `/oracle`.


You can find our full exploit [here]([_files/solution/p.py]).
