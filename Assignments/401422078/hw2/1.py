max_size = 3000
	
dp = [[0 for i in range(max_size)] for j in range(max_size)]

left_piece_is_taken = [[False for i in range(max_size)] for j in range(max_size)]

# Function to calculate the maximum value
def max_scr(value):
	n = len(value)
	total_turns = n

	turn = 0 if (total_turns % 2 == 0) else 1

	# if piece is picked by P1 add it to the ans
	for i in range(n):
		dp[i][i] = value[i] if turn else 0
		left_piece_is_taken[i][i] = 1

	turn = not turn

	# s represents the size of the state dp(i, i+sz)
	s = 1

	while s < n:
		i = 0
		while i + s < n:
			scr_one = dp[i + 1][i + s]
			scr_two = dp[i][i + s - 1]

			# First player
			if turn:
				dp[i][i + s] = max(value[i] + scr_one, value[i + s] + scr_two)

				# if leftBag has more profit
				if (value[i] + scr_one > value[i + s] + scr_two):
					left_piece_is_taken[i][i + s] = 1
				else:
					left_piece_is_taken[i][i + s] = 0

			# second player
			else:
				dp[i][i + s] = min(scr_one, scr_two)

				if (scr_one < scr_two):
					left_piece_is_taken[i][i + s] = 1
				else:
					left_piece_is_taken[i][i + s] = 0
			i += 1

		# Give turn to other player
		turn = not turn
		s += 1

	return dp[0][n - 1]

# generate the actual game
def get_best_moves(n):
	moves = ""
	left, right = 0, n - 1

	while (left <= right):
		# if the piece is picked from left
		if (left_piece_is_taken[left][right]):
			moves = moves + 'L'
			left += 1
		else:
			moves = moves + 'R'
			right -= 1
	return moves


pices = list(map(int, input().split()))
n = len(pices)
ans = max_scr(pices)

print(ans, get_best_moves(n), sep=" ")