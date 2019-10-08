---
name: vim
category: reverse
points: 726
solves: 8
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}

> A vim challenge written with [kakoune](https://kakoune.org/).


# Overview, Concept and Design Criteria
I was trying to create reverse challenge with some strange languages. (or even not a language).
This is one of them.

## Design criteria
When writing a reverse challenge,
it's not too hard to create a huge amount of 💩 which is impossible to solve,
and I want to avoid that.

To make the code reasonable,
I adopted some common pattern from asm.

For example, there are many inlined function calls, and they have prologue/epilogue to save registers.

The whole program is built from many functions, so the pattern of each function can be easily detected.

## Fun facts
* Ten days before the competition started, I suddenly realized that there's no challenge with normal architecture 😈.
* I wrote this challenge after I switched from vim to kakoune.
* I have totally no idea WTF is this 💩 one year after I wrote this challenge.


# Solution
Will be released 72 hours after the end of competition.
