def max_score(marbles):
    n = len(marbles)
    dp = [[0] * n for _ in range(n)]  # Dynamic programming table to store maximum scores
    moves = [[''] * n for _ in range(n)]  # Table to store the optimal moves

    for i in range(n):
        dp[i][i] = marbles[i]  # Base case: score of choosing the only remaining marble
        moves[i][i] = 'R'  # Base case: move of choosing the only remaining marble is 'R'

    for length in range(2, n + 1):  # Iterate over different lengths of marbles
        for i in range(n - length + 1):  # Iterate over starting indices
            j = i + length - 1  # Calculate ending index
            if marbles[i] + dp[i + 1][j] > marbles[j] + dp[i][j - 1]:
                # If choosing the first marble yields a higher score
                dp[i][j] = marbles[i] + dp[i + 1][j]
                moves[i][j] = 'R' + moves[i + 1][j]  # Update optimal moves
            else:
                # If choosing the last marble yields a higher score
                dp[i][j] = marbles[j] + dp[i][j - 1]
                moves[i][j] = 'L' + moves[i][j - 1]  # Update optimal moves

    max_score = dp[0][n - 1]  # Maximum score achievable
    moves = moves[0][n - 1]  # Optimal sequence of moves

    return max_score, moves


# Read input marbles from the user
marbles = list(map(int, input().split()))

# Call the max_score function to get the maximum score and optimal moves
max_score, moves = max_score(marbles)

# Print the maximum score and optimal moves
print(max_score, moves)
