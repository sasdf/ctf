---
name: secops
category: web
points: 316
solves: 20
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}


## Time
3 hours  
For trying different bypass methods

# Solution
The cookie is a json object which has a key `flair` storing the selected ID.
One of my team-mate(@shw) told me that there's SQL injection in the value of `flair`.
There's also a WAF to filter injection payload.
To bypass it, I use:
```
' or #\n [payload]
```
The WAF thinks the payload is comment but it isn't.
Then just bruteforce each bytes to get the flag.

# Additional Notes
There's a better solution to bypass the WAF -- \u unicode encode in json.

