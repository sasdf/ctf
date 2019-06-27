from collections import defaultdict
import subprocess


def test(x):
    with open('enc.key', 'wb') as f:
        f.write(bytes.fromhex(x))

    try:
        ret = subprocess.check_output(
            'echo "U2FsdGVkX1/andRK+WVfKqJILMVdx/69xjAzW4KUqsjr98GqzFR793lfNHrw1Blc8UZHWOBrRhtLx3SM38R1MpRegLTHgHzf0EAa3oUeWcQ=" | openssl enc -d -aes-256-cbc -pbkdf2 -md sha1 -base64 --pass file:enc.key',
            shell=True,
        )
    except subprocess.CalledProcessError:
        return None
    return ret


transition = '01111110'
inittrans = defaultdict(list)
revtrans = defaultdict(list)
for i, e in enumerate(transition):
    trans = bin(i)[2:].rjust(3, '0')
    inittrans[e].append(trans)
    revtrans[e + trans[:2]].append(trans[2])


def dfs(p, s, x):
    if len(x) == 0:
        if s[-2:] == p[:2]:
            res = test(hex(int(s[:-1], 2))[2:])
            if res and b'CTF' in res:
                print(res)
                exit(0)
            return False
        return False
    for n in revtrans[x[0] + s[-2:]]:
        if dfs(p, s + n, x[1:]):
            return True


def rev126(x, bits=32):
    x = list(bin(x)[2:].rjust(bits, '0'))
    x0 = x[0]
    for p in inittrans[x0]:
        s = p[1:]
        if dfs(p, s, x[1:]):
            break
        
    
print(rev126(0x66de3c1bf87fdfcf, 64))
