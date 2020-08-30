---
name: plam
category: reverse
points: 1000
solves: 1
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> I tried my best, but it's still a little bit slow.
> It will tell you the result after several years.


# Overview, Concept and Design Criteria
I'm a big fans of lambda calculus. It's pretty beautiful.
Three simple rules but pretty powerful.

Initially, I was trying to wrote this task with python's lambda.
However, I can't construct one of the most mind-blown stuff -- fixed point operator,
and it's also difficult to curry those lambdas.

plam works well before I switched to postfix representation.

Postfix representation looks pretty great,
I have no choice but implement a 
[interpreter]([_files/exec/main.cpp]) 
by myself to verify the challenge.

The interpreter is implemented using
[De Bruijn index](https://en.wikipedia.org/wiki/De_Bruijn_index).
It's a representation of lambda function which is invariant with respect to α-conversion.
With this property, we can cache and retrieve reduction rules in very efficient way.

## Designed Criteria
The core of this flag checker is a system of GF2 (i.e. boolean) linear equations.
To avoid it to be guessed, I generate product of 4 sums in each run.
So only 1/16 of results will be true, which make blackbox analysis much harder.
And also make the code more complicated 😈 .

Also, I don't want it to be solved with z3 after you convert those things to boolean operations without understanding them,
so I added some branches to it.
The complexity will explode for z3.


# Solution
You can find the source of that lambda program [here]([_files/source/def.txt]).

Open the file, you will see a long line consist of these sections:
```
\abcdefghi.(\j.(...) (...))

(j e e e e e e g e e g g g ... g g e e e e b) (...) (...)

f a e g (c d c c[52] c[12] c[80] c[41] c[48] ... h[57] h h[68] h h[88] h e)

Some other lambda
```

The first part is a closure that load some global functions from its parameters.

The second part is the return value of this function, it may be the main function.
Also, the second and third parts are very long and random, it looks like some embedded data.

Remaining parts are the definition of global function.

Term in the form of `c[x]` or `h[x]` are input bits.

if bit x in 0, all `c[x]` and `h[x]` will be replaced to `c` and `h` when we generating plam script.

Otherwise, all `c[x]` and `h[x]` will be replaced to `d` and `i` when we generating plam script.

Intended solution is understand those lambda and write a solver for it.
There's no other tricks because we don't even have a interpreter that can run it.

Let's try to understand the algorithm with original source code before uglified.

## Basic primitive types
```python
# Boolean [x: true branch, y: false branch]
T = λx.λy.x    # global function e
F = λx.λy.y    # global function g

# Pair -- tuple [x: first elem, y: second elem, f: callback(first -> second -> res)]
P = λx.λy.λf . f x y

# Tree node -- triple [v: node value, r: right, l: left, f: callback(node_value -> right -> left -> res)]
N = λv.λr.λl.λf . f v r l
```

These types are 
[Church encoding](https://en.wikipedia.org/wiki/Church_encoding) 
of boolean and list.


## Postfix representation
Let's take a look at section
```
c d c c[52] c[12] c[80] c[41] c[48] ... h[57] h h[68] h h[88] h e
```

It looks like a list, but it's actually stack-based tree builder for postfix binary tree representation.

```python
# Shift [n: node value, t: top, s: stack, c: callback(top -> stack -> res)]
# Pseudo code:
#     stack.push(top)
#     top = node_value
#     return (top, stack)
S = λn.λt.λs.λc . c n (P t s)


# Reduce [n: node value, t: top, s: stack, c: callback(top -> stack -> res)]
# Pseudo code:
#     left, right = stack.pop(), top
#     top = Node(node_value, right, left)
#     return (top, stack)
R = λn.λt.λs.λc . c (N n t (s T)) (s F)

# Bind the data to function partially
# Type: top -> stack -> next_instruction -> res
A = S F    # global function c
B = S T    # global function d
C = R F    # global function h
D = R T    # global function i
```

First three characters `c d c` setup the initial (invalid) state of that builder,
so that we can start chaining the function using callback.

The last instruction `e` is `T`, it will take two argument and return the first one, which is the top value (i.e. builded tree).

Actually, those callback can be replaced by returning tuple, but I think using callback will make it looks more complicated :)


## Tree Walking
Now, we have a tree, the main function must walking in that tree.
```
j = f a e g (tree)
((j e e e e ... g g e e e e b) (...) (...)) ((...) (...) (...)) g ((...) (...) (...)) g
```

The algorithm here is to generate some product of sum boolean expression.
And combine them with some branch or AND operation.

Let's take a look at implementation.

In each step, we extract two elements from the tree with two indices.
```python
# Unpack1 -- unpack level 1
V = λi.λv.λr.λl.λc . (i r l) (c v)

# Unpack2 -- unpack level 2
W = λj.λv.λw.λr.λl.λc . c v w (j r l)

# Unpack -- unpack two entries from tree [i: index1, j: index2, l: tree, c: callback(value1 -> value2 -> tree -> res)]
# Pseudo code:
#    value1 = tree.val
#    tree = tree.child[index1]
#    value2 = tree.val
#    tree = tree.child[index2]
#    return (value1, value2, tree)
U = λi.λj.λl.λc . l (V i) (W j) c
```

And then we change the state based on those elements and the index.
```python
# process -- calculate binary function [i: index1, r: result, x: accumulator, v: op, w: val, l: tree, c: callback(result -> accumulator -> tree -> res)]
# Pseudo code:
#     if index1 == op:
#         result &= accumulator
#         accumulator = val
#     else:
#         accumulator ^= val
#     return (result, accumulator, tree)

# G = \i r x v w l c . (xor i v) ( c r (xor x w) l ) ( c (and r x) w l )
G = (λi. (λr. (λx. (λv. (λw. (λl. (λc. ((((i ((v F) T)) v) (((c r) ((x ((w F) T)) w)) l)) (((c ((r x) F)) w) l)))))))))
```
All op in the path we walked are constant.
So the result of `(j e ... e b)` is product of sums for some boolean expression.


## Y combinator
Different from the tree builder that we chaining the functions by callback,
we use a fancy technique here -- Y combinator.

Y combinator is a special function in untyped lambda can be used to define recursive functions.
```python
# Y combinator -- An infinite recursive operator
# global function f
# 
# Yf = f (Yf)
Y = λf . (λx . f (x x)) (λx . f (x x))
```
It looks like it will never stop at first glance.

Actually, we can stop recursion by stop evaluating the first argument.

Here's a simple example of implement addition using Y combinator:
```python
step = λf.λa.λb.(
    if b != 0:
        return f (a + 1) (b - 1)
    else:
        # b == 0
        return a
)
add = λa.λb. Y step a b
```

Let's come back to our reverse challenge:
```python
# run -- execute single step in tree [f: recursive, r: result, x: accumulator, l: tree, i: index1, j: index2]
H = λf.λr.λx.λl.λi.λj . U i j l (G i r x) f

# run2 -- Y combinator compatible run
# global function a
# 
# Pseudo code:
#     while True:
#         i, j = input()
#         if j is bool:
#             result, accumulator, tree = run(result, accumulator, tree, i, j)
#         else:
#             return (_, _, _, result, accumulator, tree, i, j)
R = λf.λr.λx.λl.λi.λj . (j H H) f r x l i j

# End -- return r
# global function b
E = λa.λb.λf.λr.λx.λl.λi.λj . r
```

## Combine boolean expression
We're almost there, there's only one missing puzzle.

We can see those pathes grouped as follows:
```
((j e e e e ... g g e e e e b) (...) (...)) ((...) (...) (...)) g ((...) (...) (...)) g
```

We already know that `(j e ... e b)` is a boolean expression.
Evaluate a boolean value in Church encoding is branch.
```python
p a b
# is equivalent to
if p:
    return a
else:
    return b

# --- #

x y F
# is equivalent to
x and y
```

## Recover the flag
After parsing the data, We can figure out that the algorithm looks like:
```
ret = 1
for i in range(0, 16 * 3, 3):
    if expr[i]:
        ret &= expr[i+1]
    else:
        ret &= expr[i+2]

# All expr are product of 4 sums: (v11 + v12 + ...) & (v21 + v22 + ...) & (v31 + v32 + ...) & (v41 + v42 + ...)
```

The intended solution here is to try all 65536 possible branches and solve the system of linear equations for each branch.

I solve those equations with sagemath, but I think z3 may also works if you iterate through all those possible branches manually.

You can find full script [here]([_files/solution/solve.sage]).
