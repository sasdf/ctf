import itertools as it

# Function b
def apply(x, y):
    if '+' in x:
        return y + ['+']
    elif '-' in x:
        return y[1:]
    else:
        raise('WTF')
        return []
# Function c
def c(x, y):
    if len(x):
        if len(y) >= len(x):
            return y
        else:
            return y + ['-']
    else:
        return ['-'] + y
	
# Function e
def lookup(x, y, dic):
    q = ''.join(x + y)
    return dic[q]

# Function h
def modify(x, y, z):
    return z[:len(y)-1] + x + z[len(y):]

# Function i
def defApply(x, y):
    r = apply(x, y)
    if len(r):
        return r
    else:
        return ['+']

# Function j
def get(x, y):
    return y[len(x)-1:][:1]

# Function l and k
def main(state, idx, result, dic):
    state = state + ['+', '-'] # Function m
    while True:
        print(' '.join(result))

        if state == TERMINATE: # Function d
            return len([e for e in result if e == '+'])

        val, op, state = lookup(state, get(idx, result), dic)
        idx, result = defApply(op, idx), c(apply(op, idx), modify(val, idx, result))

q = {
#         val    op    next state
'++--': (['+'], ['+'], list('+++')),
'++-+': (['-'], ['+'], list('--+')),
'+++-': (['-'], ['-'], list('++-')),
'++++': (['-'], ['+'], list('-++')),
'--+-': (['+'], ['+'], list('-++')),
'--++': (['+'], ['+'], list('+--')),
'-++-': (['+'], ['-'], list('-+-')),
'-+++': (['-'], ['-'], list('-++')),
'-+--': (['+'], ['+'], list('+-+')),
'-+-+': (['+'], ['-'], list('+++')),
'+-+-': (['+'], ['+'], list('++-')),
'+-++': (['+'], ['+'], list('-+-')),
'+---': (['+'], ['+'], list('---')),
'+--+': (['+'], ['-'], list('+--'))
}
TERMINATE = list('---')
main(['+'], ['+'], ['-'], q)
