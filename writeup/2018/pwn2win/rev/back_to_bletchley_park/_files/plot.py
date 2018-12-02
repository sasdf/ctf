import pickle
from graphviz import Digraph

dot = Digraph(format='svg')

with open('dep2.pkl', 'rb') as f:
    dep = pickle.load(f)

entry = 'sqgate_3858'
print(len(dep[entry]))
print(dep[entry])

print('[*] Building graph')

visited = {}
def dfs(n, p):
    if n in visited:
        dot.edge(p, n)
        return
    visited[n] = 1
    dot.node(n)
    if p is not None:
        dot.edge(p, n)
    if n not in dep:
        return
    for t in dep[n]:
        dfs(t, n)

dfs(entry, None)

print(list(visited.keys()))

print('[*] Rendering')

dot.render('graph.gv')
