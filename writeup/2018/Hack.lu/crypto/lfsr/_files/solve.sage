from sage.crypto.util import bin_to_ascii


F = GF(2)


# LFSR Matrix
characteristic = F["x"]("x^256 + x^10 + x^5 + x^2 + 1")
LFSR = companion_matrix(characteristic, format="bottom")


# Sanity check
state = vector(F, [1] + [0] * 255)
bits = []
for i in range(1024):
    bits.append(state[0])
    state = LFSR * state
print('[*] Output of seed 0x1')
print(hex(Integer(bits, 2)))


# First 1001 Output Key-Bits (LSB = 0th output, MSB = 1000th output)
y = Integer("""
131018c85020813093200c6ae4822e400261853722f054a1e0
80560034008605080380810640342825506829c0209a04134010
1b54f1848425aa208035d40510068044597575a02b115a900243
6958884d110a2515022240aec060e0a0200c4296081062829a00
328250210001533404b206301482800234000501d0104
""", 16).bits()


print('[*] Recovering initial seed')
# x0 + x64 + x96 + x128 + x192 + x255 + 1
annihilator = [0, 64, 96, 128, 192, 255]
ones = [i for i, yi in enumerate(y) if yi]
equs = Matrix(F, [sum((LFSR^i)[annihilator]) for i in ones])
print('[+] Generated %d equations' % equs.nrows())
sol = equs.solve_right(vector(F, [1] * equs.nrows()))
for i, ker in enumerate(equs.right_kernel()):
    s = bin_to_ascii((sol + ker)[::-1])
    print('[+] Solution %d: %s' % (i, repr(s)))
