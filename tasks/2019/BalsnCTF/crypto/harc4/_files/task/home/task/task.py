#!/usr/bin/python3 -u
import os
import binascii

from Crypto.Cipher import ARC4


db = {}
IV = os.urandom(32)


def harc4(x):
    ksz = ARC4.key_size[-1]
    csz = ksz - len(IV)

    state = IV
    for i in range(0, len(x), csz):
        key = x[i:i+csz] + state
        cipher = ARC4.new(key)
        state = cipher.encrypt(state)
    return state.hex()


def main():
    # Generate the ultimate password
    db['admin'] = harc4(os.urandom(42))

    for _ in range(10):
        cmd = input('> ')

        if cmd == 'register' or cmd == 'login':
            username = input('Username: ')
            password = input('Password: ')
            try:
                password = harc4(binascii.a2b_hex(password))
            except binascii.Error:
                print('[!] Nope')
                continue

        if cmd == 'register':
            if username in db:
                print('[!] Nope')
            else:
                db[username] = password
        elif cmd == 'login':
            if db.get(username, None) != password:
                print('[!] Nope')
            elif username == 'admin':
                with open('../flag.txt') as f:
                    print('[+] ' + f.read())
            else:
                print('[+] Welcome %s' % username)
        elif cmd == '_debug':
            print(db)
        else:
            print('[!] Unknown command %s, Available commands: register, login' % cmd)


if __name__ == '__main__':
    main()
