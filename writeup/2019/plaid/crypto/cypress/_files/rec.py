import numpy as np
from tqdm import tqdm, trange


def binary_tree_layout(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, 
                  pos = None, parent = None):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node of current branch
       width: horizontal space allocated for this branch - avoids overlap with other branches
       vert_gap: gap between levels of hierarchy
       vert_loc: vertical location of root
       xcenter: horizontal location of root
       pos: a dict saying where all nodes go if they have been assigned
       parent: parent of this branch.
       each node has an attribute "left: or "right"'''
    if pos == None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = list(G.neighbors(root))
    if parent != None:
        neighbors.remove(parent)
    if len(neighbors)!=0:
        dx = width/2.
        leftx = xcenter - dx/2
        rightx = xcenter + dx/2
        for neighbor in neighbors:
            if G.node[neighbor]['child_status'] == 'left':
                pos = binary_tree_layout(G,neighbor, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=leftx, pos=pos, 
                    parent = root)
            elif G.node[neighbor]['child_status'] == 'right':
                pos = binary_tree_layout(G,neighbor, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=rightx, pos=pos, 
                    parent = root)
    return pos


class Node:
    def __init__(self):
        self.tag = None
        self.parent = None
        self.child = [None, None]
        self.is_leaf = None
        self.is_placeholder = False
        self.count = 1

    def updateCount(self):
        self.count = sum(c.count if c else 0 for c in self.child) + 1

    def rotate(self):
        idx = (self.parent.child[1] != self) * 1
        child = self.child[idx]
        self.parent.child[1 - idx] = child
        if child:
            child.parent = self.parent
        self.child[idx] = self.parent
        self.parent.updateCount()
        self.updateCount()

        grandpa = self.parent.parent
        self.parent.parent = self
        if grandpa:
            grandpa.child[1 - idx] = self
        self.parent = grandpa

    def splay(self):
        while True:
            parent = self.parent
            if not parent:
                return self
            grandpa = parent.parent
            if not grandpa:
                self.rotate()
                return self
            if (grandpa.parent and
               (parent.child[1] == self) == (grandpa.child[1] == parent)):
                parent.rotate()
            else:
                self.rotate()

            self.rotate()

    def twist(self):
        parent = self.parent
        cur = self
        ret = []
        while parent:
            left = parent.child[0]
            bit = left != cur
            if bit:
                parent.child = parent.child[::-1]
            ret.append(bit * 1)
            cur = parent
            parent = parent.parent
        self.parent.splay()
        return self.parent, ret[::-1]
            
    def _render(self, G, child_status='left'):
        G.add_node(id(self),
                   node=self,
                   child_status=child_status,
                   )
        left, right = self.child
        if left:
            left._render(G, 'left')
            G.add_edge(id(self), id(left))
        if right:
            right._render(G, 'right')
            G.add_edge(id(self), id(right))

    def render(self):
        import networkx as nx
        G = nx.Graph()
        self._render(G)
        pos = binary_tree_layout(G, id(self))
        labels = {}
        colors = []
        for nodeid in G:
            node = G.node[nodeid]['node']
            labels[nodeid] = node.tag or ''
            # labels[nodeid] = str(node.count) or ''
            if node.is_placeholder:
                colors.append('green')
            elif node.is_leaf == True:
                colors.append('red')
            elif node.is_leaf == False:
                colors.append('gray')
            elif node.is_leaf == None:
                colors.append('blue')
        nx.draw(G, pos=pos, node_color=colors, labels=labels, with_labels = True)
        return G

    def clone(self, parent=None):
        this = Node()
        this.tag = self.tag
        this.count = self.count
        this.is_leaf = self.is_leaf
        this.is_placeholder = self.is_placeholder
        this.parent = parent
        this.child = [c.clone(this) if c else None for c in self.child]
        return this

    def get(self, path):
        cur = self
        for d in path:
            cur = cur.child[d]
            if not cur:
                raise FileNotFoundError('Not Found')
        return cur


def grow(path, tag=None):
    root = Node()
    parent = root
    size = len(path) + 1
    placeholders = []
    for idx, d in enumerate(path):
        parent.is_leaf = False
        parent.count = size - idx
        child = Node()
        placeholder = Node()
        placeholder.is_placeholder = True
        placeholder.tag = str(idx)
        placeholder.count = 0
        placeholders.append(placeholder)
        parent.child[d] = child
        parent.child[1 - d] = placeholder
        child.parent = parent
        placeholder.parent = parent
        parent = child
    child.is_leaf = True
    child.tag = tag
    return root, child, placeholders


def merge(A, B, mapping):
    if A.is_placeholder:
        mapping[int(A.tag)] = B
        return
    if B is None:
        return
    assert A.is_leaf is not None
    assert B.is_leaf is not None
    if A.is_leaf != B.is_leaf:
        raise EnvironmentError('Incompatible structure')
    if B.is_placeholder:
        return
    if A.is_leaf:
        if A.tag is not None and B.tag is not None and A.tag != B.tag:
            raise EnvironmentError('Incompatible tag')
        return
    for A, B in zip(A.child, B.child):
        merge(A, B, mapping)


def init_state():
    root = Node()
    root.is_leaf = False
    left = Node()
    left.is_placeholder = True
    left.is_leaf = True
    right = Node()
    right.is_leaf = False
    rright = Node()
    rright.is_placeholder = True
    rright.is_leaf = True
    rright.parent = right
    right.child[1] = rright
    left.parent = root
    right.parent = root
    root.child = [left, right]
    return root


def inverse(state, leaves, path, tag):
    if state:
        node = state.get([0])
        if not tag:
            tag = node.tag
        ttag = tag if tag in leaves else None
        if node.tag != ttag:
            raise EnvironmentError('Incompatible existed tag')
    leaves = leaves.copy()
    leaves[tag] = 1
    before, _, bph = grow(path, tag)
    _, leaf, aph = grow(path, tag)
    after, _ = leaf.twist()
    mapping = {}
    merge(after, state, mapping)
    for i, p in enumerate(bph):
        idx = p.parent.child.index(p)
        r = mapping.get(i)
        if r:
            r = r.clone()
            p.parent.child[idx] = r
            r.parent = p.parent
            while p.parent:
                p.parent.updateCount()
                p = p.parent
        else:
            p.parent.child[idx] = None
    if not before.child[1]:
        n = Node()
        n.is_leaf = False
        n.parent = before
        before.child[1] = n
        before.updateCount()
    else:
        n = before.child[1]
    if not n.child[1]:
        ph = Node()
        ph.is_placeholder = True
        ph.is_leaf = True
        n.child[1] = ph
        ph.parent = n
        n.updateCount()
        before.updateCount()

    if before.count > 511:
        raise EnvironmentError('Too many nodes')
    
    return before, leaves
    
    
def init_tree():
    arr = [Node() for _ in range(511)]
    parent = 0
    child = 1
    while child < 511:
        p = arr[parent]
        left = arr[child]
        right = arr[child + 1]
        p.child = [left, right]
        left.parent = p
        right.parent = p
        parent += 1
        child += 2
    for i, n in enumerate(arr[:255]):
        n.is_leaf = False
    for i, n in enumerate(arr[:255][::-1]):
        n.updateCount()
    for i, n in enumerate(arr[255:]):
        n.tag = i
        n.is_leaf = True
    leaf = arr[255:]
    return arr[0], leaf


def F(root, leaf, i):
    root, ret = leaf[i].twist()
    return root, ret


def enc(key, plain):
    root, leaf = init_tree()
    for c in key:
        root, _cipher = F(root, leaf, c)

    cipher = []
    for c in plain:
        root, _cipher = F(root, leaf, c)
        cipher.append(_cipher)
    size = sum(map(len, cipher)) + 1
    cipher.append([1] + [0] * (-size % 8))
    cstr = ''.join(''.join(map(str, cs)) for cs in cipher)
    cstr = int(cstr, 2).to_bytes(len(cstr) // 8, 'big')
    return cstr, cipher, root


lenMean = np.load('./lenMean.npy')[::-1]
lenStd = np.load('./lenStd.npy')[::-1]
lenMax = 40
with open('len8.table') as f:
    len8 = [l[:-1][::-1] for l in f]
    len8 = dict.fromkeys(len8)
with open('pin.txt') as f:
    pin = [l[:-1][::-1] for l in f][::-1]
with open('chars.txt') as f:
    chars = [l[:-1] for l in f][::-1]
    
with open('secrets.zip.enc', 'rb') as f:
    secret = f.read()
    assert secret[:4] == b'SPLD'
    secret = ''.join(bin(c)[2:].rjust(8, '0') for c in secret[4:-4])
    secret = secret.rstrip('0')[:-1][::-1]


def genseg(inp, off, idx, tol=6):
    if idx < len(lenMean):
        mean = lenMean[idx]
        std = lenStd[idx]
    else:
        return [] # overflow
        mean = 13.385
        std = 10
    inp = inp[off:]
    if std == 0:
        size = int(round(mean))
        s = inp[:size]
        if size < 8 and s not in len8:
            return []
        if pin[idx] != '' and s != pin[idx]:
            return []
        return [size]
    segs = []
    start = max(int(round(mean - tol * std)), 1)
    end = min(int(round(mean + tol * std)), lenMax, len(inp))
    for sz in range(start, end):
        if sz < 8:
            s = inp[:sz]
            if s in len8:
                segs.append(sz)
        else:
            s = inp[:sz]
            if s.endswith('001') or s.endswith('101'):
                segs.append(sz)
    segs = sorted(segs, key=lambda s: -abs(s - mean))
    return segs


def step(state, s, idx):
    state, leaves = state
    tag = None
    if idx < len(chars):
        tag = chars[idx] or None
    s = list(map(int, s))
    state, leaves = inverse(state, leaves, s, tag)
    return state, leaves


def dfs(inp, idxoff=0, state=(init_state(), {}), iters=1000, out={}):
    stack = [(state, 0, genseg(inp, 0, idxoff, 10 if state[0].count >= 200 else 4))]
    ans = [0] * 10000
    print(stack)
    moff = 0
    bar = trange(iters)
    try:
        for qq in bar:
            if qq & 65535 == 0:
                print('')
                print(ans[:len(stack)])
                print('')
            idx = len(stack) - 1
            state, off, segs = stack[-1]
            if off >= len(inp):
                break
            if moff < off:
                moff = off
                out['ans'] = ans[:len(stack)]
            if qq & 127 == 0:
                bar.desc = f'{len(stack)} - {state[0].count} - {off} - {moff}'
            if len(segs) == 0:
                stack.pop()
                continue
            size = segs.pop()
            ans[idx] = size
            if off + size >= len(inp):
                continue
            try:
                state = step(state, inp[off:][:size][::-1], idx + idxoff)
            except EnvironmentError:
                continue
            off += size 
            try:
                segs = genseg(inp, off, idx + idxoff + 1, 10 if state[0].count >= 200 else 4)
            except EnvironmentError:
                continue
            stack.append((state, off, segs))
    finally:
        bar.close()
    return ans[:len(stack)]


"""
# Test the implementation of encrypt function

if __name__ == '__main__':
    with open('inp', 'rb') as f:
        inp = f.read()
    cstr, cipher, root = enc(b'tLBeLbbkuUj6IV9Me6DUb21+j+RQvN9O02NAimKv', inp)
    with open('out', 'rb') as f:
        out = f.read()[4:-4]
    assert cstr == out
"""


"""
# Recover the flag


In [10]: out = {}
# The best plaintext is stored in out['ans']
In [11]: ans = dfs(secret, iters=10000000, out=out)
^C
In [12]: ans = out['ans']

In [51]: bits0, off = [], 0
    ...: for i in ans:
    ...:     bits0.append(secret[off:][:i])
    ...:     off += i
    ...:

In [51]: state = init_state()
    ...: leaves = {}
    ...: for i, (c, p) in enumerate(itertools.zip_longest(bits0, chars)):
    ...:     print(i)
    ...:     p = p or None
    ...:     c = list(map(int, c[::-1]))
    ...:     state, leaves = inverse(state, leaves, c, p)

In [51]: s = state.clone()
    ...: plain = []
    ...: for i, c in enumerate(bits0[::-1]):
    ...:     c = list(map(int, c[::-1]))
    ...:     n = s.get(c)
    ...:     plain.append(n.tag)
    ...:     s, z = n.twist()
    ...:     print(n.is_leaf)
    ...:     print(i)
"""
