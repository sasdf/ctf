---
name: john
category: misc
points: 1000
solves: 1
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}


> Plaintext is not acceptable in our confidential flag checker.  
> All traffics are encrypted.
>  
> Note: Make sure you have a standard network setup. If you're not sure, try to use GCP.  
> Our solution is tested on AWS (us-east) and GCP (us-central & asia-east).  

# Overview, Concept and Design Criteria
In fact, I just wanted to create some baby and fun challenge that leak something in packet size.

But when I implemented it,
it's NOT WORKING AT ALL.

The cute baby suddenly becomes a devel 👿 .

And it's the one of the hardest challenges that we thought no team will conquer.

## Design Criteria
I changed the oracle in this task several times,
and UTF-8 oracle seems to be the most interesting one.

Due to the fact that the packet leak is not pretty stable,
the flag is hex-encoded to increase the entropy we can got from each successful oracle.


# Solution
Will be released 72 hours after the end of competition.
