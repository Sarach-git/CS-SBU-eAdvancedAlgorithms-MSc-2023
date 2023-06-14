import sys

def calculate_minimum_distances(N, M, roads):
    # Initialize the distance matrix with maximum distances
    distances = [[sys.maxsize] * N for _ in range(N)]

    # Set the diagonal elements to 0
    for i in range(N):
        distances[i][i] = 0

    # Update the distances using the given road lengths
    for a, b, c in roads:
        a -= 1  # Adjust city indices to 0-based
        b -= 1
        distance = 2 ** c
        distances[a][b] = min(distances[a][b], distance)
        distances[b][a] = min(distances[b][a], distance)

    # Perform Floyd-Warshall algorithm to find the minimum distances
    for k in range(N):
        for i in range(N):
            for j in range(N):
                distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])

    # Calculate the sum of all minimum distances
    total_distance = sum(sum(row) for row in distances)

    # Convert the total distance to binary representation
    binary_distance = bin(total_distance)[2:]

    return binary_distance

# Read the input
N, M = map(int, input().split())
roads = []
for _ in range(M):
    a, b, c = map(int, input().split())
    roads.append((a, b, c))

# Calculate the minimum distances and print the output
output = calculate_minimum_distances(N, M, roads)
print(output)
