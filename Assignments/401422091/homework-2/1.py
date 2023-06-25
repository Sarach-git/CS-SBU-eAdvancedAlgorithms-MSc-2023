def optimal_path_finder(input_list):
    input_length = len(input_list)
    dp = [[0] * input_length for _ in range(input_length)]
    for slot in range(input_length):
        for j in range(slot, input_length):
            i = j - slot
            x = dp[i + 2][j] if (i + 2) <= j else 0
            y = dp[i + 1][j - 1] if (i + 1) <= (j - 1) else 0
            z = dp[i][j - 2] if i <= (j - 2) else 0
            dp[i][j] = max(input_list[i] + min(x, y), input_list[j] + min(y, z))

    moves = ''
    i = 0
    j = input_length - 1
    while i <= j:
        if input_list[i] + min(dp[i + 2][j] if (i + 2) <= j else 0, dp[i + 1][j - 1] if (i + 1) <= (j - 1) else 0) > \
                input_list[j] + min(dp[i + 1][j - 1] if (i + 1) <= (j - 1) else 0, dp[i][j - 2] if i <= (j - 2) else 0):
            moves += 'L'
            i += 1
        else:
            moves += 'R'
            j -= 1
    return dp[0][input_length - 1], moves


input_list_from_user = list(map(int, input().split()))
answer = optimal_path_finder(input_list_from_user)
print(answer[0], answer[1])
