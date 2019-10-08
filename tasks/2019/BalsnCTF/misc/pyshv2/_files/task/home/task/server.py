#!/usr/bin/python3 -u

import securePickle as pickle
import codecs


pickle.whitelist.append('structs')


class Pysh(object):
    def __init__(self):
        self.login()
        self.cmds = {
            'help': self.cmd_help,
            'flag': self.cmd_flag,
        }

    def login(self):
        user = input().encode('ascii')
        user = codecs.decode(user, 'base64')
        user = pickle.loads(user)
        raise NotImplementedError("Not Implemented QAQ")

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

    def cmd_su(self):
        print("Not Implemented QAQ")
        # self.user.privileged = 1

    def cmd_flag(self):
        print("Not Implemented QAQ")


if __name__ == '__main__':
    pysh = Pysh()
    pysh.run()
