#!/usr/python3


from struct import pack, unpack
from collections import Counter


with open('../task/task', 'rb') as f:
    data = f.read()


MOV_V_R14 = b'\x4c\x8b\x35'
MOV_V_R15 = b'\x4c\x8b\x3d'
MOV_R14_V = b'\x4c\x89\x35'
MOV_R15_V = b'\x4c\x89\x3d'
MOV_R15 = b'\x49\xc7\xc7'
OFF = 7 + 7
LEA = b'\x4c\x8d\x3d'
NOP = 0x90
JMP = 0xe9


data = list(data)

#-- Remove Junk --#
def remove(pat, off, size, relative=True):
    idx, i = [], -1
    while True:
        i = bytes(data).find(pat, i + 1)
        if i == -1:
            break
        idx.append(i)
    print(f'[*] Found {len(idx)} possible junk move gadgets')

    #-- Guess SAVE memory address --#
    values = [unpack('<i', bytes(data[i+3:i+7]))[0] + i if relative else 0 for i in idx]
    movValues = Counter(values)
    SAVE = movValues.most_common(1)[0][0]
    print(f'[*] Assume SAVE is located at 0x{SAVE:x}')

    #-- Find indirect jmp gadgets --#
    idx = [i - off for i, v in zip(idx, values) if v == SAVE]
    print(f'[*] Confirmed {len(idx)} junk move gadgets')
    print(f'')

    #-- Remove --#
    for i in idx:
        for j in range(size):
            data[i + j] = NOP
    return idx


remove(MOV_V_R14, 0, 14)
remove(MOV_R14_V, 0, 14)

#-- Find indirect jmp gadgets --#
idx = [i - 7 for i in remove(MOV_R15, 7, 26, relative=False)]

#-- Make sure all gadgets assign jmp target address --#
assert(all(bytes(data[i:i+len(LEA)]) == LEA for i in idx))


#-- Modify jmp --#
for i in idx:
    addr = unpack('<i', bytes(data[i+3:i+7]))[0]
    i -= 14
    for j in range(21):
        data[i+j] = NOP
    data[i] = JMP
    addr = pack('<i', addr - 42 + 14 + 16)
    for j, e in enumerate(addr):
        data[i + 1 + j] = e



#-- Output --#
with open('direct', 'wb') as f:
    f.write(bytes(data))
