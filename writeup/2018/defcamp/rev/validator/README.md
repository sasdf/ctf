{% writeupHeader %}

{% name %}
validator

{% links %}
[Rendered GitBook version](https://sasdf.cf/ctf-tasks-writeup/)

{% category %}
rev

{% points %}
369

{% solves %}
8

{% endwriteupHeader %}

> Like any good admin, we don't store the flag, we validate that it can be generated.

## Time
6 hours


# Solution
## TL;DR
1. Extract the xor table
2. Recover the order of goroutine chain
3. Recover the last output (i.e. flag)
4. Append `}` to the flag

This is a challenge about Go and goroutine.
To recover the symbol, see
[Reversing GO binaries like a pro](https://rednaga.io/2016/09/21/reversing_go_binaries_like_a_pro/).


## Main
IDA Pro doesn't support stack calling convention that Go use.
Argument and return value are not correct,
You'll need to check the asm code to figure out correct values.

First loop in main is:
```C++
for ( i = 0LL; i <= const_num_11; i = v6 ) {
  _i = i;
  runtime_makechan(a1, v6, i, v10, v7, v8, &unk_49B3C0, 1uLL);
  v12 = _i;
  v13 = inputLen;
  if ( _i >= inputLen )
    runtime_panicindex(a1, v6);
  v14 = channels;
  a1 = &channels[_i];
  if ( dword_572D30 )
    runtime_gcWriteBarrier(a1);
  else
    channels[_i] = a9;
  v6 = (v12 + 1);
  v9 = v13;
  v10 = v14;
}
```
It create 11 channels and store to an array.

Second loop is:
```C++
for ( j = 0LL; j < const_num_11; ++j )
{
  if ( j >= _inputLen || j >= qword_54FC38 )
    runtime_panicindex(j, _inputLen);
  if ( const_num_11 == -1 )
    v20 = 0LL;
  else
    v20 = (*(off_54FC30 + j) ^ *(v16 + j)) % const_num_11;
  if ( v20 >= const_num_11 )
    runtime_panicindex(j, _inputLen);
  if ( j >= v9 || j + 1 >= v9 )
    runtime_panicindex(j, _inputLen);
  v19 = v10[j + 1];
  runtime_newproc(j, _inputLen, v10[j], v10, j + 1, const_num_11, 0x18u, &off_4C31F0, v10[j]);
  v9 = inputLen;
  v10 = channels;
  v15 = a7;
  v16 = v47;
  _inputLen = inputLen;
}
```
It spawning 11 new processes (i.e. goroutine). The arguments is actually:
```asm
mov     rbx, [rcx+rdi*8+8]               ; rcx = channels, rdi = i
mov     [rsp+0E8h+var_D0], rbx           ; arg1 = rbx = channels[i+1]
mov     [rsp+0E8h+var_D8], rdx           ; arg0 = rdi = channels[i]
mov     [rsp+0E8h+var_C8], rax           ; arg2 = rax = key[k]
mov     dword ptr [rsp+0E8h+var_E8], 18h ; arguments has 24 bytes on stack
lea     rax, off_4C31F0
mov     [rsp+0E8h+var_E0], rax           ; func = rax = &main__Z
call    runtime_newproc
```
It forms a chain of goroutine.
Proc i will have a channel between Proc i-1 and another channel to Proc i+1.

For the argument 2, `k = (input[i] ^ 0x542138[i]) % 11`:
```
.noptrdata:0000000000542138 unk_542138      db  83h                 ; DATA XREF: .data:off_54FC30↓o
.noptrdata:0000000000542139                 db  23h ; #
.noptrdata:000000000054213A                 db  42h ; B
.noptrdata:000000000054213B                 db  69h ; i
.noptrdata:000000000054213C                 db  23h ; #
.noptrdata:000000000054213D                 db 0B2h
.noptrdata:000000000054213E                 db  0Eh
.noptrdata:000000000054213F                 db  28h ; (
.noptrdata:0000000000542140                 db  97h
.noptrdata:0000000000542141                 db 0DFh
.noptrdata:0000000000542142                 db  14h
```
and keys is a array of structures in 0x553C60 (totally 11 * 0x58 bytes long).
```
.data:0000000000553C60 qword_553C60    dq 0                    ; DATA XREF: .data:off_54FC50↑o
.data:0000000000553C68                 dq offset unk_5426E0
.data:0000000000553C70                 dq 13h
.data:0000000000553C78                 dq 13h
.data:0000000000553C80                 dq offset unk_5426C0
.data:0000000000553C88                 dq 13h
.data:0000000000553C90                 dq 13h
.data:0000000000553C98                 dq 1Ah
.data:0000000000553CA0                 dq offset unk_542F00
.data:0000000000553CA8                 dq 24h
.data:0000000000553CB0                 dq 24h
...
```

Then it creates a result channel and creates two other process with different functions:
```C++
lastChan = __channels[v9 - 1];
runtime_makechan(j, _inputLen, v15, &unk_49B440, off_54FC50, qword_54FC58, &unk_49B440, 1uLL);
resultChan = a9;
runtime_newproc(j, _inputLen, v21, &hashChecker, v22, v23, 0x10u, &hashChecker, lastChan);
runtime_newproc(j, _inputLen, v24, &procTimeout, v25, v26, 8u, &procTimeout, resultChan);
a8 = v47;
v56 = inputLen;
v57 = v43;
runtime_chansend1(j, _inputLen, v27, v28, v29, v30, a7, &a8);
isCorrect = 0LL;
runtime_chanrecv1(j, _inputLen, v31, v32, v33, v34, resultChan, &isCorrect);
if ( isCorrect == 1 ) {
  // print correct
  // ...
} // else if ...
```
Check the arguments in asm like what we just done,
It passes the last element in channels and the result channel to hashChecker (`main___CRRt`).
It passes the result channel to procTimeout(`main___4`).
Then it sends the input to the first channel,
and waits for the result and output it.


## Timeout and hash checker
procTimeout send 2 to the result channel after 1 second.
hashChecker send 0 if the data from the last channel is correct, otherwise send 1.
You could nop procTimeout to avoid the program exiting while debugging.
```C++
__int64 __fastcall main___4(__int64 a1, __int64 a2, __int64 a3, __int64 a4, __int64 a5, __int64 a6, __int64 a7) {
  if ( &retaddr <= *(__readfsqword(0xFFFFFFF8) + 16) )
    runtime_morestack_noctxt(a1, a2);
  time_Sleep(a1);
  return runtime_chansend1(a1, a2, v7, v8, v9, v10, a7, &unk_4CF870);
}
__int64 __fastcall main_CRRt(__int64 a1, __int64 a2, char a3, __int64 a4, __int64 a5, __int64 a6, __int64 a7, __int64 a8) {
  if ( &v26 + 8 <= *(v8 + 16) )
    runtime_morestack_noctxt(a1, a2);
  *&v32 = 0LL;
  *(&v32 + 8) = 0LL;
  runtime_chanrecv1(a1, a2, a3, v8, a5, a6, a7, &v32);
  crypto_sha512_Sum512(a1, a2, v32, __PAIR__(v9, v33), v32, v10);
  v24 = v20;
  v25 = v21;
  v26 = v22;
  v27 = v23;
  v28 = xmmword_4D03A0;
  v29 = xmmword_4D03B0;
  v30 = xmmword_4D03C0;
  v31 = xmmword_4D03D0;
  bytes_Equal(a1, a2, v11, v12, v13, v14, &v24, 64LL, 64, &v28, 64LL);
  if ( BYTE8(v21) )
    result = runtime_chansend1(a1, a2, v15, v16, v17, v18, a8, &success_0);
  else
    result = runtime_chansend1(a1, a2, v15, v16, v17, v18, a8, &notQuite);
  return result;
}
```


## Transformer Chain
The function takes three arguments: input channel, output channel, and a structure about key.
```C++
__int64 __fastcall main__Z(__int64 a1, __int64 a2, char a3, __int64 a4, __int64 a5, __int64 a6, __int64 a7, __int64 a8, _QWORD *key) {
  runtime_chanrecv1(a1, a2, a3, v9, a5, a6, a7, &input);
  // Check part of input is correct
  for ( i = 0LL; ; ++i ) {
    v14 = key[1];
    if ( i >= key[2] )
      break;
    v15 = i + *key;
    if ( v15 >= nrecv )
      return _nrecv;
    if ( v15 >= nrecv || (v14 = (input[v15] ^ v14[i]), v10 = key[5], i >= v10) )
      runtime_panicindex(v14, i);
    if ( v14 != *(key[4] + i) )
      return _nrecv;
  }
  
  // data[key[7]:][:key[9]] ^= key[8][:]
  for ( j = 0LL; ; ++j ) {
    v17 = key[8];
    v18 = key[9];
    if ( j >= v18 )
      break;
    v19 = j + key[7];
    if ( v19 >= _nrecv )
      return _nrecv;
    if ( v19 >= _nrecv )
      runtime_panicindex(v17, j);
    v10 = _input[v19];
    _input[v19] = v10 ^ v17[j];
  }
  
  // Send data to next goroutine
  *&_nrecv = runtime_chansend1(v17, j, SBYTE8(_nrecv), _input, v18, v10, a8, &v23);
}
```
It will check partial data is same as expected,
change partial data by xor with a array in key.
and send to next goroutine.
The operations are:
```
Keys:
Index 0
[ 0:19] == 8321436325b1062c90da1db8f11bd94d3b0892
[26:62] ^= 6d955bc81686c8ed201d0767c68627f2e4fa3dea42583f6f45d451c580da6b38f6cc8d12

Index 1
[10:35] == 1db8f11bd94d3b089241dbef5bc359544dbbaa11efd7143b89
[ 6:59] ^= 46d0ba9f2f3a311f9bba0b03fb8cfa15294ff4bb1e62a68bd1ebbb6ef390a10918ba7d81e4ae745327acde37b26fc3d1d2034fe744

Index 2
[ 5:56] == b1062c90da1db8f11bd94d3b089241dbef5bc359544dbbaa11efd7143b896579cacefa585455da8673f7c702b9c0059e262d15
[53:69] ^= 521ae780305adaa32d47c3029cda6def

Index 3
[53:69] == e9d24b93a792a29b86820f6c2d353134
[ 5:31] ^= 2399ca610a706ee1ec7166774a4f6f4a12636c71dc5d6667b58e

Index 4
[40:65] == 14fc4ead8adfe51fce9cf06310e9d24b93a792a29b86820f6c
[31:49] ^= 1fb4383ac04216fd5b139f825200bd16761b

Index 5
[42:63] == c79bc1fa7bbb5acd2b8a8c29d24b93a792a29b8682
[14:63] ^= 23e2c47ae01f01c3831310299a76ead67d03dd6bff00188fec87de5e98a07f4da6ba647d5f2a6afcd7274a8761450b9daf

Index 6
[24:53] == adef53d90c9a3e3caf557af5d8c3d64025d5b174f220d044956ef06310
[26:48] ^= 67ef79da9281a66d2c8a84dfe60fae4d9e1151d26621

Index 7
[45:63] == 62f369d59cf06310e9d24b93a792a29b8682
[32:54] ^= 62d5c448202c0a9940cf0b644b9888d28f51dbe99cc0

Index 8
[17:64] == 4126a26be811e0dc33695012f522bd0938567f5c1c304f8b982f65a3f2b665956ef06310e9d24b93a792a29b86820f
[ 0:50] ^= c76217255ea3ec027e2b208d438d284be50fa38e0c48f0c0fe2b961f9a4539c4348c659210cf04aa9f6461c8292d537a5bf2

Index 9
[34:66] == 326536662fa099f25f3bbeb7dd013eb074a0e6d5056cd920f3e7901b2d0f6c2d
[38:66] ^= 4e95af906a5a8a83be325881429582b6335cee4691dfa7291a3b094c

Index 10
[12:53] == c00442f7300b69cd21fa728cadef53d90c9a3e3caf557af5d8c3d64025d5b174f220d06bdc8e726a5d
[47:64] ^= 2f49e082094d4c37ba9c7da5d9f03e2fb4
```


## Order of the chain
The Index is the position in keys' array,
not the position in the chain.
The position in the chain is determine by the first 11 bytes of the input data.
Reading the above constrains carefully,
You can find that data[0:5] is only constrained by Index 0,
and only index 8 will modify it.

Now we assume 0 runs before 8,
so we know the first 5 bytes are `83 21 43 63 25`,
xor with our index key we extracted in the first section `83 23 42 69 23 b2 0e 28 97 df 14`.
And we got the first 5 indices, `0, 2, 1, 10, 6`.

Great! 0 is the first goroutine, so we know the first 19 bytes.
and the order is `0, 2, 1, 10, 6, 3, 8, 4, 7, 5, 9`

If you assume 8 runs before 0, you won't get a reasonable result.


## Flag
Now emulate the chain and recover the input,
If you feed it to the program, 
It will tell you `this not quite lead to the flag`,
which is the output when whole transformer chain success,
but the data hashChecker received doesn't has correct hash.

When I debug the program,
I found that the hashChecker receive
`DCTF{1545dbabe88f4e3fcb321e9bffe622e6fa56b5a44c3f165dc607fb87274ea514`.
The length of flag in this CTF is 70 bytes, so the last byte must be `}`.
