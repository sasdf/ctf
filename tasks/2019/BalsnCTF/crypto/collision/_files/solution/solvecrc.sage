import pickle
import hashlib
from tqdm import tqdm
from Crypto.Util.number import bytes_to_long, long_to_bytes


F = GF(2)

with open('data.pkl', 'rb') as f:
    data = pickle.load(f)

target = vector(F, data['bits'][-1])
M = Matrix(F, data['bits'][:-1])

print(repr(M))

k = M.left_kernel()
print(repr(k.basis_matrix()))

s = M.solve_left(target)
print(repr(s))

bar = tqdm(k)
try:
    for ki in bar:
        x = s + ki
        x = ZZ(x.list(), 2)
        x = data['prefix'] + long_to_bytes(x)[::-1] + data['suffix']
        if hashlib.md5(x).hexdigest() == data['md5']:
            tqdm.write('Found')
            break
finally:
    bar.close()

with open('ctx', 'wb') as f:
    f.write(x)
