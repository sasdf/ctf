---
name: Chains of trust
category: rev
points: 391
solves: 10
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.cf/ctf-tasks-writeup/)
{% endignore %}

> Yet another reverse engineering challenge.


## Time
7 hours.

I skipped a lot of parts in this challenge using network interception.
If you want to know what those shellcodes are,
see writeup from p4.


# Solution
This is a interesting reverse challenge with anti-debugging, multithreading, and remote shellcodes.

## TL;DR
1. Delay the delivery of shellcodes with a MitM proxy
2. Find out which one is the checker by observing the timing of message `No luck.`
2. Modify the checker to print encrypted input
3. Bruteforce the flag

## Main binary
Here's the pseudo code of the binary the task provides.
The binary read shellcodes from the server and run them.
```C
void main2(char* host) {
  puts("Welcome to Chains.");
  printf("Connecting to master...");
  if ( dns(&context, host, 0x1DFFu) ^ 1 ) {
    puts("FAILED");
  } else {
    puts("OK");
    read_nbyte(&context, &arg, 1);
    while ( byte_204060 != 1 ) {
      bytes_read = read_nbyte(&context, &size, 4);
      if ( bytes_read != 4 ) {
        return print("Master disconnected (timeout?)\n");
      }
      len = (size + 4095LL) & 0xFFFFFFFFFFFFF000LL;
      addr = mmap(0LL, len, 7, 34, -1, 0LL);
      if ( !addr ) {
        return print("mmap failed, this should not happen unless you're doing sth weird.\n");
      }
      bytes_read = read_nbyte(&context, addr, size);
      if ( bytes_read != size ) {
        return print("Master disconnected (timeout?)\n");
      }
      arg = addr(funcs, arg);
      munmap(addr, len);
    }
  }
}
```

## Shellcodes
Some of the shellcodes are for anti-debugging.
It will refuse to run if you hook it with strace.

By intercepting the traffic using wireshark,
I found that this program won't send our input to the server.
The server must send some code for checking the flag.

I wrote a [mitm proxy]([_files/proxy.py]) to block those shellcodes.
The main UI will show up when you send 22nd shellcode,
and print `No luck.` when you send 85th shellcode.

Those shellcode are encrypted and there's a decryptor at the beginning.
I use a [runner]([_files/runner.c]) to run them, trace it with `gdb`,
and use `gcore` command to dump the shellcode after decrypted.


## Checker
Here's the pseudo code of the checker.
```C
int entry(a1) {
  v4[0] = byte_DEADB905;
  v4[1] = byte_DEADB92D;
  // ...
  v4[31] = byte_DEADBCED;
  for ( i = 0; i < 32; ++i ) {
    read_uint16(inp, *(a1 + 56), i + 64);
    hash(inp, &v3);
    for ( j = 0; j < 32; ++j )
      failed |= v4[i][j] ^ v3[j];
  }
  if ( failed ) {
    v1 = "No luck.";
  } else {
    v1 = "\x1B[38;5;46mYes! Well done!";
  }
}
void __fastcall hash(uint16 inp, char* out) {
  state = inp;
  v4[0] = 0x9DF9;
  v4[1] = 0x65E;
  // ...
  v4[31] = 0xBDD1;
  for ( i = 0; i < 32; ++i ) {
    v2 = rotateRight(state);
    state = v2 ^ v4[i];
    out[i] = state;
  }
}
```
It read a 16bit integer from another thread and check to a hardcoded target.
Since it is only 16bit, [bruteforce]([_files/target.py]) the result won't take too much time.
The result looks like `[0x46ca, 0x4187, 0x5582...]`,
which doesn't look like ascii.

## Debugging
To attach gdb on the process, We need to skip shellcodes for anti-debugging.
I disable ASLR, record the traffic with [record.py]([_files/record.py]) and replay it with [replay.py]([_files/replay.py]).
Run the binary with strace, now we can just throw away all anti-debugging chunks when replaying.

The checker got `[18685]*8 + [13927, ...] + [5548]*8 + [16696]*8` when input are all `a`.
If I change a byte in the input, only one byte in output will change!!
The index mapping is `0, 8, 16, 24,   1, 9, 17, 25,   2...`.

## Bruteforce the flag
To bruteforce the flag,
I modified the shellcode of checker to make it print the input and exit.
```asm
; Save the results to an array
load:00007FFFF7FEE58D                 call    read_uint16
load:00007FFFF7FEE592                 movzx   eax, ax
load:00007FFFF7FEE595                 mov     esi, [rbp+i]
load:00007FFFF7FEE598                 mov     word ptr [rbp+rsi*2+arr], ax
load:00007FFFF7FEE5A0                 jmp     short loc_7FFFF7FEE5ED

...

; Output the array and exit
load:00007FFFF7FEE5AF                 mov     rdi, 1          ; fd
load:00007FFFF7FEE5B6                 lea     rsi, [rbp+arr]  ; buf
load:00007FFFF7FEE5BD                 mov     rdx, 40h        ; count
load:00007FFFF7FEE5C4                 mov     rax, 1
load:00007FFFF7FEE5CB                 syscall                 ; LINUX -
load:00007FFFF7FEE5CD                 mov     rax, 0E7h
load:00007FFFF7FEE5D4                 mov     rdi, 0
load:00007FFFF7FEE5DB                 syscall                 ; LINUX -
```
Then just [bruteforce]([_files/brute.py]) it byte-by-byte to recover the flag.
I just solve it 6 minutes before second blood.
Thanks god that I implemented the bruteforcer with multiprocessing :)
