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
Will be released 72 hours after the end of competition.
