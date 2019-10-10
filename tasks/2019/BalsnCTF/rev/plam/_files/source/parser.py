from collections import defaultdict
import re
from pylam import Variable, Abstraction, Application


def lexer(inp):
    ret = []
    while len(inp):
        c = inp.pop(0)
        if c == ' ':
            continue
        elif c == '(':
            expr, inp = lexer(inp)
            ret.append(expr)
        elif c == ')':
            return ret, inp
        else:
            ret.append(c)

    while len(ret) == 1 and isinstance(ret[0], list):
        ret = ret[0]
    return ret, inp


def build(inp, symbols):
    if isinstance(inp, str):
        return symbols[inp][-1]

    if inp[0] == 'λ':
        arg_name = inp[1]
        assert inp[2] == '.', inp[2]
        arg = Variable(arg_name)
        symbols[arg_name].append(arg)
        expr = build(inp[3:], symbols)
        symbols[arg_name].pop()
        return Abstraction(arg, expr)
    else:
        inp = [build(e, symbols) for e in inp]
        ret = inp.pop(0)
        for arg in inp:
            ret = Application(ret, arg)
        return ret


def parse(inp, symbols=None):
    symtab = defaultdict(list)
    if symbols is not None:
        for k, v in symbols.items():
            symtab[k].append(v)
    inp, remain = lexer(list(inp))
    assert len(remain) == 0
    return build(inp, symtab)


def parseFile(path, symbols=None):
    with open(path) as f:
        inp = f.read().splitlines()

    if symbols is None:
    	symbols = {}
    for line in inp:
        line = line.strip()
        if line.startswith('#') or line == '':
            continue
        if '=' in line:
            name, expr = line.split('=')
            name = name.strip()
            symbols[name] = parse(expr, symbols)
        else:
            symbols['_'] = parse(line, symbols)
    return symbols


def subTF(x):
    a, b, c = x.groups()
    if b == c:
        return 'F'
    if a == c:
        return 'T'
    return x.group(0)


def simplifyTF(x):
    return re.sub(r'\(λ(\w+)\.λ(\w+)\.(\w+)\)', subTF, x)
