#MelikaAlikhaniRad #401422129
p = list(range(10 ** 5))

def d_get(v):
    if p[v] != v: p[v] = d_get(p[v])
    
    return p[v]

def d_merge(u, v):
    u = d_get(u)
    v = d_get(v)
    p[u] = v
    
    return u != v

n, m = map(int, input().split())
e = []
for i in range(m):
    a, b, c = map(int, input().split())
    e += [(c, b - 1, a - 1)]

e.sort()

G = [[] for x in range(n)]
for c, a, b in e:
    if d_merge(a, b):
        G[a] += [(b, c)]
        G[b] += [(a, c)]

f = [0] * m
def d(v, par = -1):
    sz = 1
    for u, c in G[v]:
        if u == par: continue
        
        y = d(u, v)
        
        f[c] = y * (n - y)
        sz += y
    
    return sz

d(0)

ans = 0
for x in f[::-1]:
    ans *= 2
    ans += x

print(bin(ans)[2:])
