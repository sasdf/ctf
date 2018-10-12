import itertools as it
import re
import hashlib

Q = {
    #      val  op  next         val  op  next
    'A.': ('x',  1, 'B'), 'Ax': ('.',  1, 'C'),
    'B.': ('.', -1, 'A'), 'Bx': ('.',  1, 'D'),
    'C.': ('x',  1, 'D'), 'Cx': ('x',  1, 'G'),
    'D.': ('x', -1, 'E'), 'Dx': ('.', -1, 'D'),
    'E.': ('x',  1, 'F'), 'Ex': ('x', -1, 'B'),
    'F.': ('x',  1, 'A'), 'Fx': ('x',  1, 'E'),
    'G.': ('x',  1, 'T'), 'Gx': ('x', -1, 'G'),
}


def emulate(pat, st):
    state, idx, last = 'E', 12, 0
    tape = ['x'] * idx + list(pat)
    for i in it.count():
        if state == 'T':
            break
        val, op, state = Q[state + tape[idx]]
        tape[idx] = val
        idx += op
        if idx >= len(tape):
            tape.append('.')
        elif idx < 0:
            if i - last == 1:
                break # Another wave
            last = i
            tape.insert(0, '.')
            idx = 0
    tape = ''.join(tape)
    nxt = re.sub(r'^(\.x)+', '', tape[3:]) # Next state
    extra = len(tape) - 12 - len(pat) + len(st) - len(nxt) + 2
    if state != 'T':
        return nxt, extra
    else:
        extra += len(nxt) # We don't have next state after terminated
        return None, (extra - len([c for c in tape if c != 'x']))


size = 0
state = ''
altSeq = '.x' * 4

for i in it.count():
    altSize = size - 2 # Length of prefix alternating sequence
    inc = altSize // 4 # Change of length after arriving right boundary
    pat = ['..', '...'][inc % 2] + altSeq[len(altSeq)-(altSize % 4):] + state

    print(f'[*] From: {size + len(state)}')
    print(f'[*] Inc: {size + len(state) + inc}')
    print(f'[*] State: {state}, Pattern: {pat}')
    state, extra = emulate(pat, state)
    size += inc + extra

    if state is None:
        break
    print(f'[*] To: {size + len(state)}, State: {state}')
    print(f'')

print(f'')
print(f'[+] Terminate: {size}')


# Decrypt Flag
d = [
    -48, 2  , -48, -8 , -59, -18, 1  , -59,
    3  , -5 , -26, -57, 53 , 3  , -43, -3 ,
    -41, -20, 1  , -64, -65, -45, -71, -47,
    -16, -47, -38, -3 , 46 , -63, -54, 1  ,
    -49, 4  , -51, -45, -61, -46, -13, -4 ,
    -65, -48, -55, -51, -38, -64, -50, -5 ,
    -65, 2  , -54, -56, -1 , -50, -28
]
h = hashlib.sha256(f'{size}\n'.encode('ascii')).hexdigest().encode('ascii')
e = bytes(a - b for a, b in zip(h, d)).decode('ascii')
print(f'[+] Flag: {e}')
