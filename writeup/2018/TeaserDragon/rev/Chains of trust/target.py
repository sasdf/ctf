import sys
from elftools.elf.elffile import ELFFile

if len(sys.argv) != 3:
    print('Usage: python3 target.py coredump')

v4 = [
    0x9DF9 , 0x65E  , 0x3B94 , 0x0FAD9,
    0x0C3D9, 0x0FE12, 0x0A57B, 0x9089 ,
    0x3FAF , 0x0BB31, 0x4CAD , 0x1415 ,
    0x74CD , 0x0CF0A, 0x1CE1 , 0x0B55A,
    0x54C6 , 0x827F , 0x179D , 0x66D9 ,
    0x0FF80, 0x8126 , 0x5579 , 0x4AED ,
    0x5F7D , 0x430F , 0x2EE4 , 0x129C ,
    0x0DBCD, 0x0EB50, 0x8DA8 , 0x0BDD1,
]

target = [
    0xDEADB905, 0xDEADB92D, 0xDEADB955, 0xDEADB97D,
    0xDEADB9A5, 0xDEADB9A5, 0xDEADB9A5, 0xDEADB9CD,
    0xDEADB9F5, 0xDEADBA1D, 0xDEADBA45, 0xDEADBA6D,
    0xDEADBA6D, 0xDEADBA95, 0xDEADBABD, 0xDEADBAE5,
    0xDEADBB0D, 0xDEADBB35, 0xDEADBB5D, 0xDEADBB85,
    0xDEADBBAD, 0xDEADBBD5, 0xDEADBBFD, 0xDEADBBFD,
    0xDEADBC25, 0xDEADBC4D, 0xDEADBC75, 0xDEADBC9D,
    0xDEADBCC5, 0xDEADBC75, 0xDEADBCED, 0xDEADBCED,
]

elf = ELFFile(open(sys.argv[1], 'rb'))
target = [next(elf.address_offsets(t)) for t in target]
elf.stream.seek(0)
data = elf.stream.read()
target = [data[t:t+32] for t in target]

for t in range(32):
    found = False
    for i in range(65536):
        k = i
        for z in range(32):
            k = ((k >> 1) | (k << 15)) & 0xffff
            k = k ^ v4[z]
            if (k & 0xff) != target[t][z]:
                break
            if z == 31:
                found = True
                print('%2d 0x%04x' % (t, i))
    if not found:
        print('wtf')
