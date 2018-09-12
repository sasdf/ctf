import os
import sys
from struct import pack, unpack
from IPython import embed
import subprocess
import re

root = sys.argv[1]

sizes = {
	7:  3, # Class
	9:  5, # Field ref
	10: 5, # Method ref
	11: 5, # Interface ref
	8:  3, # String
	3:  5, # Integer
	4:  5, # Float
	5:  9, # Long
	6:  9, # Double
	12: 5, # NameAndType
	1:  0, # UTF8 [var length]
	15: 4, # Method Handle
	16: 3, # Method Type
	18: 5, # Invoke Dynamic
}

JAVAP = 'C:\\Users\\sasdf\\Downloads\\jdk-10.0.2_windows-x64_bin\\tools\\bin\\javap'

def subSpace(s):
	for i in range(0x10):
		c = chr(0x2000 + i)
		h = ('%x__' % i)
		s = s.replace(c, h)
	return s

def getBSM(path):
	raw = subprocess.check_output([JAVAP, '-v', '-p', path])
	dis = subprocess.check_output([JAVAP, '-c', '-s', '-p', '-constants', path])
	idx = raw.find(b'BootstrapMethods:')
	if idx == -1:
		return []
	assert( raw.find(b'BootstrapMethods:', idx+1) == -1 )
	ret = raw[idx:].split(b'\n')[1:]
	res = []
	for i in range(0, len(ret), 7):
		chunk = [l.strip() for l in ret[i:i+7]]
		if b'd__7__b__5__e__2__f__a__f__c__."5__a__e__3__9__2__6__4__a__8__"' not in chunk[0]:
			continue
		print(chunk)
		invokeIdx = int(chunk[0][:chunk[0].find(b':')].decode('utf8'))
		className = int(chunk[4][1:chunk[4].find(b' ')].decode('utf8'))
		memberName = int(chunk[5][1:chunk[5].find(b' ')].decode('utf8'))
		memberDesc = int(chunk[6][1:chunk[6].find(b' ')].decode('utf8'))
		res.append((invokeIdx, className, memberName, memberDesc))
	return res, dis

def decrypt(s, key):
	res = ''.join(chr(ord(c) ^ key) for c in s.decode('utf8'))
	return subSpace(res)

def process(path):
	print(path)
	bsm, dis = getBSM(f'{path}.class')
	with open(f'{path}.class', 'rb') as f:
		data = f.read()
	assert( data.startswith(b'\xCA\xFE\xBA\xBE') )
	count, = unpack('>H', data[8:10])
	pool = [None]
	idx = 10
	for i in range(count-1):
		if data[idx] not in sizes:
			raise Error('WTFFF')
		if data[idx] == 1:
			l, = unpack('>H', data[idx+1:idx+3])
			pool.append(data[idx+3:idx+3+l])
			idx += l + 3
		elif data[idx] == 8:
			l, = unpack('>H', data[idx+1:idx+3])
			assert(isinstance(pool[l], bytes))
			pool.append(pool[l])
			idx += 3
		else:
			pool.append(None)
			if data[idx] == 5 or data[idx] == 6:
				pool.append(None)
			idx += sizes[data[idx]]
	for (invokeIdx, className, memberName, memberDesc) in bsm:
		invokeIdx = str(invokeIdx).encode('utf8')
		try:
			className = decrypt(pool[className], 4382)
			memberName = decrypt(pool[memberName], 3940)
			memberDesc = decrypt(pool[memberDesc], 5739)
		except:
			embed()
			raise
		rep = f'//  InvokeDynamic #{invokeIdx}: {className}/{memberName}:{memberDesc} |:'
		dis = dis.replace(b'// InvokeDynamic #' + invokeIdx + b':', rep.encode('utf8'))
	with open(f'{path}.class.java', 'wb') as f:
		f.write(dis)

def walk(root):
	global n
	for filename in os.listdir(root):
		path = os.path.join(root, filename)
		if os.path.isdir(path):
			walk(path)
		elif os.path.isfile(path):
			if not filename.endswith('.class'):
				continue
			process(path[:-6])
		else:
			raise Error('WTFFFFF')
walk(root)