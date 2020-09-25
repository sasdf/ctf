---
name: metal
category: rev
points: 500
solves: 1
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}


## Time
20 hours


# Behavior
We got a C++ program that somehow encrypt the flag.
There are two files called "hw_x64.metal" and "metal_genx.isa".


# Solution
## TL;DR
1. Disassemble the cisa binary file to visa asm.
2. Cleanup the syntax.
3. Manually decompiled it to pseudo code.
4. Construct the eigenvector (i.e. key) from eigenvalues.


## Host Executable
The main executable "hw_x64.metal" is unstripped.
It won't be too hard to understand.

Searching for the library/strings on the Internet,
we can figure out that it is using Intel's C for Metal (i.e. GPGPU).
And here's a
[sample code](https://01.org/c-for-metal-development-package/blogs/huangli/2019/basic-host-programming)
that looks similar to our main executable.

The executable will load the flag and key,
encrypt it with the GPU kernel (`metal_genx.isa`),
and save the output from GPU to a file.

All encryption logics in the GPU kernel.

## Disassemble
To understand the GPU kernel,
we need to find the definition of its ISA.
We found [this file in intel-graphics-compiler](https://github.com/intel/intel-graphics-compiler/blob/master/visa/Common_ISA.cpp)
on GitHub.
There are
[documentations of ISA](https://github.com/intel/intel-graphics-compiler/blob/master/documentation/visa/index.md)
and a disassembler (!!!) in the same repo.

The repo is hard to compile. Luckily, we have pre-compiled version on Ubuntu 20.04.
Spin up a VM and run the following code will give us visa asm file.
```bash
# ubuntu 20.04
sudo apt-get install libigc-tools
GenX_IR metal_genx.isa -dumpcommonisa
```
Now, time for reversing :)

## Virtual ISA of Metal
The assembly code looks like:
```python
...
.decl V32 v_type=G type=uw num_elts=1 align=word
.decl V33 v_type=G type=d num_elts=1 align=dword
.decl V34 v_type=G type=df num_elts=64 align=GRF
.decl V35 v_type=G type=d num_elts=1 align=dword
...
.decl V297 v_type=G type=ud num_elts=1 align=dword alias=<V37, 0>
.decl V298 v_type=G type=w num_elts=2 align=dword alias=<V35, 0>
.decl V299 v_type=G type=w num_elts=2 align=dword alias=<V41, 0>
.decl V300 v_type=G type=uw num_elts=1 align=word alias=<V42, 0>
...
.function "encrypt_BB_0_1_0"

encrypt_BB_0_1_0:
    mov (M1, 1) V32(0,0)<1> V2(0,0)<0;1,0>                                       /// $1
    mov (M1, 1) V33(0,0)<1> V32(0,0)<0;1,0>                                      /// $2
    mov (M1, 8) V34(0,0)<1> 0x0:df                                               /// $3
    mov (M1, 1) V146(0,0)<1> V33(0,0)<0;1,0>                                     /// $4
    call (M1, 1) _Z13getDataMatrixIdEv15cm_surfaceindexiu2CMmr8x8_T__BB_1_2_1    /// $5
    mov (M1, 1) V35(0,0)<1> 0x0:d                                                /// $6
...
BB_5_6:
    mov (M1, 4) V50(0,0)<1> V6(0,0)<1;1,0>                                       /// $38
    add (M1, 1) V303(0,0)<1> V45(0,0)<0;1,0> (-)V50(0,0)<0;1,0>                  /// $39
    cmp.lt (M1, 1) P4 V51(0,0)<0;1,0> 0x0:b                                      /// $40
    (P4) jmp (M1, 1) BB_6_7                                                      /// $41
    mov (M1, 1) V52(0,0)<1> 0x8:w                                                /// $42
...
```

The syntax contains too much information, and too hard to read.
Take the first instruction as an example,
```
mov       (M1,      1       )
mnemonic  exec_mask exec_size

V32  (0,        0        ) <1>
dst  row_offset col_offset stride

V2   (0,        0        ) <0;             1,    0               >
src0 row_offset col_offset vertical_stride width horizontal_stride
```
The semantics of `mov` instruction is:
```c
for (i = 0; < exec_size; ++i) {
    if (ChEn[i]) {        // i.e. exec_mask
        dst[i] = src0[i]; // with type conversion
    }
}
```
A lot of the instruction in metal is SIMD operation.
It operates on multiple data with one instruction.

The exec_mask in this task is always `M1`, which means no masking.
So we can ignore the branch on `ChEn`.

All the variables in metal are arrays, and we have various way to access the values in these array.

The offsets in the parenthesis specified how many bytes we want to skip in front of the array.
The byte offset defined as:
```c
32 / sizeof(element) * row_offset + col_offset
```

In destination variable,
`stride` indicate how many elements we should skip to move to the next element.

Using python's syntax, it is:
```python
dst[offset::stride][:exec_size]
```

Source variable is more complicated.

After applying the byte offset, we reshape the remaining array as a matrix.
* `width` is the width of the matrix.
* `horizontal_stride` indicate how many elements we should skip to move to the next element in the same row.
* `vertical_stride` indicate how many elements we should skip to move to the next row.

And then we flatten the matrix back to a 1D array.
For example, `(M1, 8) V0<0, 2, 0>` means `[[V0[0]] * 2] * 4`.

Fortunately, there are only 7 kind of different indices in this task:
```
Scalar:               0;1,0
Pointer Array:        1,0
Row vector:           1;1,0
One column of Pairs:  2;1,0
arr[:]:               1
arr[::8]:             8
arr[::16]:            16
```

Most of the variables in this task is scalar,
we converted the syntax to numpy-like to make it more readable.
```python
.function "encrypt_BB_0_1_0"

encrypt_BB_0_1_0:
    mov<1>               V32:uw               thread_y:G          
    mov<1>               V33:d                V32:uw              
    mov<8>               V34[0:]:df           0x0:df              
    mov<1>               V146:d               V33:d               
    call<1>              _Z13getDataMatrixIdEv15cm_surfaceindexiu2CMmr8x8_T__BB_1_2_1
    mov<1>               V35:d                0x0:d               
    lifetime.start       V58                 
...
    mov<8>               V287[0:]:df          V58[0:]:df          
    mov<8>               V287[8:]:df          V58[8:]:df          
    mov<8>               V287[16:]:df         V58[16:]:df         
    mov<8>               V287[24:]:df         V58[24:]:df         
    mov<8>               V287[32:]:df         V58[32:]:df         
```

In the second part of variable definition, there are some variable aliases:
```python
.decl V37 v_type=G type=d num_elts=1 align=dword
.decl V35 v_type=G type=d num_elts=1 align=dword
.decl V297 v_type=G type=ud num_elts=1 align=dword alias=<V37, 0>
.decl V298 v_type=G type=w num_elts=2 align=dword alias=<V35, 0>
```
It is for type conversion, And we replace all those aliases with Go-like syntax.
```
    shr<1>               V38:ud               V37.(ud[1]):ud       0x4:ud              
```

Branches are implemented by conditional instructions:
```python
    cmp.eq (M1, 1) P8 V61(0,0)<0;1,0> 0x8:d                                      /// $83
    (!P8) jmp (M1, 1) BB_10_11                                                   /// $84
    ...
    cmp.gt (M1, 1) P39 V174(0,0)<0;1,0> V168(0,0)<0;1,0>                         /// $434
    (P39) sel (M1, 1) V69(0,0)<1> r[A43(0),0]<0;1,0>:d V69(0,0)<0;1,0>           /// $435
    (P39) sel (M1, 1) V70(0,0)<1> V169(0,0)<0;1,0> V70(0,0)<0;1,0>               /// $436
```

There are also pointer/address types in this language:
```python
    shl<1>               V42:w                V41.(w[2])[0]:w      0x3:w               
    addr_add<1>          A0[0:1]:A            &V39+0               V42.(uw[1]):uw      
    mov<1>               V43:df               A0[0][0]:uq         
```
This snippet is equivalent to `V43 = V39[V41]`.
Note that `addr_add` works on byte offset, so there are `shl 3` multiplying the element size. (V39 is unsigned qword array)

Full script can be found at [here]([_files/cleanup.py]).


## Decompile
With the simplified assembly,
we manually translate it into python-like pseudo code.
```python
     // v58 = [None] * 64
     lifetime.start       V58
 BB_2_3:
     // for v35 in range(0, 8):
         // v38 = thread_y * 32 + v35 * 4
         // v38p = thread_y * 64 + v35 * 8
         shl<1>               V36:d                V35:d                0x6:d
         mov<1>               V37:d                0x200:d
         mad<1>               V37:d                V32:uw               V37:d                V36:d
         shr<1>               V38:ud               V37.(ud[1]):ud       0x4:ud
         // v39 = inp_t6[v38p:v38p+8]
         oword_ld             (4)                  T6                   V38(0,0)<0;1,0>      V39.0
         // v40 = v35 * 8 * 8
         shl<1>               V40:w                V35.(w[2])[0]:w      0x6:w
         mov<1>               V41:d                0x0:d
 BB_3_4:
         // for v41 in range(0, 8):
             // v43 = v39[v41]
             shl<1>               V42:w                V41.(w[2])[0]:w      0x3:w
             addr_add<1>          A0[0:1]:A            &V39+0               V42.(uw[1]):uw
             mov<1>               V43:df               A0[0][0]:uq
```
This process might be simplified by some pattern matchings / symbolic engines,
but we doing it manually, taking about 12 hours...

In this ISA, there's no predefined register set, and no calling convention.
the argument and return value are implemented using global variable:
```python
// # V285 is the argument, and V286 is the return value.
// v67[v70] = func_v287_tri_argmax(v70)
mov<1>               V285:d               V70:d
call<1>              func_v287_tri_argmax
shl<1>               V126:w               V70.(w[2])[0]:w      0x2:w
addr_add<1>          A30[0:1]:A           &V67+0               V126.(uw[1]):uw
mov<1>               A30[0][0:]:d         V286:d
```
The variable can be found around the caller, and the free variables in the function.

Here is the [annotated asm]([_files/annotated.asm]) and its [translated pseudo code]([_files/pseudo.py])


## Algorithm
The last function is find the position of maximum element in column v285 in upper triangular part of v287 key matrix.

```python
# _Z16aAqwvgDTmHcpllEMIdEiu2CMmr8x8_T_i_BB_14_15_14:
def func_v287_tri_argmax(v285):
    # global v287
    v286 = v285 + 1
    if v285 < 6:
        for v289 in range(v285 + 2, 8):
            v292 = abs(v287[v285 * 8 + v289])
            v295 = abs(v287[v285 * 8 + v286])
            if v292 > v295:
                v286 = v289
    return v286
```
And the result is cached in v67.
```python
# After modified v287
v287[i66] = v287[i66] * v190 + v242

# We should update v67
a67v = v67[v239]
if a67v != v189:
    v248 = abs(v287[i66])
    v251 = abs(v287[v239 * 8 + a67v])
    if v248 > v251:
        continue
    v286 = v189
else:
    v286 = func_v287_tri_argmax(v239)
v67[v239] = v286
```
And this function is finding maximum element in upper triangle using v67 caches.
```python
# _Z16JPYgRtzJnMjnpuDbIdEvu2CMmr8x8_T_RiS2__BB_16_17_16:
def func2():
    # global v67, v287
    v69 = v67[0]

    v167 = abs(v287[v67[0]])
    v168 = v167
    v70 = 0
    for v169 in range(1, 7):

        v174 = abs(v287[v169 * 8 + v67[v169]])

        if v174 > v168:
            v69 = v67[v169]
            v70 = v169

        v168 = max(v174, v168)

    return v69, v70
```
The cache makes the code looks more complicated than it should be,
Actually, we can remove those parts and calculate full argmax without cache.

There are also some functions inlined in main function,
We move those function out to simplify main function.

Finally, we convert the it to runnable python code which can be found
[here]([_files/decompiled.py]).

The main function looks like:
```python
def encrypt(inp_key_t6, inp_data_t8):
    data_v34 = func_getDataMatrix(inp_data_t8, thread_y)

    assert inp_key_t6.dtype == np.uint64
    mat_org_v58 = inp_key_t6[thread_y * 64:][:64].astype(np.double).reshape(8, 8)
    mat_org_v58 *= 2.0**(-64)

    # set m[i,j] = m[j,i] or m[j,i] = m[i,j] according to tsc
    mat_org_v58 = maybe_to_random_symmetric(mat_org_v58)

    out_v66 = np.eye(8, dtype=np.double) # diagonal_mat8x8

    mat = mat_org_v58.copy()
    for _ in range(0x800):
        mc, mr = func_upper_tri_abs_argmax(mat)

        if too_small_cf_diag(mat, mr, mc):
            mat[mr,mc] = 0

        c3, c1, c2 = func_get_wtf_coeffs(mat, mr, mc)
        mat = func_mix_matrix(mat, mr, mc, c1, c2, c3)
        out_v66 = func_mix_row(out_v66, mr, mc, c1, c2)

    # get diagonal array, first 8 elements
    diag_elems_v87 = np.zeros(64)
    diag_elems_v87[:8] = np.diag(mat)[:8]

    # latter 8 * 7 = 56 elements
    for r in range(8):
        mat = remove_col_and_row(mat_org_v58, r)

        for _ in range(0x800):
            mc, mr = func_upper_tri_abs_argmax(mat)

            # whether adding m[mr,mc] to m[mr,mr] and m[mc,mc] won't change its value
            # (i.e. m[r,c] + m[r,r] == m[r,r] and m[r,c] + m[c,c] == m[c,c])
            if too_small_cf_diag(mat, mr, mc):
                mat[mr,mc] = 0

            c3, c1, c2 = func_get_wtf_coeffs(mat, mr, mc)
            mat = func_mix_matrix(mat, mr, mc, c1, c2, c3)

        diag_elems_v87[r * 7 + 8:][:7] = np.diag(mat)[:7]

    out_v66 = data_v34 * np.abs(out_v66)

    return diag_elems_v87.tobytes() + out_v66.tobytes()
```

The function will do the following things:
1. Reshape the key to a 8x8 matrix
2. Shrink its value range to [0, 1].
3. Generate two matrix `mat` and `out_v66` from the key.
4. `out_v66` is the key for encrypting flag.
5. We also got diagonal of the `mat` and 8 sub matrixes.


I was trying to understand wtf is those mix functions first, but failed.

Then I increased 0x800 to 0x1000.
Found that the result has already converged and didn't change.
It looks like some numerical method, but it didn't help.

Last, I print out the `mat` and `out_v66`.
The `mat` is almost a diagonal matrix, and `out_v66` is something looks random.

The previous CTF I played is p4ctf, and they have some challenges about diagonalization.
It makes me tried the equation:
```python
out_v66.T @ np.diag(np.diag(mat)) @ out_v66 ~= mat_org_v58
```

Bingo! The loop is calculating SVD.

It means we have several eigenvalues and we need to found its eigenvectors.

There was a paper quite famous in last year called
[Eigenvectors from Eigenvalues](https://arxiv.org/abs/1908.03795).
And the only equation we need is in its abstract.

For numerical stability, I calculate it in log domain.
Also don't forget to use `round` instead of `floor`.

[Here]([_files/solve.py]) is the decryption script.
