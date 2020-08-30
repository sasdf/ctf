---
name: pyshv3
category: misc
points: 906
solves: 4
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}


> Continuous delivery is awesome.  
> We deploy our code to production whenever we can.  
> No code, no vulnerability.  
> Everything works great.  


# Overview, Concept and Design Criteria
See [pyshv1](../pyshv1/index.html)


# Solution
Some participants found a unintended solution by copying `__builtins__` to module attribute,
which is much more powerful than intended solution.

But intended solution is still quite interesting and worth to take a look.


## Behavior
Many things got implemented in this version:
```python
def login(self):
    with open('../flag.txt', 'rb') as f:
        flag = f.read()
    flag = bytes(a ^ b for a, b in zip(self.key, flag))
    user = input().encode('ascii')
    user = codecs.decode(user, 'base64')
    user = pickle.loads(user)
    print('Login as ' + user.name + ' - ' + user.group)
    user.privileged = False
    user.flag = flag
    self.user = user

def cmd_flag(self):
    if not self.user.privileged:
        print('flag: Permission denied')
    else:
        print(bytes(a ^ b for a, b in zip(self.user.flag, self.key)))
```

And import is switched back to `find_class`, so that our monkey patch won't work.

The flag will pop out if `user.privileged` is truthy value, but it's set to False after our pickle loaded.
One solution is overwrite `__setattr__` so that the assignment is ignored.
It won't work because we also need the `user.flag` to be set.
(Actually, this method is the reason why this strange flag assignment logic exists)


## Descriptor
The trick of this version is descriptor,
it can overwrite the setter or getter of one specific field.

So we can ignore the assignment of `user.privileged` while leaving assignment of `user.flag` keep working.

To build a descriptor, we need to have a class with `__set__` method.
We can reuse our `User` class here by adding a `__set__` method to it.

Pickle cannot create function, we can only use existed function.
Constructor of `User` is suitable for this case, both of its arity and side effect fit.

After add `__set__` function, we can create a descriptor for `privileged` field.
Just create a `User` instance and store it at `User.privileged`.

When we accessing `user.privileged`, it will return the descriptor itself, which is truthy.
And the flag will pop out as expected.

You can find the final pickle bytecode [here]([_files/solution/solve.py]).
