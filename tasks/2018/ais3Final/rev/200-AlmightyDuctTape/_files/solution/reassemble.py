#!/usr/python3


"""
To run this script, You need to install keystone from github (commit 067d2bd, which is the newest commit at the time writing).
You also need to patch [a symbol_resolver bug](https://github.com/keystone-engine/keystone/issues/351) to make it work.
If you want to use keystone from pip, see `reassemble2.py` for a hacky implementation of relocation.
"""
import re
import capstone
import keystone
from struct import pack
from elftools.elf.elffile import ELFFile
# from IPython import embed


elfPath = '../task/task'


print(f'[*] Initializing (dis)assembler')
MOV_R15 = b'\x49\xc7\xc7'
LEA = b'\x4c\x8d\x3d'
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
ks = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
md.detail = True
md.skipdata = True


print(f'[*] Loading ELF')
f = open(elfPath, 'rb')
f.seek(0)
orig = f.read()
elf = ELFFile(f)
text = elf.get_section_by_name('.text')
text_va = text.header['sh_addr']
text_off = text.header['sh_offset']
text_data = text.data()
print(f"[-] Text section at 0x{text_va:x} (0x{text_off:x})")
symtab = elf.get_section_by_name('.symtab')
symtab_off = symtab.header['sh_offset']
symtab_data = symtab.data()
print(f"[-] Symbol table at 0x{symtab_off:x}")
entry = elf.header['e_entry']
print(f"[-] Entrypoint at 0x{entry:x}")
main = next(i for i in md.disasm(text_data[entry - text_va:][:200], entry)
    if i.mnemonic == 'mov' and
    i.operands[0].type == capstone.x86.X86_OP_REG and
    i.operands[0].value.reg == capstone.x86.X86_REG_RDI and
    i.operands[1].type == capstone.x86.X86_OP_IMM
    )
mainAddr = main.operands[1].value.imm
print(f"[-] main at 0x{mainAddr:x}")
print(f'')


print(f'[*] Collecting fragments')
idx, i = [], -1
while True:
    i = text_data.find(MOV_R15, i + 1)
    if i == -1:
        break
    if text_data[i-14:i-11] == LEA:
        idx.append(i-7)
print(f'[-] Found {len(idx)} fragments')
print(f'')


print(f'[*] Parsing fragments')
fragments = {}
for i in idx:
    #-- Disassemble fragment --#
    code = text_data[i - 200: i]
    instrs = list(md.disasm(code, i - 200 + text_va))
    insn, nxt = instrs[-4], instrs[-1]

    #-- Parse address of next fragment --#
    assert(nxt.mnemonic == 'lea')
    assert(nxt.operands[0].type == capstone.x86.X86_OP_REG)
    assert(nxt.operands[0].value.reg == capstone.x86.X86_REG_R15)
    assert(nxt.operands[1].type == capstone.x86.X86_OP_MEM)
    assert(nxt.operands[1].value.mem.base == capstone.x86.X86_REG_RIP)
    assert(nxt.operands[1].value.mem.index == capstone.x86.X86_REG_INVALID)
    nxt = nxt.operands[1].value.mem.disp + nxt.address + len(nxt.bytes) - 42 + 14

    #-- Parse instruction --#
    assert(insn.insn_name() != '(invalid)')
    # print("0x%x:\t%s\t%s" % (insn.address, insn.mnemonic, insn.op_str))

    fragments[insn.address] = (nxt, insn)
print(f'')


print(f'[*] Sorting fragments')
addrs = set(fragments.keys())
nxts = set(nxt for nxt, insn in fragments.values())
head, tail = addrs - nxts, nxts - addrs
assert(len(head) == 1 and len(tail) == 1)
head, tail = next(iter(head)), next(iter(tail))
fragments[tail] = (None, None)
sortedFrags = []
nxt = head
while nxt:
    nxt, insn = fragments[nxt]
    if insn:
        sortedFrags.append(insn)
print(f'')


print(f'[*] Labeling fragments')
top, bottom = text_va + idx[0], text_va + idx[-1]
labelMap = {insn.address: f'GLUE_{i}' for i, insn in enumerate(sortedFrags)}
labeledFrags = []
sign = '+-'
for insn in sortedFrags:
    mnemonic = insn.mnemonic
    opstr2 = opstr = insn.op_str
    for op in insn.operands:
        if op.type == capstone.x86.X86_OP_MEM and op.value.mem.base == capstone.x86.X86_REG_RIP:
            target = op.mem.disp + insn.address + len(insn.bytes)
            label = labelMap.get(target, f'REL_{target:x}')
            memstr = f'[rip {sign[op.mem.disp < 0]} 0x{abs(op.mem.disp):x}]'
            opstr2 = re.sub(re.escape(memstr), f'[rip + {label}]', opstr2)
        elif op.type == capstone.x86.X86_OP_IMM:
            target = op.value.imm
            label = labelMap.get(target, None)
            if label is not None:
                memstr = f'0x{target:x}'
                opstr2 = re.sub(re.escape(memstr), label, opstr2)
    if opstr != opstr2:
        print(f"[.] {mnemonic}\t{opstr}\t->\t{mnemonic}\t{opstr2}")
    labeledFrags.append((labelMap[insn.address], f'{mnemonic} {opstr2}'))
print(f'')


print(f'[*] Assembling')
code = ''.join(f'{label}:\n{insn}\n' for label, insn in labeledFrags)
labels = list(labelMap.items())
code += ''.join(f'jmp {label}\n' for addr, label in labels)
def sym_resolver(symbol, value):
    if symbol.startswith(b'REL_'):
        addr = int(symbol[4:], 16)
        value.contents.value = addr
        return True
    return False
ks.sym_resolver = sym_resolver
reassembled, _ = ks.asm(code, top)
reassembled = bytes(reassembled)
disasm = list(md.disasm(reassembled, top))
disasm, addrs = disasm[:-len(labels)], disasm[-len(labels):]
tail = sum(len(insn.bytes) for insn in addrs)
reassembled = reassembled[:-tail]
for insn in disasm:
    print(f"[.] 0x{insn.address:x}\t{insn.mnemonic}\t{insn.op_str}")
addrs = [insn.operands[0].value.imm for insn in addrs]
addrMap = {src: dest for (src, _), dest in zip(labels, addrs)}
print(f"[-] New main at 0x{addrMap[mainAddr]:x}")
mainInsn = bytes(ks.asm(f'mov rdi, {addrMap[mainAddr]}', main.address)[0])
print(f'')


print(f'[*] Relocating symbol table')
symPatch, i = [], -1
for i, sym in enumerate(symtab.iter_symbols()):
    i = i * 24 + 8
    if '_GLUE' in sym.name:
        symPatch.append((i, b'\0' * 8))
    elif sym.entry.st_value in addrMap:
        symPatch.append((i, pack('<Q', addrMap[sym.entry.st_value])))
print(f'[-] Found {len(symPatch)} symbols need to be relocated')
print(f'')


print(f'[*] Reassembling & Patching')
with open('reassemble', 'wb') as out:
    out.write(orig)
    out.seek(text_off + top - text_va)
    out.write(b'\x90' * (bottom - top))
    out.seek(text_off + top - text_va)
    out.write(reassembled)
    out.seek(text_off + main.address - text_va)
    out.write(b'\x90' * len(main.bytes))
    out.seek(text_off + main.address - text_va)
    out.write(mainInsn)
    for addr, dest in symPatch:
        out.seek(symtab_off + addr)
        out.write(dest)

# embed()
