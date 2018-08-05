# TL;DR
* Solution1: Reassemble the binary in normal order.
* Solution2: Remove junk code and believe IDA can understand it.


# Overview, Concept and Design Criteria
In this challenge,
I shuffled all the opcodes and use jmp to connect them with original execution order.

I was thinking that it won't be too difficult to design such challenge.
However, the strength of HexRay decompiler was beyond my expectations.
If you just jump directly to next opcode, IDA can decompile it with about 30% of chance.
I hardened the jump gadget in several attempts to make it completely unrecognizable to IDA.
For more details of jump gadget, see the appendix of Obfuscation at the bottom.

The underlying encryption algorithm is [TEA](https://en.wikipedia.org/wiki/Tiny_Encryption_Algorithm),
where I changed the delta magic constants to one of sha256's initial state.
(Hope that didn't make you thought it was sha256 xD.)

The program will encrypt the flag in CBC mode. In CBC mode, if you slightly modify the plaintext,
only the block you modified and blocks after it will be changed.
In order to introduce avalanche effect, I decided to encrypt the data with CBC mode for multiple rounds.
As the result, whole ciphertext will change dramatically even if you just increase a single character.

Although I failed to solve it directly with angr,
z3 seems to be able to solve TEA(16 iteration variant).
In order to totally eliminate the chances of being solved by symbolic execution,
I substitute the result of TEA using SBox from AES.
Symbolic execution hates array indexing :)
(Again, hope that didn't make you thought it was AES xD.)


# Solution

## Detect Fragments
Fortunately, the pattern of the jump gadget can be easily detected.
You can find each gadget by searching absolute move of r15 (`\x49\xc7\xc7`),
and find the address of next fragment in lea before it.

You can also find each fragments using symbol table,
each fragment is tagged with `L_{xxx}_GLUE{id}`,
where id actually means its original position.

## A Easier but Weaker Method -- Directly Jump to Next Fragment
As I mentioned in overview,
IDA can understand the code if you replace all jump gadgets with direct jump.
Fix the address by subtracting 42 from it, and patch lea to nop and jmp.

Now IDA can decomplied the program for you,
If you think those local variables looks bad,
you can change the type of `a1 @ rbp` to a custom structure to create a variable for each local variable.

You can find the implementation of this method in `directJmp.py`.

## A Harder but Better Method -- Reassemble the Binary
This was the original intended solution before I start implementing the challenge.

Sort the fragments by execution order and it becomes a normal reversing challenge.
There are some instructions reference relative to rip,
so you need to relocate the offset when you moving it.

To make IDA decompile correctly, you also need to fix symbol table (.symtab section).
IDA will refuse to create a function if there are labels inside functions.
You can simply strip the binary to remove whole symbol table.
Or you can relocate function symbols, and remove GLUE tags by pointing to some invalid address such as NULL.

You can find the implementation of this method in `reassemble.py`.
The code using `capstone` for disassembling, `keystone` for assembling,
and `pyelftools` for parsing ELF.

There are also many other tools that can help you modify binary such as `miasm`.


# Other Possible Solving Ideas
There some solutions I didn't test, but I think those may work:

## Execution trace
Recorded all opcode executed and filter the jump gadget.
One disadvantage is that you need to analyze the program at assembly level.
There are a lot of reversing writeup of other challenge using this technique.

## Dynamically debugging
There are about 300 shattered fragments,
and there's no crazily complex x86 instructions.
It may be possible to set a access breakpoint on the memory of flag,
observe the difference, and derive the operation applied on it.


# See also
If you are interesting in this topic,
take a look at
[this great article](https://blog.quarkslab.com/deobfuscation-recovering-an-ollvm-protected-program.html)
about deobfuscation of ollvm.
It has a much stronger protection on jmp destination using fake control flows,
and they remove it by symbolic execution.

Thanks Inndy for telling me about ollvm.


# Appendix - Obfuscation
Here are the some result of my several attempts to confuse the decompiler.

### Naive jump
Directly jmup to next opcode.

IDA can recognize all the function chunks with high probabilities.
It may skipped some chunks if there are too many chunks.

### Indirect jump
These gadgets has similar effect:
* `lea r15, addr; jmp r15`
* `lea r15, addr + 42; lea r15, [r15 - 42]; jmp r15`
* `lea r15, addr + 42; mov jmpaddr, r15; mov r14, jmpaddr; lea r15, [r14 - 42]; jmp r15`
* Save the destination address in a register or memory, and jump to a shared gadget that performs actual jump.

The indirect jump make IDA failed to decompile the whole function.
Instead, it thinks each chunks as a function.
Also, it can recognize the correct destination address even if you add a constant to it.
For example, it will create code looks like this for each chunk.
```C
a += b; // The opcode for this chunk
jmpaddr = sub_xxxx + 42;
v3 = sub_xxxx;
JUMPOUT(__CS__, v3);
```
For the last variant, I thought the shared gadget should be decompiled as a seperated function.
In fact, it expanded inline into each decomplied function. It has same result as above example.

### Recursive indirect
In order to make the jump gadget to be decompiled as a seperated function,
I constructed it as a recursive function, which cannot be expanded.
The gadget swaps two variable A, B, and jump to A.
Passing (A, B) = (destination, gadget) actually performs `jmp gadget; jmp gadget; jmp dest`.
With this gadget, IDA failed to detect correct destination address.
It will produce some code like this:
```C
a += b; // The opcode for this chunk
jmpaddr1 = &loc_xxxx + 2; // We are actually refering to loc_xxoo + 42
jmpaddr2 = &loc_oooo + 5; // Actually loc_oxox + 42, which is the jump gadget.
JUMPOUT(__CS__, loc_oxox);
```
However, objdump can resolve destination address correctly because it is an unstripped binary.
