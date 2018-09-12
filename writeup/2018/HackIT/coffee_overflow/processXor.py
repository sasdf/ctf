import os
import sys
from struct import pack, unpack
from IPython import embed
import subprocess
import re

root = sys.argv[1]

def process(path):
	print(path)
	with open(path, 'rb') as f:
		dis = [l.rstrip() for l in f.read().split(b'\n')]
	for i in range(2, len(dis)):
		if dis[i].endswith(b'ixor') and b'// int ' in dis[i-1] and b'// int ' in dis[i-2]:
			a = int(dis[i-2][dis[i-2].find(b'// int ')+7:])
			b = int(dis[i-1][dis[i-1].find(b'// int ')+7:])
			off = dis[i-2].find(b'// int ')
			dis[i] = dis[i].ljust(off) + b'// eql ' + str(a ^ b).encode('utf8')
	with open(path, 'wb') as f:
		f.write(b'\n'.join(dis))

def walk(root):
	global n
	for filename in os.listdir(root):
		path = os.path.join(root, filename)
		if os.path.isdir(path):
			walk(path)
		elif os.path.isfile(path):
			if not filename.endswith('.java'):
				continue
			process(path)
		else:
			raise Error('WTFFFFF')
walk(root)