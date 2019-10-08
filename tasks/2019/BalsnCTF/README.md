---
name: BalsnCTF 2019
category: overview
points: 
solves: 720
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}

> Thanks everyone for playing BalsnCTF this year.
> Hope you guys enjoy this trip to the hell.


## Fun facts
* Ten days before the competition started, I suddenly realized that there's no challenge with normal architecture 😈.
* I wrote a vim challenge after I switched from vim to kakoune.
* I have totally no idea WTF is this :poop: one year after I wrote vim challenge.
* `collision` is the first solved non-trivial challenge.
* I thought `unpredictable` is the hardest one among those crypto. Apparently, it's not.
* I planned to create a ML task, everything is ready, but the model refused to be trained. (That's what we faces everyday when researching ML).


# Overview, Concept and Design Criteria
## Reverse challenges
Created a series of reverse challenge in strange language,
No IDA is need :)

Yep, they are totally unreal and useless,
but it's pretty fun for me to find a way abusing these things.

Hope that we can have bunch of strange things next time.

## Crypto challenges
I don't like paper challenges, although I learnt a lot from them because I usually won't read crypto papers.

All crypto challenges I wrote this year don't have a paper,
and all you need is on wikipedia.
(Because I grab those idea from there. LOL)

Just read those wiki and burn your brain.
You can solved it if your brain is not overheated.

I was pretty shocked that my challenge got so many solves.
Realized I'm a noob again.

## Misc challenges
The main design criteria is fun, and without guessing.

I thought I know python pretty well, until I got some unintended solutions from the participants.

## Crypto pwn challenge
This category is inspired by another crypto-pwn challenge, `secret note`, from HITCON CTF 2018.
It's a pretty great challenge, take a look if you didn't know it before.

The main design criteria is that it should be a mixed challenge,
not just a multi-level challenge.

That is, you have to know how2crypto to find where to pwn,
while you also need to know how2pwn to break the cipher.
And, again, you need to know how2crypto to fully pwn the program.
So... do you know how2hack?
