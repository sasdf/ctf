---
name: unpredictable
category: crypto
points: 810
solves: 6
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}


> Our team, Balsn, is full of prophets.
> We know the future, we know the flag.
> How about you?


# Overview, Concept and Design Criteria
I found the idea when I trying to figure out the difference between py2/py3's random.
And I was wondering whether I can reconstruct python3's random state.

The beauty of this task is that it's very simple: just `randrange` with default setting in python3.

I planned to make a server for this task, where the code will look much more simpler than current one.

However, due to the traffic it'll generated, I changed it to a offline challenge.

BTW, it's the hardest challenge for me in those 3 taskes I wrote.
I was pretty surprised that so many people solved it.

It tooks me more than 2 days to solve it,
and I have totally no idea whether my solution will work or not when I was implementing it.

I'm noob :(

There's also a harder version -- smaller randrange, or ultimately one bit randrange, and I still don't know how to solve it.


## Fun facts
* I thought `unpredictable` is the hardest one among those crypto. Apparently, it's not.


# Solution
In this challenge, we have 0x1337 integers generated from randrange(3133731337), and the goal is to reconstruct PRNG state.

## Mersenne twister
Mersenne twister is a common PRNG that is default random generator in many programming language.
It's state is composed of 624 32-bit integers,
and the state is transformed with some linear operation.
The output of mersenne twister is it's state processed with some reversible function,
so we can construct it's state after we have 624 consecutive output.

Even it's not consecutive,
we can still reconstruct the state if we know the length of gaps between each output.
The transformed of state is linear, so simply solve some matrix will recover it.

But this task is more evil,
python drop some of the output randomly, and you have no idea what the gaps are.

## Rejection sampling
Python's `randrange` use 
[rejection sampling](https://en.wikipedia.org/wiki/Rejection_sampling) 
to convert random bits to uniform distribution in a given range.
```python
def _randbelow_with_getrandbits(self, n):
    "Return a random int in the range [0,n).  Raises ValueError if n==0."

    getrandbits = self.getrandbits
    k = n.bit_length()  # don't use (n-1) here because n can be 1
    r = getrandbits(k)          # 0 <= r < 2**k
    while r >= n:
        r = getrandbits(k)
    return r
```

In our case, the probability of an output to be dropped is about `0.27`.

## Align the numbers
To reconstruct the state, we have to reconstruct the position first.
Fortunately, all output with distance (0, 1, 397, 624) should follow these condition:
```
y = _int32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
self.mt[i] = (y >> 1) ^ self.mt[(i + 397) % 624]

if y % 2 != 0:
    self.mt[i] = self.mt[i] ^ 0x9908b0df
```
The first number only provide one bit, which is not useful. Just ignore it and try both possible condition.

If we find a triple that satisfied the condition, we got a constraint about their relative position.
And we can group a lot of constraints to reconstruct the actual position we need.

## Probability of positions
However, We may got some false positives that match the condition but their relative position is incorrect.
We can filter out these error based on their position after dropped.

Those positions after dropped follow gamma distribution, where the parameters are the actual distance and drop rate.
We only take those triple with high probability to reconstruct position.

## Reconstruct position
In my solution, I propagate possible position to other constraint nearby, group them together and choice the largest one.

I also heard from other participant that we can solve this step by converting this problem to a shortest path problem,
and solve it with some well-known algorithm.

## Reconstruct the state
After you have position, just solve some linear equations to recover it,
I use a tool I wrote before which is much faster, but you can solve it with other tools like sagemath too.

You can find full exploit [here]([_files/solution/solve.py]).
