import sys
from parser import parseFile, parse
from pylam import Variable

sys.setrecursionlimit(100000)


symbols = {}
symbols['M'] = Variable('M', showid=False)
symbols['I'] = Variable('I', showid=False)
symbols = parseFile('def.txt', symbols)

for k, v in symbols.items():
    if k in 'YMI_':
        continue
    symbols[k] = v.eval().simplify()
    assert len(symbols[k].freevar()) == 0, k

print(symbols['_'].alpha_norm())
