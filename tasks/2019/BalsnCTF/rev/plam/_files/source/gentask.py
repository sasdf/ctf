import re
import random
import sys
sys.setrecursionlimit(100000)
from pprint import pprint
from collections import defaultdict

flagSZ = 96
branchSZ = 16
fakeSZ = 16
chunkSZ = 4
randBranchNum = 32
randLeafNum = 10000
randBranchSZ = flagSZ * chunkSZ
use_pair = False
use_plam = True


# flag = input('flag > ').strip()
with open('flag.txt') as f:
    flag = f.read().strip()
assert re.match(r'^Balsn\{[0-9a-f]{24}\}$', flag)
flag = bin(int(flag[6:-1], 16))[2:].rjust(flagSZ, '0')
assert len(flag) == flagSZ
flag = list(map(int, flag))

assert flagSZ % chunkSZ == 0
TF = [set(), set([flagSZ])]

# Generate invertible matrix
matrix = [set([i]) ^ TF[v] for i, v in enumerate(flag)]
for _ in range(10000):
	i, j = random.randrange(flagSZ), random.randrange(flagSZ)
	if i == j:
		continue
	matrix[i] ^= matrix[j]
# matrix[0] ^= TF[1]

# Helper methods
def rand_comb(matrix):
	"""Random linear combination"""
	res = set()
	while len(res) == 0:
		for row in matrix:
			if random.randrange(2):
				res ^= row
	return res

def rand_row():
	"""Random row"""
	res = []
	while len(res) == 0:
		res = set(i for i in range(flagSZ) if random.randrange(2))
	res ^= TF[random.randrange(2)]
	return res

# Build branch group
chunks0 = [matrix[i:i+chunkSZ] for i in range(0, flagSZ, chunkSZ)]
data0 = []
truth0 = []

# Construct first group with linear dependent row
Msel = [rand_row() for _ in range(chunkSZ)]
Msel[0] = rand_comb(matrix) ^ TF[1] ^ rand_comb(Msel[1:])
Mtrue = [rand_row() for _ in range(chunkSZ)]
Mfalse = [rand_comb(matrix) for _ in range(chunkSZ)]
same = Mfalse[0]
while same in Mfalse:
	same = rand_comb(Mfalse)
Mtrue[0] = same ^ rand_comb(Msel) ^ rand_comb(Mtrue[1:])
data0.append((Msel, Mtrue, Mfalse))
truth0.append(same)

while True:
	chunks = chunks0[:]
	data = data0[:]
	truth = truth0[:]
	# Construct other groups with collision
	while len(chunks):
		if len(chunks) > 1 and random.randrange(2):
			Msel = chunks.pop()
			swap = False
		else:
			Msel = [rand_row() for _ in range(chunkSZ)]
			Msel[0] = rand_comb(matrix) ^ TF[1] ^ rand_comb(Msel[1:])
			swap = True
		Mtrue = chunks.pop()
		Mfalse = [rand_row() for _ in range(chunkSZ)]
		Mfalse[0] = rand_comb(truth) ^ TF[1] ^ rand_comb(Mfalse[1:])
		truth.extend(Mtrue)
		if swap:
			Mfalse[0] ^= rand_comb(Msel)
			Mtrue, Mfalse = Mfalse, Mtrue
		else:
			truth.extend(Msel)
		data.append((Msel, Mtrue, Mfalse))
	if len(data) == branchSZ:
    		break

# Randomize branch group order
random.shuffle(data)

# Flatten & negate & add dummy tail
tables = []
for branch in data:
	tables.extend([r ^ TF[1] for r in t] + [rand_row()] for t in branch)

# Evaluate
"""
for t in tables:
	f = flag + [1]
	res = sum(sum(f[i] for i in row) & 1 for row in t[:-1]) == len(t) - 1
	print('FT'[res])
"""

# Add dummy chain
for _ in range(fakeSZ):
	tables.append([rand_row() for _ in range(chunkSZ + 1)])


"""
tables = [[
	[1, 0, 0, 1, 1],
	[1, 1, 0, 0, 1],
	[0, 0, 1, 1, 0],
	[0, 0, 1, 0, 1],
	[1, 0, 0, 1, 1],
], [
	[0, 1, 0, 1, 1],
	[0, 1, 0, 0, 1],
	[1, 0, 1, 1, 0],
	[0, 0, 1, 0, 1],
	[0, 0, 0, 1, 1],
],
]
"""

varset = ['[%s]' % i for i in range(flagSZ)] + ['T', 'F']

depth_list = defaultdict(list)
class Node(object):
	def __init__(self, val, depth, parent):
		self.val = val if val is not None else random.choice(varset)
		self.depth = depth
		depth_list[depth].append(self)
		self.parent = parent
		self.child = [None, None]

	def getLeaves(self, leaves=None):
		if leaves is None:
			leaves = []
		for i, e in enumerate(self.child):
			if e: e.getLeaves(leaves)
			else: leaves.append((i, self))
		return leaves

	def born(self, i):
		self.child[i] = Node(None, self.depth + 1, self)
		return self.child[i]

	def grow(self, size):
		if size == 0:
			return self
		for i, c in enumerate(self.child):
			if c is None:
				return self.born(i).grow(size - 1)
		raise MemoryError('No available edge')

	def path(self):
		if self.parent is None:
			return []
		else:
			idx = self.parent.child.index(self)
			return self.parent.path() + [idx]

	def random_twist(self):
		random.shuffle(self.child)
		for c in self.child:
			if c is not None:
				c.random_twist()

	def __repr__(self):
		if use_pair:
			reprs = [repr(c) if c else random.choice(varset) for c in self.child]
			return f'(P {self.val} {reprs[1]} {reprs[0]})'
		else:
			# leaf (None) -> shift (A / B)
			# parent (Node) -> reduce (C / D)
			def rand_leaf_var():
				c = random.choice(varset)
				if c == 'F': return 'A'
				if c == 'T': return 'B'
				return 'A' + c
			reprs = [repr(c) if c else rand_leaf_var() for c in self.child]
			if self.val in 'FT':
				op = 'CD'['FT'.index(self.val)]
			else:
				op = f'C{self.val}'

			return f'{reprs[0]} {reprs[1]} {op}'



# Grow initial tree
primerSZ = 10
maxDepth = primerSZ * 2 - 1
root = Node(None, 0, None)
root.grow(maxDepth)
for i in range(len(tables) - 1):
	ok = False
	while not ok:
		d = random.randrange(1, maxDepth, 2)
		ns = depth_list[d][:]
		random.shuffle(ns)
		for n in ns:
			try:
				n.grow(maxDepth - d)
				ok = True
				break
			except MemoryError:
				continue

leafs = depth_list[len(depth_list)-1]
assert len(leafs) == len(tables)

# Add vals
separators = []
for table, n in zip(tables, leafs):
	state, i = set(), n
	while i is not None:
		state ^= set([i.val])
		i = i.parent.parent

	seps = []
	for row in table:
		state = list(state ^ set(varset[i] for i in row))
		random.shuffle(state)

		for v in state:
			n = n.born(0).born(0)
			n.val = v

		seps.append(n)
		state = set()
	separators.append(seps)
separators = separators[:-fakeSZ]

# Set op
root.random_twist()
for seps in separators:
	# xor op
	n = seps[-1]
	while n is not None:
		n.parent.val = 'TF'[n.parent.child.index(n)]
		n = n.parent.parent

	# and op
	for s in seps[:-1]:
		c = s.child[0] or s.child[1]
		c.child = c.child[::-1]

# Random branches
leaves = root.getLeaves()
for _ in range(randBranchNum):
	k = random.randrange(len(leaves))
	(i, e) = leaves.pop(k)
	c = e.born(i)
	c.grow(random.randrange(1, randBranchSZ))
	c.random_twist()

# Random leaves
leaves = root.getLeaves()
for _ in range(randLeafNum):
	k = random.randrange(len(leaves))
	(i, e) = leaves.pop(k)
	c = e.born(i)
	leaves.extend(c.getLeaves())

# Serialize tree
r = repr(root)
if not use_pair:
	r = '(A B A ' + r + ' T)'

# Replace placeholder
"""
inp = flag[:]
for i, v in enumerate(inp):
	if use_pair:
		r = r.replace(f'[{i}]', 'FT'[v])
	else:
		r = r.replace(f'C[{i}]', 'CD'[v])
		r = r.replace(f'A[{i}]', 'AB'[v])
"""

M = '(Y R T F ' + r + ')'

# Get paths
pathstr = []
for seps in separators:
	path = seps[-1].path()
	res = ['FT'[p] for p in path]
	res.append('T')
	pathstr.append('(M ' + ' '.join(res) + ' T E)')

I = ''
for i in range(0, len(pathstr), 3):
	I += '(' + ' '.join(pathstr[i:i+3]) + ') '
	if i != 0:
		I += 'F '
I = '(' + I + ')'

# print(M)
# print(I)

with open('tmpl') as f:
    out = f.read().strip()
out = out.replace('M', M)
out = out.replace('I', I)

fr = "REABTYFCDM"
to = "abcdefghij"
for f, t in zip(fr, to):
    out = out.replace(f, t)
if use_plam:
    out = out.replace('λ', '\\')
    out = out.replace('.\\', '')

with open('task.txt', 'w') as f:
    f.write(out + '\n')
