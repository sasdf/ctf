import os
import sys
from IPython import embed

root = sys.argv[1]

def subSpace(s):
	for i in range(0x10):
		c = chr(0x2000 + i).encode('utf8')
		h = ('_%x_' % i).encode('utf8')
		s = s.replace(h, c)
	return s

def walk(path):
	if os.path.isdir(path):
		root = path
		for filename in os.listdir(root):
			path = os.path.join(root, filename)
			walk(path)
	elif os.path.isfile(path):
		if path.endswith('.class'):
			with open(path, 'rb') as f:
				data = subSpace(f.read())
			with open(path, 'wb') as f:
				f.write(data)
	else:
		raise Error('WTFFFFF')
walk(root)