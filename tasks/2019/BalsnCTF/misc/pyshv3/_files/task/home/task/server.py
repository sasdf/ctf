#!/usr/bin/python3 -u

import securePickle as pickle
import codecs
import os


pickle.whitelist.append('structs')


class Pysh(object):
    def __init__(self):
        self.key = os.urandom(100)
        self.login()
        self.cmds = {
            'help': self.cmd_help,
            'whoami': self.cmd_whoami,
            'su': self.cmd_su,
            'flag': self.cmd_flag,
        }

    def login(self):
        with open('../flag.txt', 'rb') as f:
            flag = f.read()
        flag = bytes(a ^ b for a, b in zip(self.key, flag))
        user = input().encode('ascii')
        user = codecs.decode(user, 'base64')
        user = pickle.loads(user)
        print('Login as ' + user.name + ' - ' + user.group)
        user.privileged = False
        user.flag = flag
        self.user = user

    def run(self):
        while True:
            req = input('$ ')
            func = self.cmds.get(req, None)
            if func is None:
                print('pysh: ' + req + ': command not found')
            else:
                func()

    def cmd_help(self):
        print('Available commands: ' + ' '.join(self.cmds.keys()))

    def cmd_whoami(self):
        print(self.user.name, self.user.group)

    def cmd_su(self):
        print("Not Implemented QAQ")
        # self.user.privileged = 1

    def cmd_flag(self):
        if not self.user.privileged:
            print('flag: Permission denied')
        else:
            print(bytes(a ^ b for a, b in zip(self.user.flag, self.key)))


if __name__ == '__main__':
    pysh = Pysh()
    pysh.run()
