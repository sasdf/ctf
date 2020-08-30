---
name: securenote
category: crypwn
points: 1000
solves: 0
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> Notes family is known to be pwned, we secure it with SOTA encryption.
> There's nothing you can control.


# Overview, Concept and Design Criteria
This challenge is inspired by another crypto-pwn challenge, `secret note`, from HITCON CTF 2018.

The way they mixed different field is pretty great,
and I was trying to design another one by myself.

The main design criteria is that it should be a mixed challenge,
not just a multi-level challenge.

That is, you have to know how2crypto to find where to pwn,
while you also need to know how2pwn to break the cipher.
And, again, you need to know how2crypto to fully pwn the program.
So... do you know how2hack?


# Solution
## TL;DR
1. Create free chunk near the counter
2. Overflow to chunksize of top chunk
3. Allocate some chunk to change the terminator
4. Get the keystream for printing heap content
5. Create overlapped chunk by modifying the size
6. Partial overwrite to forge fd to counter
7. Reset counter
8. Get the keystream for writing
9. Use normal heap exploitation techniques to win


## Recap: AES Counter mode & nonce reuse
If you're not familiar with crypto, let me recap some property of AES-CTR we need.
* Just assume AES is a blackbox and don't dig into it.
* Encrypting in CTR mode is just xor plaintext with some random, secure, unknown keystream.
* We can recover keystream given a plain/ciphertext pair because they're just xored together.
* Keystream is always the same for same counter.

With these property, let's look the goal again:
If we leak the keystream and then reset the counter,
we can control ciphertext because we already knew what will be xored to our plaintext.

The first goal of crypto part is pwning the program to reset the counter, so that we can control the data on heap.

## Off by one
The code about creating a new note looks like:
```c
memset(buf, 0, sizeof(buf));

int nbyte = read(0, buf, sizeof(buf) - 1);

if (buf[nbyte - 1] == '\n') {
    buf[nbyte - 1] = 0;
}

char* note = malloc(nbyte);

strcpy(note, buf);
```

Instead of allocate `strlen(buf) + 1` bytes, we only allocate the number of bytes we read.

When there's no `\0` or `\n` in the string,
strcpy will copy one more null byte,
result in one byte heap overflow.

With this vulnerability,
we can modify the size of next chunk,
and exploit it with some well-known heap tricks.

However, we still can't control the content we write.


## Leak keystream
First, let's see how to leak the content (i.e. ciphertext) on heap.

Originally, I create a overlapped chunk and change the terminator byte on the next note.
But @Billy found a more brilliant way to do this.

Create a chunk with overflow to top chunk's size,
which means that the terminator is the last byte of top chunk's size.

When you allocate one more chunk,
the size (i.e. the terminator) will be changed,
and it will print excessive bytes and leak ciphertext of heap.

Those content on heap are known (default is zero),
and we have corresponding ciphertext.
XOR them together reveals the keystream of our leaker note.


## Reset counter
Now, how can we reset the counter?

With overlapped chunk,
we can modify heap but we can't control the content we write.

Deadend.

Actually, we have another way to modify heap -- free.

When we free a chunk, 
the address to free chunk list will be write to the first 8 bytes (i.e. fd).

On the other hand, when we allocate a chunk,
the first 8 bytes will be copied back to libc as the pointer of next chunk.

After we allocate on counter,
free it and then allocate it back will reset it to some unknown but fixed value.


## Allocate on counter
To allocate on counter,
we can exploit tcache.

First, we create a free chunk near the counter,
and let another free chunk's fd points to it.

And then partial overwrite fd to make it points to the counter.

Another way is to forge it byte-by-byte,
but it requires a super low latency network due to the large amount of operation needed.

To avoid giving adventange to someone who has better network,
I blocked this method by limiting the number of operation in one connection.


## Pwned
Once we are able to reset the counter,
we can control the content on heap.

The remaining parts are just as same as classic heap exploitation.

In my solution, I modify a tcache chunk's fd to mallochook and write onegadget to it.

My teammate use another solution by setting freehook to system.

There are many ways to pwn it in this step, just choice the one you like.

You can find my exploit [here]([_files/solution/solve.py]).
