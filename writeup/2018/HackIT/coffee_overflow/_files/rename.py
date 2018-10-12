import os
import sys
from IPython import embed

root = sys.argv[1]

def subSpace(s):
	for i in range(0x10):
		c = chr(0x2000 + i).encode('utf8')
		h = ('_%x_' % i).encode('utf8')
		s = s.replace(c, h)
	return s

def walk(root):
	global n
	for filename in os.listdir(root):
		path = os.path.join(root, filename)
		if os.path.isdir(path):
			walk(path)
		elif os.path.isfile(path):
			pass
			with open(path, 'rb') as f:
				data = subSpace(f.read())
			with open(path, 'wb') as f:
				f.write(data)
		else:
			raise Error('WTFFFFF')
		newname = subSpace(filename.encode('utf8')).decode('utf8')
		print(f'{repr(filename)} => {newname}')
		os.rename(path, os.path.join(root, newname))
walk(root)