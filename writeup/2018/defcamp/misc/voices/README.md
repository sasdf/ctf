{% writeupHeader %}

{% name %}
voices

{% links %}
[Rendered GitBook version](https://sasdf.cf/ctf-tasks-writeup/)

{% category %}
misc

{% points %}
281

{% solves %}
28

{% endwriteupHeader %}

> Listen. Can you hear the voices? They are there. Somehow.

## Time
1 hours

# Solution
There are two tracks of signals on its spectrum.
There are totally 70 bits.
Extract them, zip, and convert to bytes to get the flag.
Here's the [solver]([_files/extract.py]).
