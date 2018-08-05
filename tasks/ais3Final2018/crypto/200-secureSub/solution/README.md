# TL;DR
Solve the substitution cipher with hill climbing / genetic algorithm.


# Overview, Concept and Design Criteria
This challenge runs substitution cipher on encoded string,
so online services like quipquip won't work.
There are many articles about how to solve substitution cipher under base64,
and that is why I choose uuencode rather than base64.


# Solution
A common method to solve substitution cipher (and many other classical cipher)
is to model the task as an optimization problem:
Given a fitness function on decrypted data,
we want to find a key which maximize that fitness function.
Since our plaintext is in English,
we have to find some fitness function that measure how silmiar the decryped text is to English.
There are many language model you can found on the Internet, and one popular option is ngram.
To optimize our key, we can use hill climbing (or more sophisticated genetic algorithm) for approximating global optima.

You can find a implementation of hill climbing algorithm in `hill.py` and a implementation of genetic algorithm in `ga.py`,
where genetic algorithm produce slightly better result than hill climbing and much more stable.
In my solution, I choose trigram log probabilities from wikidump as fitness function.
The mutation of key is randomly swapping two characters.
It may converge to local optima, you may need to run it several times.
The result isn't always perfect, but it is clear enough to fix it manually.
