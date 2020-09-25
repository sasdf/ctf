import re


with open('./metal_genx_0.visaasm') as f:
    code = f.read()
    code = re.sub(r'///[^\n]+', '', code)
    code = code.splitlines()
    code = [line.strip() for line in code]

REGION = {
    '0;1,0': '',
    '1,0':   '.Pointer',
    '1;1,0': ':',
    '2;1,0': '::2',
    '1':     ':',
    '8':     '::8',
    '16':    '::16',
}
SIZES = {
    'q':    8, 'v':  4, 'd':  4, 'w':  2, 'b':  1,
    'uq':   8, 'uv': 4, 'ud': 4, 'uw': 2, 'ub': 1,
    'df':   8, 'f':  4, 'vf': 4, 'hf': 2,
    'bool': 1, 'G':  32,
}
decl = {}
replaces = {}

def format_arg(org):
    modifier, arg, kind = re.match(r'^(?:\(([^)]+)\))?([^:]+)(?::(.+))?$', org).groups()
    modifier = f'({modifier})' if modifier else ''
    kind = f':{kind}' if kind else ''
    if arg.startswith('0x'):
        return org
    elif arg.startswith('&'):
        return org
    elif arg.startswith('r['):
        key, addr_offset, ind_offset, region = re.match(r'^r\[(\w+)\((\w+)\),(\w+)\]<([^>]+)>$', arg).groups()
        if region == '1,0':
            return f'{modifier}{key}[{addr_offset}:, {ind_offset}]{kind}'
        else:
            return f'{modifier}{key}[{addr_offset}][{ind_offset}{REGION[region]}]{kind}'
    else:
        key, row_offset, col_offset, region = re.match(r'^(\w+)(?:\((\w+)(?:,(\w+))?\))?(?:<([^>]+)>)?$', arg).groups()
        row_offset = int(row_offset or '0')
        col_offset = int(col_offset or '0')
        assert kind == ''
        vkind, vname, numel, kind = decl[key]
        if numel == 1 and region in [None, '1', '0;1,0'] and vkind != 'A':
            kind = f':{kind}' if kind else ''
            return f'{modifier}{key}{kind}'
        if region is None:
            return arg
        if vkind != 'A':
            size = SIZES[kind]
            assert 32 % size == 0
            offset = row_offset * 32 // size + col_offset
            return f'{modifier}{key}[{offset}{REGION[region]}]:{kind}'
        else:
            assert row_offset == col_offset == 0
            return f'{modifier}{key}[0:{region}]:A'

ret = ''
for line in code:
    if line.startswith('//'):
        pattern = r'// .decl (\w+) v_type=(\w+) v_name=(\w*)'
        key, vkind, vname = re.match(pattern, line).groups()
        decl[key] = (vkind, vname, 1, 'G')
        replaces[key] = vname
        ret += line + '\n'
        pass
    elif line.startswith('.decl'):
        pattern = '.decl (\w+) v_type=(\w+)(?: type=(\w+))? num_elts=(\w+)(?: align=(\w+))?(?: alias=<(\w+), 0>)?(?: v_name=(\w+))?$'
        key, vkind, kind, numel, align, alias, vname = re.match(pattern, line).groups()
        decl[key] = (vkind, vname, int(numel), kind)
        replaces[key] = vname
        if alias is not None:
            replaces[key] = f'{alias}.({kind}[{numel}])'
        ret += line + '\n'
        pass
    elif line.startswith('.'):
        ret += line + '\n'
        pass
    elif line.endswith(':'):
        ret += line + '\n'
        pass
    elif line == '':
        ret += line + '\n'
        pass
    else:
        pred, op, em, args = re.match(r'^(?:\(([\w!]+)\) )?([\w\.]+)(?: \((?:M1, )?(\w+)\))?(.*)$', line).groups()
        em = int(em or '0')
        pred = f'({pred})' if pred else ''
        args = [e for e in args.strip().split(' ') if e]
        ret += ' ' * 4
        if op in ['oword_ld', 'oword_st']:
            ret += line + '\n'
            continue
        op2 = f'{op}<{em}>{pred}' if em else f'{op}{pred}'
        ret += op2.ljust(15)
        if op in ['jmp', 'call', 'ret']:
            ret += f'{" ".join(args)}' + '\n'
            continue
        args = [format_arg(e) for e in args]
        ret += ' '.join(e.ljust(20) for e in args) + '\n'
        pass

replaces = {k: v for k, v in replaces.items() if v is not None}
print(replaces)
for key, val in replaces.items():
    ret = re.sub(r'\b'+re.escape(key)+r'\b', val, ret)

aligned = ''
for line in ret.splitlines():
    if line.startswith('  '):
        line = re.split(r'\s+', line.strip())
        line = ' '*4 + ' '.join(e.ljust(20) for e in line)
    aligned += line + '\n'
print(aligned)
