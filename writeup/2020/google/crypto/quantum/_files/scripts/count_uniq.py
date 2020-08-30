import struct
from collections import Counter


sigs = []
with open('sigs.txt') as f:
    for line in f:
        try:
            line = bytes.fromhex(line)
            line = struct.unpack('<160Q', line)
            sigs.append(line)
        except Exception:
            break


print(f"{'idx':3s}: {'#uniq':^5s} - {'example':^16s} x {'cnt':<5s}")
for i in range(160):
    cnt = Counter(e[i] for e in sigs)
    m = cnt.most_common(1)
    print(f'{i:3d}: {len(cnt):5d} - {m[0][0]:016x} x {m[0][1]:<5d}')
