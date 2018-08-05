import sys
import random
from encryption import encrypt


#-- Create 512-bits key, extremely strong :) --#
mapping = list(range(32, 96))
random.shuffle(mapping)
print(f'key: {mapping}')

#-- Encrypt secret document --#
"""
The document contains several human readable
paragraphs from wikipedia and a flag you want.
"""
with open(sys.argv[1], 'r') as f:
    plaintext = f.read().encode('ascii')
ciphertext = encrypt(plaintext, mapping)

#-- Sanity check --#
rev = {e-32: i+32 for i, e in enumerate(mapping)}
rev = [rev[i] for i in range(64)]
decrypted = encrypt(ciphertext, rev)
assert(decrypted == plaintext)

#-- Output --#
with open(sys.argv[2], 'wb') as f:
    f.write(ciphertext)
