import socket
import codecs

flagSZ = 1

def recvn(s, n):
    r = b''
    while len(r) != n:
        z = s.recv(n - len(r))
        if z == b'':
            raise EOFError('QAQ')
        r += z
    return r

def showall(s):
    z = None
    while z != b'':
        z = s.recv(1024)
        print(len(z))
        print(z)

def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('18.234.58.168', 5452))

    data = recvn(s, 81 * (flagSZ + 1)).splitlines()
    data = data[:flagSZ]
    payload = codecs.decode(b''.join(data), 'hex')

    xorkey = b'\x80'
    xorkey = list(xorkey) + [0] * len(payload)
    payload = bytes(a ^ b for a, b in zip(payload, xorkey))

    payload = codecs.encode(payload, 'hex')
    payload = b''.join([payload[i:i+80] + b'\n' for i in range(0, len(payload), 80)])


    for i in range(20):
        print(i)
        s.sendall(payload)
        recvn(s, 24+138)
    s.close()

while True:
    run()
