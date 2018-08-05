#!/usr/python3


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


print(f'[*] Relocating fragments')
top, bottom = text_va + idx[0], text_va + idx[-1]
addrMap = {insn.address: top + i * 10 for i, insn in enumerate(sortedFrags)}
addrMap[main.address] = main.address
sortedFrags.insert(0, main)
relocatedFrags = []
for insn in sortedFrags:
    addr = addrMap[insn.address]
    mnemonic = insn.mnemonic
    opstr2 = opstr = insn.op_str
    for op in insn.operands:
        if op.type == capstone.x86.X86_OP_MEM and op.value.mem.base == capstone.x86.X86_REG_RIP:
            target = op.mem.disp + insn.address
            sign = '+' if target >= 0 else '-'
            memstr = f'[rip {sign} 0x{op.mem.disp:x}]'
            relocation = addrMap.get(target, target) - addrMap[insn.address]
            signr = '+' if relocation >= 0 else '-'
            recstr = f'[rip {signr} 0x{relocation:x}]'
            opstr2 = re.sub(re.escape(memstr), recstr, opstr2)
        elif op.type == capstone.x86.X86_OP_IMM:
            target = op.value.imm
            memstr = f'0x{target:x}'
            relocation = addrMap.get(target, None)
            if relocation is not None:
                recstr = f'0x{relocation:x}'
                opstr2 = re.sub(re.escape(memstr), recstr, opstr2)
    if opstr != opstr2:
        print(f"[.] 0x{addr:x}\t{mnemonic}\t{opstr}\t->\t{mnemonic}\t{opstr2}")
    relocatedFrags.append((addr, f'{mnemonic} {opstr2}'))
print(f"[-] New main at 0x{addrMap[mainAddr]:x}")
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
    for addr, insn in relocatedFrags:
        insn = bytes(ks.asm(insn, addr)[0])
        out.seek(text_off + addr - text_va)
        out.write(insn)
    for addr, dest in symPatch:
        out.seek(symtab_off + addr)
        out.write(dest)

# embed()
