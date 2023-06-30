die_numbers = 1000

# best_score(i, j) is the best score possible if only the dies from i, j were present.
best_score = [[0 for i in range(die_numbers)] for j in range(die_numbers)]

# leftdie(i, j) is 1 if in the optimal game the player picks the leftmost die when only the dies from i to j are present.
leftdie = [[False for i in range(die_numbers)] for j in range(die_numbers)]

# Function to calculate the maximum value


def maxScore(dies):
    # we will fill the best_score table
    # in a bottom-up manner. fill
    # all states that represent
    # lesser number of dies before
    # filling states that represent
    # higher number of dies.
    # we start from states best_score(i, i)
    # as these are the base case of
    # our best_score solution.
    n = len(dies)
    totalTurns = n

    # turn = 1 if it is player 1's
    # turn else 0. Who gets to pick
    # the last die(bottom-up so we
    # start from last turn)
    turn = 0 if (totalTurns % 2 == 0) else 1

    # if die is picked by P1 add it
    # to the ans else 0 contribution
    # to score.
    for i in range(n):
        best_score[i][i] = dies[i] if turn else 0
        leftdie[i][i] = 1

    # 2nd last die is picked by
    # the other player.
    turn = not turn

    # sz represents the size
    # or number of dies in
    # the state best_score(i, i+sz)
    sz = 1

    while sz < n:
        i = 0
        while i + sz < n:
            scoreOne = best_score[i + 1][i + sz]
            scoreTwo = best_score[i][i + sz - 1]

            # First player
            if turn:
                best_score[i][i + sz] = max(dies[i] + scoreOne,
                                            dies[i + sz] + scoreTwo)

                # if leftdie has more profit
                if (dies[i] + scoreOne > dies[i + sz] + scoreTwo):
                    leftdie[i][i + sz] = 1
                else:
                    leftdie[i][i + sz] = 0

            # second player
            else:
                best_score[i][i + sz] = min(scoreOne, scoreTwo)

                if (scoreOne < scoreTwo):
                    leftdie[i][i + sz] = 1
                else:
                    leftdie[i][i + sz] = 0
            i += 1

        # Give turn to the
        # other player.
        turn = not turn

        # Now fill states
        # with more dies.
        sz += 1

    return best_score[0][n - 1]

# Using the leftdie matrix,
# generate the actual game
# moves that lead to the score.


def getMoves(n):
    moves = ""
    left, right = 0, n - 1

    while (left <= right):
        # if the die is picked from left
        if (leftdie[left][right]):
            moves = moves + 'L'
            left += 1
        else:
            moves = moves + 'R'
            right -= 1
    return moves


ar = [10, 80, 90, 30]
arraySize = len(ar)

dies = ar
ans = maxScore(dies)

print(ans, getMoves(len(dies)), sep=" ")

ar = [20, 3, 10, 48]
arraySize = len(ar)

dies = ar
ans = maxScore(dies)

print(ans, getMoves(len(dies)), sep=" ")
