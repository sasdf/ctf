import sys
from parser import parseFile, parse, simplifyTF

sys.setrecursionlimit(100000)


print('[*] Parsing')
symbols = parseFile(sys.argv[1])

print('[*] Running')
result = repr(symbols['_'].eval().simplify().alpha_norm())
result = simplifyTF(result)
print('[-] Result:', result)

