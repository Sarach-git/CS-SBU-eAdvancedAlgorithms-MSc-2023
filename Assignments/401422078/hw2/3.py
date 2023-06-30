
class Graph():

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                    for row in range(vertices)] # Graph to Matrix


    def min_dist(self, dist, sp):

        # minimum distance for next node
        min = 99999999
        min_index = None
        for v in range(self.V):
            if dist[v] < min and sp[v] == False:
                min = dist[v]
                min_index = v

        return min_index

    # solving using Dijkstra
    def solve(self, src):

        dist = [99999999] * self.V
        dist[src] = 0
        sp = [False] * self.V

        for ct in range(self.V):

            # Pick the minimum distance vertex from not visited vertices
            u = self.min_dist(dist, sp)

            sp[u] = True

            # Update dist value of the adjacent vertices
            for v in range(self.V):
                if (self.graph[u][v] > 0 and
                sp[v] == False and
                dist[v] > dist[u] + self.graph[u][v]):
                    dist[v] = dist[u] + self.graph[u][v]

        return dist

# Driver program
n, m = input().split()
n, m = int(n), int(m)
g = Graph(n)
for i in range(m):
    a, b, c = input().split()
    a, b, c = int(a), int(b), int(c)
    g.graph[a-1][b-1] = 2 ** c
    g.graph[b-1][a-1] = 2 ** c

s = 0
for i in range(n):
    d = g.solve(i)
    for item in d[i:]:
        s += item

print(str(bin(s))[2:])