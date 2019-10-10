---
name: vim
category: reverse
points: 726
solves: 8
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf/)
{% endignore %}

> A vim challenge written with [kakoune](https://kakoune.org/).


# Overview, Concept and Design Criteria
I was trying to create reverse challenge with some strange languages. (or even not a language).
This is one of them.

## Design criteria
When writing a reverse challenge,
it's not too hard to create a huge amount of 💩 which is impossible to solve,
and I want to avoid that.

To make the code reasonable,
I adopted some common pattern from asm.

For example, there are many inlined function calls, and they have prologue/epilogue to save registers.

The whole program is built from many functions, so the pattern of each function can be easily detected.

## Fun facts
* Ten days before the competition started, I suddenly realized that there's no challenge with normal architecture 😈.
* I wrote this challenge after I switched from vim to kakoune.
* I have totally no idea WTF is this 💩 one year after I wrote this challenge.


# Solution
There's no special tricks in this task,
just read and understand it.

Backtick and colon are good separators for this file.


## Register and function
I use lowercase marks to represent registers, 
and uppercase marks as stack.

In our calling convention,
`reg a` is for return value, similar to `eax`.
parameters are pushed to stack.


## Integer and list
Integers are represented by number of `x` in a line starts with `X`.

Each registers' point to a list.
which is composed of several lines of integer and an separator (i.e. empty line).

There's also some operation on lists that:
* Allocate: create separator
* Free: delete all those lines between separators
* Insert: add lines between separator.
* Access: go to nth line.


## Example
```
#----- caller -----
# Pass parameters
`bmZ    # push b ; arg0

#----- callee -----
# prologue (Save registers)
`bmY    # push b
`cmX    # push c

# Load parameters
`Zmb    # mov b, arg0

# result[@reg c] = alloc()
Go\<esc>ma    # inlined alloc()
`amc          # move return value to c

# ...

# return result[@reg c]
`cma    # move c to return value (i.e. reg a)

# epilogue (Restore registers)
`Xmc    # pop c
`Ymb    # pop b

#----- caller -----
# Save the result
# c = func(b)
`amc
```

[Here]([_files/solution/annotated.vim])
is the annotated version I parsed manually.


## Algorithm
Main algorithm is just matrix multiplication modulo 32.

The matrix is derived from first few letters in the banner.

There's also some bit operations and rot13 to obfuscate the linear property of matrix,
avoiding the algorithm to be guessed by looking at the output.

All of these operations are invertible.
You can undo them step by step.

You can find full script [here]([_files/solution/solve.py]).
