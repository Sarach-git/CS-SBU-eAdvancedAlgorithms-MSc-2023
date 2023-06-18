def optimalStrategyOfGame(arr, n):
    move_table = [["" for i in range(n)] for i in range(n)]
    table = [[0 for i in range(n)] for i in range(n)]
    for gap in range(n):
        for j in range(gap, n):
            i = j - gap
            x = 0
            if ((i + 2) <= j):
                x = table[i + 2][j]
            y = 0
            if ((i + 1) <= (j - 1)):
                y = table[i + 1][j - 1]
            z = 0
            if (i <= (j - 2)):
                z = table[i][j - 2]

            if (arr[i] + min(x, y)) > (arr[j] + min(y, z)):
                table[i][j] = arr[i] + min(x, y)
                move_table[i][j] = "R"
            else:
                table[i][j] = arr[j] + min(y, z)
                move_table[i][j] = "L"
    moves = str(move_table[0]).replace(',', '').replace("'", "").replace(']', '').replace('[', '').replace(' ', '')
    return table[0][n - 1], moves


arr1 = [10, 80, 90, 30]
n = len(arr1)
result, moves = optimalStrategyOfGame(arr1, n)
print(result, end=" ")
print(moves[::-1])
