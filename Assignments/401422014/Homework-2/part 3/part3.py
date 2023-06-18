import sys

def floyd_warshall(N, graph):
    # Initialize the distance matrix with infinity values
    distances = [[float('inf')] * N for _ in range(N)]

    # Initialize the diagonal values as 0
    for i in range(N):
        distances[i][i] = 0

    # Fill in the distance matrix with the initial values
    for a, b, c in graph:
        distances[a-1][b-1] = min(distances[a-1][b-1], 2 ** c)
        distances[b-1][a-1] = min(distances[b-1][a-1], 2 ** c)

    # Perform the Floyd-Warshall algorithm
    for k in range(N):
        for i in range(N):
            for j in range(N):
                distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])

    return distances

# Read input
N, M = map(int, input().split())
graph = []
for _ in range(M):
    a, b, c = map(int, input().split())
    graph.append((a, b, c))

# Apply Floyd-Warshall algorithm
distances = floyd_warshall(N, graph)

# Find the sum of all distances
total_distance = sum(sum(row) for row in distances) // 2

# Print the sum of distances in binary form
binary_form = bin(total_distance)[2:]
print("Total distance (binary):", binary_form)