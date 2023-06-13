def min_distance(n, roads):
    # Create array
    min_dist = [[float('inf')] * n for _ in range(n)]

    # Set the diagonal elements to 0
    for i in range(n):
        min_dist[i][i] = 0

    # Iterate over the roads
    for road in roads:
        c1, c2, distance = road
        min_dist[c1 - 1][c2 -
                         1] = min(min_dist[c1 - 1][c2 - 1], 2 ** distance)
        min_dist[c2 - 1][c1 -
                         1] = min(min_dist[c2 - 1][c1 - 1], 2 ** distance)

    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                min_dist[i][j] = min(
                    min_dist[i][j], min_dist[i][k] + min_dist[k][j])

    # Calculate total distance
    total_distance = sum(min_dist[i][j]
                         for i in range(n) for j in range(i + 1, n))
    return total_distance


N, M = map(int, input().split())
roads_list = []

for i in range(M):
    x, y, z = map(int, input().split())
    roads_list.append((x, y, z))

total_distance_decimal = min_distance(N, roads_list)
print(bin(total_distance_decimal)[2:])
