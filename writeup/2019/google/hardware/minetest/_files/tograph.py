import pickle
import networkx as nx
from collections import Counter


with open('blocks.pkl', 'rb') as f:
    blocks = pickle.load(f)


edges = []
nodes = []

"""
insulated @ 0: ---
                 .
cross_over @ 0: ---
                 '
corner @ 0: --.
              |
gate @ 0: =>-

tjunction @ 0: T

clock-wise rotate
"""

print('build graph')
for (x, z, y), (name, rot) in blocks.items():
    assert z == 2
    # print(x, y, name, rot)
    if 'insulated' in name:
        if rot == 0 or rot == 2:
            edges.append(((x-0.5, y), (x+0.5, y)))
        elif rot == 1 or rot == 3:
            edges.append(((x, y-0.5), (x, y+0.5)))
    elif 'crossover' in name:
        edges.append(((x-0.5, y), (x+0.5, y)))
        edges.append(((x, y-0.5), (x, y+0.5)))
    elif 'corner' in name:
        if rot == 0:
            edges.append(((x-0.5, y), (x, y-0.5)))
        elif rot == 1:
            edges.append(((x-0.5, y), (x, y+0.5)))
        elif rot == 2:
            edges.append(((x+0.5, y), (x, y+0.5)))
        elif rot == 3:
            edges.append(((x+0.5, y), (x, y-0.5)))
    elif 'tjunction' in name:
        if rot == 0 or rot == 2:
            edges.append(((x-0.5, y), (x+0.5, y)))
        elif rot == 1 or rot == 3:
            edges.append(((x, y-0.5), (x, y+0.5)))

        if rot == 0:
            edges.append(((x-0.5, y), (x, y-0.5)))
        elif rot == 1:
            edges.append(((x-0.5, y), (x, y+0.5)))
        elif rot == 2:
            edges.append(((x+0.5, y), (x, y+0.5)))
        elif rot == 3:
            edges.append(((x+0.5, y), (x, y-0.5)))
    elif 'not' in name:
        assert rot == 3
        nodes.append(('not', (x, y+0.5), [(x-0.5, y), (x, y-0.5), (x+0.5, y)]))
        pass
    elif 'xor' in name:
        assert rot == 3
        nodes.append(('xor', (x, y+0.5), [(x-0.5, y), (x, y-0.5), (x+0.5, y)]))
        pass
    elif 'and' in name:
        assert rot == 3
        nodes.append(('and', (x, y+0.5), [(x-0.5, y), (x, y-0.5), (x+0.5, y)]))
        pass
    elif 'or' in name:
        assert rot == 3
        nodes.append(('or', (x, y+0.5), [(x-0.5, y), (x, y-0.5), (x+0.5, y)]))
        pass
    elif 'lamp' in name:
        nodes.append(('lamp', None, [(x, y+0.5), (x-0.5, y), (x, y-0.5), (x+0.5, y)]))
        pass
    elif 'lever' in name:
        assert rot == 0
        nodes.append(('lever_%s' % (x), (x, y+0.5), []))
        pass
    else:
        print(name)
        raise ValueError('WTF name')

print('add edges')
g = nx.Graph()
g.add_edges_from(edges)

print('add nodes')
ns = [out for name, out, inp in nodes if out is not None]
ns += [e for name, out, inp in nodes for e in inp]
g.add_nodes_from(ns)

print('simplify edges')
ccs = list(nx.connected_components(g))
ccmap = {}
for i, cc in enumerate(ccs):
    for e in cc:
        ccmap[e] = i

nodes2 = []
for name, out, inp in nodes:
    inp = [ccmap.get(e) for e in inp]
    inp = [e for e in inp if e is not None]
    out = ccmap.get(out)
    nodes2.append((name, out, inp))

print('remove unconnected edges')
edge_ctr = Counter()
for name, out, inp in nodes2:
    edge_ctr.update([out])
    edge_ctr.update(inp)

edge_ctr[None] = 0
del edge_ctr[None]

edge_map = {}
for edge, cnt in edge_ctr.items():
    if cnt >= 2:
        edge_map[edge] = len(edge_map)

nodes3 = []
for name, out, inp in nodes2:
    inp = [edge_map.get(e) for e in inp]
    inp = [e for e in inp if e is not None]
    out = edge_map.get(out)
    nodes3.append((name, out, inp))


print('topological sort')
G = nx.DiGraph()
for name, out, inp in nodes3:
    G.add_node(str(out), name=name)
    
for name, out, inp in nodes3:
    for i in inp:
        G.add_edge(str(i), str(out))

z = list(nx.topological_sort(G))
z.pop(-1)
z = list(map(int, z))
        
levers = []
for name, out, inp in nodes3:
    if 'lever' in name:
        levers.append((name, out))
        
levers = sorted(levers, key=lambda x: int(x[0].split('_')[1]))
for name, i in levers:
    z.remove(i)
    
z = [i for name, i in levers] + z

zz = {e: i for i, e in enumerate(z)}
nodes4 = []
for name, out, inp in nodes3:
    inp = [zz.get(i) for i in inp]
    out = zz.get(out)
    nodes4.append((name, out, inp))
    
nodes5 = sorted(nodes4, key=lambda x: x[1] if x[1] is not None else 10000000)
