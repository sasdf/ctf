#!/usr/bin/python3 -u

import sys
import os
import codecs
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class SecureConsole(object):
    def __init__(self):
        self.remaining = 40
        aes = algorithms.AES(os.urandom(32))
        mode = modes.CTR(os.urandom(16))
        backend = default_backend()
        self.cipher = Cipher(aes, mode, backend=backend)
        self.encryptor = self.cipher.encryptor()

    def readhexline(self):
        chunk = b''
        while len(chunk) < 81:
            ret = sys.stdin.buffer.read(81 - len(chunk))
            if len(ret) == 0:
                raise EOFError('EOF while readhexline')
            chunk += ret
        assert chunk[-1:] == b'\n', 'newline'
        chunk = codecs.decode(chunk[:-1], 'hex')
        return chunk
        
    def readline(self):
        data = b''
        decryptor = self.cipher.decryptor()
        while not data.endswith(b'\0'):
            chunk = self.readhexline()
            chunk = decryptor.update(chunk)
            data += chunk
        return data.rstrip(b'\0')

    def write(self, data):
        data = data.encode('utf8')
        while len(data):
            chunk = data[:self.remaining]
            ct = self.encryptor.update(chunk)
            ct = codecs.encode(ct, 'hex')
            sys.stdout.buffer.write(ct)
            data = data[len(chunk):]
            self.remaining -= len(chunk)
            if self.remaining == 0:
                sys.stdout.buffer.write(b'\n')
                self.remaining = 40
        return self

    def endl(self):
        ct = self.encryptor.update(b'\0' * self.remaining)
        ct = codecs.encode(ct, 'hex') + b'\n'
        sys.stdout.buffer.write(ct)
        self.remaining = 40
        return self


def main(flag):
    sc = SecureConsole()

    sc.write(flag).endl()
       
    for _ in range(30):
        sc.write('[>] Gimme your flag: ').endl()
        line = sc.readline()

        sc.write('[*] Result: ')

        try:
            line = line.decode('utf8')
            if line == flag:
                sc.write('OK').endl()
            else:
                sc.write('Nope').endl()
        except:
            sc.write('QAQ').endl()


if __name__ == '__main__':
    sys.stderr.close()
    with open('../flag.txt', 'rb') as f:
        flag = f.read()
    flag = codecs.encode(flag, 'hex').decode('utf8')
    assert len(flag) <= 70
    main(flag)
