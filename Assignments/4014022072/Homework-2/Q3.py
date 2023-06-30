INF = float('inf')


def floyd_warshall(N, M, edges):
    # initialize the adjacency matrix with infinite values
    adj_mat = [[INF] * N for _ in range(N)]

    # set diagonal elements to zero
    for i in range(N):
        adj_mat[i][i] = 0

    # populate the adjacency matrix with edge weights
    for a, b, c in edges:
        adj_mat[a - 1][b - 1] = 2 ** c
        adj_mat[b - 1][a - 1] = 2 ** c

    # run the Floyd-Warshall algorithm
    for k in range(N):
        for i in range(N):
            for j in range(N):
                adj_mat[i][j] = min(adj_mat[i][j], adj_mat[i][k] + adj_mat[k][j])

    # compute the sum of all distances
    total_dist = int(sum(sum(row) for row in adj_mat) / 2)

    # print the sum in base 2
    print(bin(total_dist))


# example usage
print("Enter M&N and enter the city of origin and destination and distance according to the problem in each next line:")
# example :
# 5 6
# 1 3 5
# 4 5 0
# 2 1 3
# 3 2 1
# 4 3 4
# 4 2 2

N, M = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(M)]
floyd_warshall(N, M, edges)
