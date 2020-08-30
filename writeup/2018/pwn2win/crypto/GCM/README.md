---
name: GCM
category: crypto
points: 373
solves: 8
---

{% ignore %}
[Go to rendered GitBook version](https://sasdf.github.io/ctf/)
{% endignore %}

> There is only one method of performing bank transactions that can not be monitored by The Bavarian.
> It's not an ATM, but a secret system.


## Time
3 hours

# Behavior
```
.. nc 200.136.252.51 5555

Welcome to Tr4nsferw1s3! Please chose one of the options:
  [1] Login
  [2] Transfer/pay
  [3] Exit
1
Username: abc
Password: abc
Logged in as abc! Here is the token:
{'enc': '05a32e329fc834fad58ef89102b5d74ceed1a935bf36df445ce17f09f56794ce2b51cb4d8c2f9794e29e52bcf0c3df4c67fbade8b0fcfebc145d369922d7b9835c270d66305c178fac95e8d2c801fe07b9767eea89aa14b6de72c55351', 'tag': '0116edb64e4a66fcf2bc2e722e59a610', 'iv': '3928aba0f3629befcb300671'}

Welcome to Tr4nsferw1s3! Please chose one of the options:
  [1] Login
  [2] Transfer/pay
  [3] Exit
2
Token: {'enc': '05a32e329fc834fad58ef89102b5d74ceed1a935bf36df445ce17f09f56794ce2b51cb4d8c2f9794e29e52bcf0c3df4c67fbade8b0fcfebc145d369922d7b9835c270d66305c178fac95e8d2c801fe07b9767eea89aa14b6de72c55351', 'tag': '0116edb64e4a66fcf2bc2e722e59a610', 'iv': '3928aba0f3629befcb300671'}
Huh? you have no money and want the flag? -.-
```

# Solution
## TL;DR
1. Patch the token
2. Try all 256 truncated one byte tag

The service encrypts the token with AES-GCM mode,
iv is generated from urandom.
It seems no vulnerbilities inside the crypto parts.

Our input is parsed with `ast.literal_eval`,
which means we can send strange type in the payload.
After I stucked on finding vulns of GCM mode,
I started poking the service with strange payload.

## Strange Behavior
I tried to put something data type in tag or iv.
It crashed the program but nothing intersting happened.

However, when I put empty string (or array/dict...) in tag:
```
.. nc 200.136.252.51 5555

Welcome to Tr4nsferw1s3! Please chose one of the options:
  [1] Login
  [2] Transfer/pay
  [3] Exit
1
Username: abc
Password: abc
Logged in as abc! Here is the token:
{'enc': 'b31af0e48908c0d7850ad7803745909a3b3c95a7457c605860809eb0db9a1e52a53f195a9c99d88566a591f580d472cad64759ac8fc89af09b48f56dad36c55dd0b9f0bbb30ab2b64d3f11abca04bac635c2d3b37c2012b902b688aa63', 'tag': 'e7fe3cad3a227bee1a658ca4100bab86', 'iv': 'cc6a230be51e9faf8ae35abc'}

Welcome to Tr4nsferw1s3! Please chose one of the options:
  [1] Login
  [2] Transfer/pay
  [3] Exit
2
Token: {'enc': 'b31af0e48908c0d7850ad7803745909a3b3c95a7457c605860809eb0db9a1e52a53f195a9c99d88566a591f580d472cad64759ac8fc89af09b48f56dad36c55dd0b9f0bbb30ab2b64d3f11abca04bac635c2d3b37c2012b902b688aa63', 'tag': '', 'iv': 'cc6a230be51e9faf8ae35abc'}
Traceback (most recent call last):
  File "/home/gcm/chall.py", line 79, in <module>
    menu()
  File "/home/gcm/chall.py", line 71, in menu
    pay()
  File "/home/gcm/chall.py", line 53, in pay
    account = ast.literal_eval(decryptor.update(enc) + decryptor.finalize_with_tag(tag))
  File "/usr/local/lib/python2.7/dist-packages/cryptography/hazmat/primitives/ciphers/base.py", line 206, in finalize_with_tag
    data = self._ctx.finalize_with_tag(tag)
  File "/usr/local/lib/python2.7/dist-packages/cryptography/hazmat/backends/openssl/ciphers.py", line 209, in finalize_with_tag
    self._backend.openssl_assert(res != 0)
  File "/usr/local/lib/python2.7/dist-packages/cryptography/hazmat/backends/openssl/backend.py", line 105, in openssl_assert
    return binding._openssl_assert(self._lib, ok)
  File "/usr/local/lib/python2.7/dist-packages/cryptography/hazmat/bindings/openssl/binding.py", line 76, in _openssl_assert
    errors_with_text
cryptography.exceptions.InternalError: Unknown OpenSSL error. This error is commonly encountered when another library is not cleaning up the OpenSSL error stack. If you are using cryptography with another library that uses OpenSSL try disabling it before reporting a bug. Otherwise please file an issue at https://github.com/pyca/cryptography/issues with information on how to reproduce this. ([])

```

And here's the output of my local python:
```
In [99]: dec.finalize_with_tag(b'')
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-99-1ad91645a4ee> in <module>()
----> 1 dec.finalize_with_tag(b'')

/usr/local/lib/python3.7/site-packages/cryptography/hazmat/primitives/ciphers/base.py in finalize_with_tag(self, tag)
    204         if self._ctx is None:
    205             raise AlreadyFinalized("Context was already finalized.")
--> 206         data = self._ctx.finalize_with_tag(tag)
    207         self._tag = self._ctx.tag
    208         self._ctx = None

/usr/local/lib/python3.7/site-packages/cryptography/hazmat/backends/openssl/ciphers.py in finalize_with_tag(self, tag)
    203             raise ValueError(
    204                 "Authentication tag must be {0} bytes or longer.".format(
--> 205                     self._mode._min_tag_length)
    206             )
    207         res = self._backend._lib.EVP_CIPHER_CTX_ctrl(

ValueError: Authentication tag must be 16 bytes or longer.
```

Hmm... the errors are not the same, what's going wrong?

I searched for the
[source](https://github.com/pyca/cryptography/blob/master/src/cryptography/hazmat/backends/openssl/ciphers.py#L202)
in github, and it's same as my local version.
It checks the length of tag first.

Then I try to find when this check is added.
It was added in the
[commit d4378e](https://github.com/pyca/cryptography/commit/d4378e42937b56f473ddade2667f919ce32208cb#diff-7f9182acb7dedf7b702ac6c6b98fd678)
, which is about tag truncation.
It says:
> * **SECURITY ISSUE:**
> :meth:`~cryptography.hazmat.primitives.ciphers.AEADDecryptionContext.finalize_with_tag`
> allowed tag truncation by default which can allow tag forgery in some cases.
> The method now enforces the ``min_tag_length`` provided to the
> :class:`~cryptography.hazmat.primitives.ciphers.modes.GCM` constructor.

Ah Ha!! We found the vulnerbilities.


Now, change `"admin": "N"` to `"admin": "Y"` by XOR,
and then try all 256 one byte tag to get the flag.
([Script]([_files/solve.py]))
