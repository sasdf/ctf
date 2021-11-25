---
name: BalsnCTF 2021
category: overview
points: 
solves: 7
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> Thanks everyone for playing BalsnCTF this year.
> Hope you guys enjoy this trip to the hell.


# Overview, Concept and Design Criteria
This year I've submitted three crypto challenges.
The difficulty of this year's crypto challenges would be slightly easier than before because

1. We always got some feedbacks that our challenges are too hard.
2. I'm out of idea :(

This year we've covered three sub-categories:
* Easy: PRNG - 1337 pins (5 solves)
* Medium: Side-channel - dlog (2 solves)
* Hard: Hash collision - trinity (0 solves)

The topics are slightly overlapped with our 2019 CTF,
which has PRNG and side-channel challenges too.
Hope I can explore more fields next year.

The difficulty about the algorithm between `dlog` and `trinity` would be similar,
but `trinity` is much more difficult to code.

Same as before, I tried to avoid paper challenges.
Unfortunately, I found a paper solving the same 3-collision problem (i.e. task `trinity`) after I finished writing it.
Since half of the challenge is about GPU programming, I decided to keep it.
