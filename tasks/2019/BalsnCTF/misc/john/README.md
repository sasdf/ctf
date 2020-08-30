---
name: john
category: misc
points: 1000
solves: 1
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}


> Plaintext is not acceptable in our confidential flag checker.  
> All traffics are encrypted.
>  
> Note: Make sure you have a standard network setup. If you're not sure, try to use GCP.  
> Our solution is tested on AWS (us-east) and GCP (us-central & asia-east).  

# Overview, Concept and Design Criteria
In fact, I just wanted to create some baby and fun challenge that leak something in packet size.

But when I implemented it,
it's NOT WORKING AT ALL.

The cute baby suddenly becomes a devel 👿 .

And it's the one of the hardest challenges that we thought no team will conquer.

## Design Criteria
I changed the oracle in this task several times,
and UTF-8 oracle seems to be the most interesting one.

Due to the fact that the packet leak is not pretty stable,
the flag is hex-encoded to increase the entropy we can got from each successful oracle.


# Solution
## Behavior
The main function looks like:
```python
def main(flag):
    sc = SecureConsole()

    sc.write(flag).endl()
       
    for _ in range(30):
        sc.write('[>] Gimme your flag: ').endl()
        line = sc.readline()

        sc.write('[*] Result: ')

        try:
            line = line.decode('utf8')
            if line == flag:
                sc.write('OK').endl()
            else:
                sc.write('Nope').endl()
        except:
            sc.write('QAQ').endl()
```

`.readline` will read null terminated ciphertext and return its plaintext.

`.write` will encrypt the data, encoded to hexstring, chunked to 80 byte lines, and then print the result.

`.endl` will pad the space in current line with encrypted null bytes to 80 bytes.

The encryption here is AES-CTR with urandom key.

With property of CTR mode, we can flip bits for input without knowing its content.

If we can somehow distinguish between those three outcomes, it's a UTF-8 oracle for plaintext.


## Packet oracle
Cipher for output is used correctly,
so they're just some random strings if you don't have the key.

All three kinds of output will be padded to same length, so there's no way to distinguish between them.

However, data and padding are printed out in two separated syscall.

Maybe we can find one packet for each syscall. Can we?

No we can't.

If you capture their packets, you will see only two packets.
One is the prompt `[*] Result: ` and another one is data + padding.
The reason is that we're trying to send three packets out.

Second and third one will be buffered and concated when waiting first one to be ACKed.
This is called [Nagle's algorithm](https://en.wikipedia.org/wiki/Nagle%27s_algorithm).

```
if there is new data to send
  if the window size >= MSS and available data is >= MSS
    send complete MSS segment now
  else
    if there is unconfirmed data still in the pipe
      enqueue data in the buffer until an acknowledge is received
    else
      send data immediately
    end if
  end if
end if
```

## Racing with Nagle
The idea to bypass it is simple: we have to ACK the first packet before second write.

Actually, this would happened with a small probability if client and server are inside the same intranet.

But we need to make it happened across Internet too.

Network latency is inevitable, we have to send ACK in advance to ACK the packet in time.

When kernel receive an invalid ACK from the future, it will think it's come from other connection.
And our connection won't be affected.

So we can send many ACK packets in advance, hoping one of them will ACK the first packet before second write.

Once we trigger that race condition, we can get one bit of oracle.

I craft and send / recv raw packets with scapy,
the performance of default L3 send is pretty bad for flooding.
You need to optimized it to make it possible for racing.


## UTF-8 oracle
The flag is hex-encoded, so here is the possible charset we need to leak:
```
a 0110 0001
b 0110 0010
c 0110 0011
d 0110 0100
e 0110 0101
f 0110 0110

0 0011 0000
1 0011 0001
2 0011 0010
3 0011 0011
4 0011 0100
5 0011 0101
6 0011 0110
7 0011 0111
8 0011 1000
9 0011 1001
```
Also, we already know the prefix is `Balsn{`, and there are some trailing null bytes.

There are some special codepoint in UTF8 is invalid.
We can use these codepoint to leak some bits.

The first oracle is `Invalid continuation`, we can leak first four bits with this oracle.
```
Query Pattern:   1101xxxx ????xxxx
Success Pattern: 1101xxxx 10xxxxxx
```

Second oracle is code points larger than `U+10FFFF`:
```
F5 - FF
Query Pattern:   1111??xx 101xxxxx 10xxxxxx 10xxxxxx
Success Pattern: 111100xx 101xxxxx 10xxxxxx 10xxxxxx
```

Third oracle is two bytes overlong encoding:
```
C0 / C1
Query Pattern:   110000?x 101xxxxx
Success Pattern: 1100001x 101xxxxx
```

And the last oracle is three bytes overlong encoding:
```
Query Pattern:   1110000? 10000000 10000000
Success Pattern: 11100001 10000000 10000000
```

You can find full exploit [here]([_files/solution/solve.py]).
