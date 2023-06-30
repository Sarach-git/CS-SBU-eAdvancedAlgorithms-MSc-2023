def optimalGame(beads):
    n = len(beads)

    # Initialize the dp table with zeros
    dp = [[0] * n for _ in range(n)]

    # Initialize the moves table with empty strings
    moves = [[''] * n for _ in range(n)]

    # Fill the diagonal elements of dp table with the bead scores
    for i in range(n):
        dp[i][i] = beads[i]
        moves[i][i] = 'L'  # Player chooses the leftmost bead

    # Fill the remaining elements of the dp table diagonally
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            # If the first player chooses the leftmost bead
            left_score = beads[i] + min(dp[i + 2][j] if i + 2 <= j else 0, dp[i + 1][j - 1] if i + 1 <= j - 1 else 0)
            right_score = beads[j] + min(dp[i][j - 2] if i <= j - 2 else 0, dp[i + 1][j - 1] if i + 1 <= j - 1 else 0)

            if left_score > right_score:
                dp[i][j] = left_score
                moves[i][j] = 'L'
            else:
                dp[i][j] = right_score
                moves[i][j] = 'R'

    # Print the maximum possible score and the sequence of movements
    print(dp[0][n - 1], getMoves(beads, moves))


def getMoves(beads, moves):
    n = len(beads)
    i, j = 0, n - 1
    sequence = ''

    while i <= j:
        move = moves[i][j]
        sequence += move

        if move == 'L':
            i += 1
        else:
            j -= 1

    return sequence


# Get input for the scores of the beads
beads_input = input()
beads = list(map(int, beads_input.split()))

# Call the optimalGame function with the user input
optimalGame(beads)