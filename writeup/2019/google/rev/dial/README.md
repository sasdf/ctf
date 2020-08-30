---
name: Dialtone
category: rev
points: 189
solves: 56
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> You might need a pitch-perfect voice to solve this one.
> Once you crack the code, the flag is CTF{code}.


## Time
40 minutes  


# Behavior

It's a ELF executable that will record some voice using your microphone,
and then tell you whether you pass the test.


# Solution
## TL;DR
1. Reverse the executable
2. Extract the sequence from switch case.
3. Convert to value using a DTMF keypad table.

## Reversing

Here's its main function:

```c

//...

mic = pa_simple_new(0LL, *argv, 2LL, 0LL, "record", &ss_3811, 0LL, 0LL, &err);
if ( mic ) {
    v8 = 0;
    v9 = 0;
    v10 = 0;
    do {
        if ( (signed int)pa_simple_read(mic, &buf, 0x8000LL, &err) < 0 ) {
            errStr = pa_strerror(err);
            fprintf(stderr, "pa_simple_read() failed: %s\n", errStr);
            return 1;
        }
        x(&buf, &v7);
        good = r(&v8, &v7);
        if ( good < 0 ) {
            fwrite("FAILED\n", 1uLL, 7uLL, stderr);
            return 1;
        }
    } while ( good );
    fwrite("SUCCESS\n", 1uLL, 8uLL, stderr);
    pa_simple_free(mic, 1LL);
    result = 0;
} else {
    v3 = pa_strerror(err);
    fprintf(stderr, "pa_simple_new() failed: %s\n", v3);
    result = 1;
}
return result;
```

And the library function's prototype found from
[here](https://freedesktop.org/software/pulseaudio/doxygen/simple_8h.html).

```c
pa_simple * pa_simple_new (
    const char *server, const char *name, pa_stream_direction_t dir,
    const char *dev, const char *stream_name, const pa_sample_spec *ss,
    const pa_channel_map *map, const pa_buffer_attr *attr, int *error);
int pa_simple_read (pa_simple *s, void *data, size_t bytes, int *error);
```

It use PulseAudio to record some audio, and run some test.

Here's how `x` looks like:

```c
void x(__int64 buf, __int64 output) {
    int step;

    bit_flip(buf, output);
    for ( int i = 1; i < 14; ++i ) {
        step = 1 << i;
        for ( int j = 0; j < 0x2000; j += step )
            y(output, j, step);
    }
}
```

It's still not clear what is will do.
Let's look into `bit_flip`.

```c
void __fastcall bit_flip(__int64 buf, __int64 output) {
    double v2; // ST00_8
    signed __int64 v3; // rax
    int i; // [rsp+24h] [rbp-4h]

    for ( i = 0; i <= 0x1FFF; ++i ) {
        v2 = *(4LL * i + buf);
        v3 = 16LL * reverse_bits(i) + output;
        *v3 = v2;
        *(v3 + 8) = 0LL;
    }
}
```

It tells us that `buf` is a float32 array,
and `output` is a double array.

Let's change its type:

```c
void bit_flip(float *buf, double *output) {
    double v2; // ST00_8
    double *v3; // rax
    int i; // [rsp+24h] [rbp-4h]

    for ( i = 0; i <= 0x1FFF; ++i ) {
        v2 = buf[i];
        v3 = &output[2 * reverse_bits(i)];
        *v3 = v2;
        v3[1] = 0.0;
    }
}
```

OK, it converts the float32 input into double array,
and insert a zero between each elements.

Let's look at `y`:

```c
__int64 __fastcall y(double *output, __int64 a2, int a3) {
    // ...
    for ( i = 0; ; ++i ) {
        // ...
        cexp(output, a2);
        // ...
        complex_mul(output);
        // ...
        complex_add(output);
        // ...
        complex_sub(output);
        // ...
    }
    return result;
}
```

It looks like that the output is a double complex array instead of a double array.
To change the type to double complex in IDA, we have to create a structure first:

```
00000000 Complex         struc ; (sizeof=0x10, mappedto_13)
00000000 real            dq ?
00000008 imag            dq ?
00000010 Complex         ends
```

Now, we can change their types. Remember to fix those signature of library functions.

```c
void bit_flip(float *sample, Complex *output) {
  double inp_i; // ST00_8
  Complex *out_i; // rax
  signed int i; // [rsp+24h] [rbp-4h]

  for ( i = 0; i <= 0x1FFF; ++i ) {
    inp_i = sample[i];
    out_i = &output[reverse_bits(i)];
    out_i->real = inp_i;
    out_i->imag = 0.0;
  }
}

void y(Complex *A, signed int k, __int64 step) {
  Complex w; // kr00_16
  Complex u; // ST30_16
  Complex t; // kr10_16
  signed int m; // [rsp+10h] [rbp-60h]
  int j; // [rsp+5Ch] [rbp-14h]

  m = step;
  for ( j = 0; j < m / 2; ++j ) {
    w = cexp(__PAIR__(j * -6.283185307179586477 / m, (-0.0 * j / m)));
    u = A[k + j];
    t = complex_mul(w, A[j + k + m / 2]);
    A[k + j] = complex_add(u, t);
    A[j + k + m / 2] = complex_sub(u, t);
  }
}
```

It looks like a radix-2 FFT, Here's the pseudo code from 
[wikipedia](https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm#Data_reordering,_bit_reversal,_and_in-place_algorithms).
You can compare it with our reversed code.

```
algorithm iterative-fft is
    input: Array a of n complex values where n is a power of 2
    output: Array A the DFT of a

    bit-reverse-copy(a,A)
    n ← a.length 
    for s = 1 to log(n)
        m ← 2s
        ωm ← exp(−2πi/m) 
        for k = 0 to n-1 by m
            ω ← 1
            for j = 0 to m/2 – 1
                t ← ω A[k + j + m/2]
                u ← A[k + j]
                A[k + j] ← u + t
                A[k + j + m/2] ← u – t
                ω ← ω ωm
   
    return A
```

Back to our main function. Now, it looks like:

```c
do {
    if ( pa_simple_read(mic, sample, 0x8000LL, &err) < 0 ) {
        // raise error
    }
    FFT(sample, freq);
    good = r(&state, freq, v3);
    if ( good < 0 ) {
        fwrite("FAILED\n", 1uLL, 7uLL, stderr);
        return 1;
    }
}
while ( good );
fwrite("SUCCESS\n", 1uLL, 8uLL, stderr);
```

And here's how `r` check our sound:

```c
int run(State *state, Complex *freq, double a3) {
    double f2[4]; // [rsp+10h] [rbp-70h]
    double f1[4]; // [rsp+30h] [rbp-50h]
    int num; // [rsp+54h] [rbp-2Ch]
    bool ok; // [rsp+5Bh] [rbp-25h]
    int j; // [rsp+5Ch] [rbp-24h]
    double max_f2; // [rsp+60h] [rbp-20h]
    int argmax_f2; // [rsp+68h] [rbp-18h]
    int i; // [rsp+6Ch] [rbp-14h]
    double max_f1; // [rsp+70h] [rbp-10h]
    int argmax_f1; // [rsp+7Ch] [rbp-4h]

    if ( ++state->retry > 20 )
        return 0xFFFFFFFFLL;
    f1[0] = f(freq, 1209);
    f1[1] = f(freq, 1336);
    f1[2] = f(freq, 1477);
    f1[3] = f(freq, 1633);
    argmax_f1 = -1;
    max_f1 = 1.0;
    for ( i = 0; i <= 3; ++i ) {
        if ( f1[i] > max_f1 ) {
            argmax_f1 = i;
            max_f1 = f1[i];
        }
    }
    f2[0] = f(freq, 697);
    f2[1] = f(freq, 770);
    f2[2] = f(freq, 852);
    f2[3] = f(freq, 941);
    argmax_f2 = -1;
    max_f2 = 1.0;
    for ( j = 0; j <= 3; ++j ) {
        if ( f2[j] > max_f2 ) {
            argmax_f2 = j;
            max_f2 = f2[j];
        }
    }
    if ( state->need_blank ) {
        if ( argmax_f1 < 0 && argmax_f2 < 0 ) {
            state->need_blank = 0;
            state->retry = 0;
        }
    } else if ( argmax_f1 >= 0 && argmax_f2 >= 0 ) {
        num = argmax_f1 | 4 * argmax_f2;
        ok = 0;
        switch ( state->idx ) {
            case 0u:
                ok = num == 9;
                goto LABEL_30;
            case 1u:
                ok = num == 5;
                goto LABEL_30;
            case 2u:
                ok = num == 10;
                goto LABEL_30;
            case 3u:
                ok = num == 6;
                goto LABEL_30;
            case 4u:
                ok = num == 9;
                goto LABEL_30;
            case 5u:
                ok = num == 8;
                goto LABEL_30;
            case 6u:
                ok = num == 1;
                goto LABEL_30;
            case 7u:
                ok = num == 13;
                goto LABEL_30;
            case 8u:
                if ( num )
                    goto LABEL_30;
                return 0LL;
            default:
LABEL_30:
                if ( ok != 1 )
                    return 0xFFFFFFFFLL;
                ++state->idx;
                state->retry = 0;
                state->need_blank = 1;
                break;
        }
    }
    return 1LL;
}
```

where `f` returns the amplitude of that frequency:

```c
double f(Complex *freq, int v) {
  return cabs(freq[(v << 13) / 44100]);
}
```

The goal is clear now,
we have to input an audio that will be converted to `9, 5, 10, 6, 9, 8, 1, 13, 0`.

Googling with the challange name `dialtone` and those frequency constant,
we can find a [frequency to keypad table from wikipedia](https://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling#Keypad).
This is the sound you'll hear while dialing:

|      | 1209Hz | 1336Hz | 1477Hz | 1633Hz |
|----- | ------ | ------ | ------ | ------ |
|697Hz | 1      | 2      | 3      | A      |
|770Hz | 4      | 5      | 6      | B      |
|852Hz | 7      | 8      | 9      | C      |
|941Hz | *      | 0      | #      | D      |

convert the index to those character, we get `CTF{859687201}`.
