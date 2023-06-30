#MelikaAlikhaniRad #401422129
maxSize = 3000
	
# d(i, j) is the best

d = [[0 for i in range(maxSize)] for j in range(maxSize)]

leftBag = [[False for i in range(maxSize)] for j in range(maxSize)]

# Function to calculate the maximum
def maxScore(money):
	# we will fill the d table
	# in a bottom-up manner. fill
	# all states that represent
	# lesser number of bags before
	# filling states that represent
	# higher number of bags.
	# we start from states d(i, i)
	# as these are the base case of
	# our DP solution.
	n = len(money)
	totalTurns = n
	turn = 0 if (totalTurns % 2 == 0) else 1
	for i in range(n):
		d[i][i] = money[i] if turn else 0
		leftBag[i][i] = 1

	turn = not turn
	z = 1

	while z < n:
		i = 0
		while i + z < n:
			scoreOne = d[i + 1][i + z]
			scoreTwo = d[i][i + z - 1]

			# First player
			if turn:
				d[i][i + z] = max(money[i] + scoreOne, money[i + sz] + scoreTwo)

				# if leftBag has more profit
				if (money[i] + scoreOne > money[i + z] + scoreTwo):
					leftBag[i][i + z] = 1
				else:
					leftBag[i][i + z] = 0

			# second player
			else:
				d[i][i + z] = min(scoreOne, scoreTwo)

				if (scoreOne < scoreTwo):
					leftBag[i][i + z] = 1
				else:
					leftBag[i][i + z] = 0
			i += 1

		# Give turn to the
		# other player.
		turn = not turn

		z += 1

	return d[0][n - 1]

def getMoves(n):
	moves = ""
	left, right = 0, n - 1

	while (left <= right):
		# if the bag is picked from left
		if (leftBag[left][right]):
			moves = moves + 'L'
			left += 1
		else:
		moves = moves + 'R'
		right -= 1
	return moves

ar = [ 10, 80, 90, 30 ]
arraySize = len(ar)

bags = ar
ans = maxScore(bags)

print(ans, getMoves(len(bags)), sep=" ")


