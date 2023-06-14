# Function to calculate the maximum score
def maxScore(dies):
    n = len(dies)
    totalTurns = n
    turn = 0 if totalTurns % 2 == 0 else 1

    # Fill the base cases in the best_score table
    for i in range(n):
        best_score[i][i] = dies[i] if turn else 0
        leftdie[i][i] = 1

    turn = not turn
    sz = 1

    while sz < n:
        i = 0
        while i + sz < n:
            scoreOne = best_score[i + 1][i + sz]
            scoreTwo = best_score[i][i + sz - 1]

            if turn:
                # Player 1's turn
                best_score[i][i + sz] = max(dies[i] + scoreOne, dies[i + sz] + scoreTwo)
                leftdie[i][i + sz] = dies[i] + scoreOne > dies[i + sz] + scoreTwo
            else:
                # Player 2's turn
                best_score[i][i + sz] = min(scoreOne, scoreTwo)
                leftdie[i][i + sz] = scoreOne < scoreTwo

            i += 1

        turn = not turn
        sz += 1

    return best_score[0][n - 1]


# Function to generate the game moves
def getMoves(n):
    moves = ""
    left, right = 0, n - 1

    while left <= right:
        if leftdie[left][right]:
            moves += 'L'  # Pick the leftmost die
            left += 1
        else:
            moves += 'R'  # Pick the rightmost die
            right -= 1

    return moves


# Take input from the user
dies_input = input()
dies = list(map(int, dies_input.split()))

arraySize = len(dies)

# Initialize the best_score and leftdie tables
best_score = [[0 for _ in range(arraySize)] for _ in range(arraySize)]
leftdie = [[False for _ in range(arraySize)] for _ in range(arraySize)]

# Calculate the maximum score and optimal moves
max_score = maxScore(dies)
optimal_moves = getMoves(arraySize)

# Print the results
print( max_score , optimal_moves)
