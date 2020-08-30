---
name: Quantum Pyramids
category: crypto
points: 373
solves: 9
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> A super efficient post-quantum signature scheme has been deployed. Can you forge a signature?


## Time
5 hours


# Behavior
The attatchment is a zip of [sphincsplus](https://github.com/sphincs/sphincsplus) repo.

> You are given access to a service, which allow you to obtain digital signatures for messages of your choice.
> The service uses SPHINCS+ with a custom set of highly efficient parameters,
> not even a quantum computer will help you to break it.
>
> Your goal is to produce a valid signature for the message opensesame and send it to the /verify endpoint in order to get access to the secret flag.


# Solution
## TL;DR
1. Collect some signatures until all secrets are revealed
2. Hook on the code of sphincs+ to build the full hash tree
3. Generate the signature with the hash tree


## Settings
```
$ git status
On branch master
Your branch is behind 'origin/master' by 47 commits, and can be fast-forwarded.
  (use "git pull" to update your local branch)

Revert currently in progress.
  (run "git revert --continue" to continue)
  (use "git revert --skip" to skip this patch)
  (use "git revert --abort" to cancel the revert operation)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        new file:   ref/params/params-sphincs-haraka-ctf2020.h

no changes added to commit (use "git add" and/or "git commit -a")
```

And the only changes is:
```diff
$ diff ref/params/params-sphincs-haraka-ctf2020.h ref/params/params-sphincs-haraka-128f.h
5c5
< #define SPX_N 8
---
> #define SPX_N 16
7c7
< #define SPX_FULL_HEIGHT 4
---
> #define SPX_FULL_HEIGHT 60
9c9
< #define SPX_D 2
---
> #define SPX_D 20
11,12c11,12
< #define SPX_FORS_HEIGHT 6
< #define SPX_FORS_TREES 17
---
> #define SPX_FORS_HEIGHT 9
> #define SPX_FORS_TREES 30
```

Looks like they decrease the parameters a lot.

So, what is SPHINCS+ ?


## SPHINCS+ and hash-based signatures
> SPHINCS+ is a stateless hash-based signature scheme,
> which was submitted to the NIST post-quantum crypto project.
> The design advances the SPHINCS signature scheme,
> which was presented at EUROCRYPT 2015.
> It incorporates multiple improvements,
> specifically aimed at reducing signature size. 

Basically, sphincs+ is a combination of many hash-based signature techniques to make it usable.

Hash-based signature is based on the assumption that given `H(x)`, it is hard to find `x`.
The spirit is simple, use secret inputs as signature, and their hash is public key.
All variants are just about the way of generating secret and the way of hashing.

For example, The simplest scheme (Lamport signature) for signing one bit looks like this:
1. Generate two secret strings A, B as secret key
2. Publish H(A), H(B) as public key
3. If we are signing 0, the signature is A, otherwise B.

Clearly, the secret can be used only once.
After publish A, we should make sure that B should never become public.

In practice, we usually use hash tree (e.g. Merkle-tree) or hash chain (e.g. Winternitz ots).
These details is not necessary for solving this challenge,
but it is more easily to understand it with these knowledge.
You could find some great explanation in these posts:
    * https://sphincs.cr.yp.to/slides-sphincs-20150421.pdf
    * https://huelsing.net/wordpress/wp-content/uploads/2016/02/20160223_pq_winter_school.pdf
    * https://huelsing.net/wordpress/?p=558

In sphincs, they eliminate the state by using a hypertree which has a lot of leaves (i.e. secret inputs).
We don't need to remember which secret is already used, the probability of reusing is just small enough to be ignored.


## Solving the challenge
BUT, notice that we have a special sphincs+ instances with a lot of parameters become very small.

I pulled about 10000 signatures from the server, and here's the count of unique values in each qwords:
```
idx: #uniq -     example      x cnt  
  0: 12772 - 2d853651495084b4 x 1    // Random key for hashing
  1:  1024 - 7e7585c57531d678 x 25   // FORS-1
  2:  1024 - 8d26227f72cc914b x 25   // FORS-1
  3:   512 - 27da1a6c634238c6 x 38   // FORS-1
  4:   256 - d32e9ea01783a3cc x 70   // FORS-1
  5:   128 - b39121da965bef8f x 125  // FORS-1
  6:    64 - 3d02b49eda59a150 x 235  // FORS-1
  7:    32 - fd9d015ab65900fd x 435  // FORS-1
  8:  1024 - bd1bd911f2f39cec x 26   // FORS-2
  9:  1024 - fa6ac0752e9cb731 x 26   // FORS-2
 10:   512 - 34e6bd54a770b469 x 42   // FORS-2
 11:   256 - 82651ba74dd9455c x 69   // FORS-2
 12:   128 - 158c3d25a24a02b8 x 128  // FORS-2
 13:    64 - 1a4ad7f8f0783719 x 232  // FORS-2
 14:    32 - 562329eccec33799 x 457  // FORS-2
 15:  1024 - d2b61dbb2daf5b49 x 23   // FORS-3
 16:  1024 - ac4b54d0c48276cc x 23   // FORS-3
 17:   512 - 683875de63b890a4 x 39   // FORS-3
 18:   256 - ddd93bcfd720b3a2 x 70   // FORS-3
 19:   128 - a041760993c0a32c x 124  // FORS-3
 20:    64 - 6462557963caaae8 x 228  // FORS-3
 21:    32 - 838ed3cfd29c542c x 434  // FORS-3
 22:  1024 - b41cf9a4c9ebcaec x 25   // FORS-4
 23:  1024 - 4895b0e833dcb3ba x 25   // FORS-4
 24:   512 - e460e9e2822c9a8b x 42   // FORS-4
 25:   256 - b0e3c052ec4b4733 x 72   // FORS-4
 26:   128 - 43e04ee4a70e017f x 124  // FORS-4
 27:    64 - 733a7c1469b550fa x 231  // FORS-4
 28:    32 - c24c722efa5a5b7f x 440  // FORS-4
 29:  1024 - 53916bedb9969899 x 25   // FORS-5
 30:  1024 - 349cd77029ce6c93 x 25   // FORS-5
 31:   512 - ad533a08f172b061 x 40   // FORS-5
 32:   256 - 1b1236e10ff354cb x 79   // FORS-5
 33:   128 - 7330eddf964c65c4 x 124  // FORS-5
 34:    64 - fad3f1375b44d129 x 233  // FORS-5
 35:    32 - 894f09dda8d41c83 x 438  // FORS-5
 36:  1024 - 257b3682f83700f0 x 26   // FORS-6
 37:  1024 - a5f83e3cc73082a6 x 26   // FORS-6
 38:   512 - 9603a086b9a56b2d x 41   // FORS-6
 39:   256 - 12d334597803b5fd x 74   // FORS-6
 40:   128 - d0419c4dd6c10f6d x 129  // FORS-6
 41:    64 - ae593d7d358363bd x 230  // FORS-6
 42:    32 - b9ef4c2308ddc235 x 433  // FORS-6
 43:  1024 - 2b0c4b6d49f3f071 x 27   // FORS-7
 44:  1024 - 7cc0ba2a1c2f7cae x 27   // FORS-7
 45:   512 - d03c25e0c4866988 x 46   // FORS-7
 46:   256 - 013a79d19bd341af x 76   // FORS-7
 47:   128 - ac2ea4824895c00c x 124  // FORS-7
 48:    64 - e232f877dee34d4f x 234  // FORS-7
 49:    32 - e838684115a2fdfd x 441  // FORS-7
 50:  1024 - a350886647d2bb7a x 24   // FORS-8
 51:  1024 - c5403169c0cedc57 x 24   // FORS-8
 52:   512 - 600ee241c95d86b8 x 38   // FORS-8
 53:   256 - 10fb53e0c5712372 x 68   // FORS-8
 54:   128 - 153a01c7da1eaed2 x 127  // FORS-8
 55:    64 - 71a59e74ee59ca96 x 225  // FORS-8
 56:    32 - a0bb0637bb628d0c x 437  // FORS-8
 57:  1024 - 9c955e74d15a9271 x 25   // FORS-9
 58:  1024 - 0cf47ef4802ff20c x 25   // FORS-9
 59:   512 - 639c4fea77c4ae08 x 45   // FORS-9
 60:   256 - 974947da86e06764 x 75   // FORS-9
 61:   128 - 395d3254b13300dd x 129  // FORS-9
 62:    64 - 1bb1e78fd6c745ab x 234  // FORS-9
 63:    32 - d28daa26b8f93d31 x 440  // FORS-9
 64:  1024 - c3d33b90ed3f4261 x 26   // FORS-10
 65:  1024 - c5d588fdd7ac241f x 26   // FORS-10
 66:   512 - 9f02a614c0333125 x 41   // FORS-10
 67:   256 - 52dd9ce0f515048c x 70   // FORS-10
 68:   128 - 3bea14cedfdbc377 x 136  // FORS-10
 69:    64 - c9cc2741e503dfe7 x 236  // FORS-10
 70:    32 - fa20723c1213f64d x 435  // FORS-10
 71:  1024 - 5a3fc193020948b2 x 25   // FORS-11
 72:  1024 - 11793b3477d2ba55 x 25   // FORS-11
 73:   512 - 6892969e91673ff6 x 40   // FORS-11
 74:   256 - 5d00330cc3277fba x 68   // FORS-11
 75:   128 - 2fde22ff6c903077 x 120  // FORS-11
 76:    64 - 53ec8779630ed300 x 227  // FORS-11
 77:    32 - 18c651049b988ebf x 454  // FORS-11
 78:  1024 - 4b997ebe9b956450 x 28   // FORS-12
 79:  1024 - 2585e0b777a2a027 x 28   // FORS-12
 80:   512 - 4ad993d5e0e9f289 x 40   // FORS-12
 81:   256 - a62796d7dac335d7 x 68   // FORS-12
 82:   128 - 1ebd59935972274c x 121  // FORS-12
 83:    64 - 1972d2a5eeedfca8 x 226  // FORS-12
 84:    32 - 3430a3f87ba5e2d1 x 435  // FORS-12
 85:  1024 - 23c4b9b48a5ea619 x 26   // FORS-13
 86:  1024 - 002623cb166d2f1a x 26   // FORS-13
 87:   512 - 591f8901a2500fda x 41   // FORS-13
 88:   256 - 7407d7a8b256c529 x 75   // FORS-13
 89:   128 - 92f805c6ec356348 x 125  // FORS-13
 90:    64 - 5a3b424062ece24b x 234  // FORS-13
 91:    32 - 8618a525eaafc6db x 439  // FORS-13
 92:  1024 - 0f662b03f2438cb0 x 24   // FORS-14
 93:  1024 - d9aef0dc2dc86728 x 24   // FORS-14
 94:   512 - e428f650d73dd171 x 42   // FORS-14
 95:   256 - 8a1802b636d97ee8 x 69   // FORS-14
 96:   128 - d896d78fa3b95b9c x 120  // FORS-14
 97:    64 - 66c3cf4775adc63c x 224  // FORS-14
 98:    32 - 25f9002bb6d74238 x 435  // FORS-14
 99:  1024 - 3897ad41884aff94 x 26   // FORS-15
100:  1024 - e9e909bbb895b49f x 26   // FORS-15
101:   512 - f11525c63d283d2d x 40   // FORS-15
102:   256 - 623c548f2d645896 x 73   // FORS-15
103:   128 - 1da0c2f11cf8c06c x 132  // FORS-15
104:    64 - 61bfe0c1e2a3df2f x 243  // FORS-15
105:    32 - e34b71c327b8dee3 x 441  // FORS-15
106:  1024 - b54d4040ef827aa5 x 26   // FORS-16
107:  1024 - 47492b0be2b69e67 x 26   // FORS-16
108:   512 - ef1693f20cf1f9f2 x 41   // FORS-16
109:   256 - 21a8c6feb971ebe4 x 71   // FORS-16
110:   128 - 55add77a56e283db x 131  // FORS-16
111:    64 - 4b0490eccab5003f x 240  // FORS-16
112:    32 - f59b4c9c8941830e x 433  // FORS-16
113:  1024 - af0c87dd0c99950c x 26   // FORS-17
114:  1024 - eac4c09b747aa013 x 26   // FORS-17
115:   512 - 67491f7392c76f73 x 41   // FORS-17
116:   256 - 2456c78dfa9402cf x 67   // FORS-17
117:   128 - 8d83a6fb5c98660b x 125  // FORS-17
118:    64 - 5f526edfb152bd09 x 225  // FORS-17
119:    32 - cc41df0e98c5c10f x 439  // FORS-17
120:    16 - 4d4acc3d1bb16e12 x 848  // WOTS
121:    16 - af97fbb0bce0cc32 x 848  // WOTS
122:    16 - 98e275e0d71c2777 x 848  // WOTS
123:    16 - 4fae664d1da13c70 x 848  // WOTS
124:    16 - 854bbecfb2064401 x 848  // WOTS
125:    16 - 6888ddf833bfe1e6 x 848  // WOTS
126:    16 - 054448ff9847ba1a x 848  // WOTS
127:    16 - b40a539f735444c2 x 848  // WOTS
128:    16 - dab57309507067a1 x 848  // WOTS
129:    16 - 82dbd184da82f3b6 x 848  // WOTS
130:    16 - f560dad64a766d6a x 848  // WOTS
131:    16 - 198d0d2b2659fc21 x 848  // WOTS
132:    16 - a59b0c82d444e2b3 x 848  // WOTS
133:    16 - 818e7d699419a31b x 848  // WOTS
134:    16 - cb88ef1012d68c53 x 848  // WOTS
135:    16 - c54d7c011dbc7dbd x 848  // WOTS
136:    16 - b569183e57239212 x 848  // WOTS
137:    16 - f438b1646efeba9e x 848  // WOTS
138:    16 - 7f9f2e96415b8fd0 x 848  // WOTS
139:     8 - 93dc80152c4b61bc x 1635 // WOTS
140:     4 - 3c5d48449c59b17f x 3229 // WOTS
141:     4 - 11935c93beccf89b x 3229 // WOTS
142:     4 - 6d02255e5fcdd972 x 3229 // WOTS
143:     4 - 736ff7d507243dc5 x 3229 // WOTS
144:     4 - b4de6e12321633bd x 3229 // WOTS
145:     4 - 2a6d7a360178a468 x 3229 // WOTS
146:     4 - 5625ce003a25875b x 3229 // WOTS
147:     4 - 234e0dedd8bf9a33 x 3229 // WOTS
148:     4 - 4fee4659cbc577ea x 3229 // WOTS
149:     4 - 1921f20b6e42ceb4 x 3229 // WOTS
150:     4 - c80af1fe32aea76d x 3229 // WOTS
151:     4 - 998dd80f2e0bf988 x 3229 // WOTS
152:     4 - f0e710e45429ae01 x 3229 // WOTS
153:     4 - 8930607dc9dc4058 x 3229 // WOTS
154:     4 - 2e346cb18267065f x 3229 // WOTS
155:     4 - dd68f2b3f7b30cc3 x 3229 // WOTS
156:     4 - 1b35da4cb4e89fc8 x 3229 // WOTS
157:     4 - 65706e33de120c8f x 3229 // WOTS
158:     4 - d9c3456528632d02 x 3229 // Merkle tree
159:     2 - 624299f44512271e x 6430 // Merkle tree
```

Great! It looks like that we have all the secret values.

Now, the problem is which value should we use for the signature given a input message.

The sphincs scheme is quite complex with a lot of details for building the tree,
I'm pretty sure I'll messup all the things if I implemented by myself at 4 am.
So I decide to modify the code of signature verification instead.
I modify all the places that will access the value of signature,
and save the value to a table.
Fortunately, the implementation in sphincsplus use a universal address for trees:
```c
for (i = 0; i < SPX_FORS_TREES; i++) {
    idx_offset = i * (1 << SPX_FORS_HEIGHT);

    set_tree_height(fors_tree_addr, 0);
    set_tree_index(fors_tree_addr, indices[i] + idx_offset);

    // My hook for saving/loading signatures to/from the database
    load_addr(sig, fors_tree_addr);

    /* Derive the leaf from the included secret key part. */
    fors_sk_to_leaf(leaf, sig, pub_seed, fors_tree_addr);
    sig += SPX_N;

    /* Derive the corresponding root node of this tree. */
    compute_root(roots + i*SPX_N, leaf, indices[i], idx_offset,
                 sig, SPX_FORS_HEIGHT, pub_seed, fors_tree_addr);
    sig += SPX_N * SPX_FORS_HEIGHT;
}
```
`sig` in a pointer to signature, and we can use `fors_tree_addr` as the index to save/load the values.

After hooking on all those signature accessing code,
we're able to build the table by running "verification" function on all signatures we collected.
And we can build the signature with "verification" function too.
You can found those patched files at [here]([_files/patches/]).
