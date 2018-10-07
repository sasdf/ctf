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

TERMINATE = 'T'
state = 'A'
idx = 90
tape = ['.'] * 120
for i in range(7000):
    # Visulize
    line = ''.join(tape)[-120:]
    print(f'{i:4d} {state} {line}')

    if state == TERMINATE:
        print(len([e for e in tape if e == 'x']))
        exit(0)

    # Next state
    val, op, state = Q[state + tape[idx]]
    tape[idx] = val
    idx += op

    # Extend tape
    if idx >= len(tape):
        tape.append('.')
    elif idx < 0:
        tape.insert(0, '.')
        idx = 0
