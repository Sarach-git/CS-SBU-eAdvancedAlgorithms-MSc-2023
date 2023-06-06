def min_distance(N, roads):
    dist = [[float('inf')] * N for _ in range(N)]

    for i in range(N):
        dist[i][i] = 0

    for road in roads:
        city1, city2, distance = road
        dist[city1 - 1][city2 - 1] = 2 ** distance
        dist[city2 - 1][city1 - 1] = 2 ** distance

    for k in range(N):
        for i in range(N):
            for j in range(N):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    print(dist)
    total_distance = sum(dist[i][j] for i in range(N) for j in range(i + 1, N))
    return total_distance


N, M = map(int, input().split())
roads_list = []
for _ in range(M):
    x, y, z = map(int, input().split())
    roads_list.append((x, y, z))

total_distance_decimal = min_distance(N, roads_list)
print(bin(total_distance_decimal)[2:])
