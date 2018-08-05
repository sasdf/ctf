#!/usr/bin/python3.6

from elftools.elf.elffile import ELFFile
import subprocess
import binascii


with open('../task/task', 'rb') as f:
    #-- Get address of encrypted flag --#
    elf = ELFFile(f)
    symtab = elf.get_section_by_name('.symtab')
    target = symtab.get_symbol_by_name('C')[0].entry.st_value
    target = next(elf.address_offsets(target))

    #-- Read encrypted flag --#
    f.seek(target)
    target = f.read(64)

    #-- Decrypt == Encrypt --#
    out = subprocess.check_output('../task/task', input=target, stderr=subprocess.STDOUT)
    out = b''.join([l[len(b'[=] '):] for l in out.split(b'\n') if l.startswith(b'[=] ')])
    out = out.replace(b'0x', b'').replace(b' ', b'').replace(b',', b'')
    out = binascii.a2b_hex(out).rstrip(b'\0').decode('ascii')
    print(f'[+] Flag: {out}')
