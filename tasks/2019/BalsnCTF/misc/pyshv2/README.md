---
name: pyshv2
category: misc
points: 857
solves: 5
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
Now things become a little bit harder, there are two difference between these two version.

```diff
diff --git a/pyshv1/task/home/task/securePickle.py b/pyshv2/task/home/task/securePickle.py
index da5db40..6eb82f4 100644
--- a/pyshv1/task/home/task/securePickle.py
+++ b/pyshv2/task/home/task/securePickle.py
@@ -11,7 +11,8 @@ class RestrictedUnpickler(pickle.Unpickler):
     def find_class(self, module, name):
         if module not in whitelist or '.' in name:
             raise KeyError('The pickle is spoilt :(')
-        return pickle.Unpickler.find_class(self, module, name)
+        module = __import__(module)
+        return getattr(module, name)


 def loads(s):

diff --git a/pyshv1/task/home/task/server.py b/pyshv2/task/home/task/server.py
index 7c008b7..3fc63be 100755
--- a/pyshv1/task/home/task/server.py
+++ b/pyshv2/task/home/task/server.py
@@ -4,13 +4,16 @@ import securePickle as pickle
 import codecs


-pickle.whitelist.append('sys')
+pickle.whitelist.append('structs')


 class Pysh(object):

 # ...

diff --git a/pyshv2/task/home/task/structs.py b/pyshv2/task/home/task/structs.py
new file mode 100644
index 0000000..8b13789
--- /dev/null
+++ b/pyshv2/task/home/task/structs.py
```

First thing is that we are only able to import an empty module `structs` now.
Second thing is that we use `__import__` here.

The trick of this challenge is monkey patching.
`__import__` is a builtin function in `__builtins__`, which is a dict shares among all modules.

We can overwrite `__import__` by overwriting `structs.__builtins__`.

Overwrite `__import__` with `structs.__getattribute__`,
we can retrieve some attributes deeper inside, just like what we did in `pyshv1`.

You can find the final pickle bytecode [here]([_files/solution/solve.py]).
