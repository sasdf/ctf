import telnetlib
import binascii
from tqdm import tqdm, trange

r = telnetlib.Telnet('arcade.fluxfingers.net', 1821)
d = ''
for k in trange(2):
    for i in range(64 * k, 64 * (k+1)):
        r.write(f'XOR\n'.encode('ascii'))
        r.write(f'{1 << i:x}\n'.encode('ascii'))
        r.write(f'ADD\n'.encode('ascii'))
        r.write(f'{1 << i:x}\n'.encode('ascii'))

    for i in range(64 * k, 64 * (k+1)):
        r.read_until(b'Ciphertext is  ')
        x = r.read_until(b'\n')[:-1] + r.read_until(b'\n')[:-1]
        r.read_until(b'Ciphertext is  ')
        a = r.read_until(b'\n')[:-1] + r.read_until(b'\n')[:-1]
        d = str((x != a) * 1) + d
        tqdm.write(d)

key = binascii.b2a_base64(int(d, 2).to_bytes(16, 'big')).replace(b'\n', b'')
r.read_until(b'-----------------------------*\n')
r.write(f'DEC\n'.encode('ascii'))
r.write(key + b'\n')
r.interact()
