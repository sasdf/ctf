#!/usr/bin/python3 -u

import securePickle as pickle
import codecs


pickle.whitelist.append('sys')


class Pysh(object):
    def __init__(self):
        self.login()
        self.cmds = {}

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


if __name__ == '__main__':
    pysh = Pysh()
    pysh.run()
