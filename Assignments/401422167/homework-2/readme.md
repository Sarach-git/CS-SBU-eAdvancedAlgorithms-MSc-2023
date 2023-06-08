# Homework 1

## 1

### 1.1

Let `best(v) -> a, s` be a function that takes the vector of coin
values `v` and returns the most possible amount of points earned
by the first player `a` with the sequence of moves `s`.

We have the brute-force algorithm in [1.1.py](1.1.py) to calculate
the `best` function.

Let the time consumed to run this algorithm for an input of length
`n` be `t(n)`, then we know that `t(n) = 2 * t(n - 1)`, and
`t(0) = 1`. We can conclude that `t(n) = 2 ^ n`, which is
exponential.

### 1.2

We can improve the given algorithm by pruning away branches that
are guaranteed to be suboptimal, reducing the number of evaluations
and improving efficiency.

1. When it's the first player's turn, we check if the current score 
is greater than the current `p1_max`. If it is, the `p1_max` is
updated to the new score. This represents the best score found so
far for the first player.

2. At the same level, when it's the second player's turn, we check
if the current score is less than the current `p2_min` value. If it
is, the `p2_min` is updated to the new score. This represents the 
worst score found so far for the second player.

3. At any level, if the `p1_max` becomes greater than or equal to
the `p2_min` value, it means that the subtree rooted at the current
position will never be reached in the actual gameplay because there
exists a better move that has already been evaluated. Therefore, the
algorithm can safely prune the remaining branches of that subtree
and stop evaluating further.

### 1.3

The original algorthim is of `O(2 ^ n)`. However, the pruning
technique reduces the number of recursive calls needed by
eliminating branches that are guaranteed to be suboptimal. By
pruning away certain branches, the algorithm avoids evaluating
all `2 ^ n` possible moves, significantly reducing the number of 
function calls.

Considering the worst case scenario where no pruning occurs, the
time complexity is `O(2 ^ n)`. However, in practice, the pruning can
greatly reduce the number of function calls, resulting in a
significant improvement in the actual running time of the algorithm.

Therefore, while the worst case time complexity is `O(2 ^ n)`, the
average case time complexity is much better, typically closer to
`O(n ^ 2)` due to the effectiveness of pruning.

### 1.4

The implementation can be found in [1.4.py](1.4.py).

## 2

We have to assume the availability of a gas station within the
remaining fuel range at each step.

The greedy algorithm would be as follows.

1. Start at the initial city with a full tank of fuel.
2. Determine the farthest gas station from the current position,
within the remaining fuel range. 
3. Drive to the gas station determined in step 2. 
4. Refuel the car at that gas station to the maximum capacity. 
5. Repeat steps 2-4 until you reach the destination city.

We can prove that this algorithm, leads to the optimal solution.

- Let `n` be the fuel capacity of the car.
- Let `d[i]` represent the distance between the starting city and 
the `i`-th gas station.
- The greedy algorithm would, at each step, select the farthest gas
station `j` within the remaining fuel range, i.e., such that 
`d[j] - d[i] <= n`. This choice ensures that you maximize the
distance covered between stops.

Assume the gas stations are `s...p...x...y...z...d`, and there is
an optimal solution `...pxz...`. The first stop after `p` is `x`
and after that is `z`, while it is possible to refuel at `y` after
`p`. Replacing the `x` with `y` would not invalidate the sequence
as it is still possible to reach `z` afterward, meaning that this
choice would not make the sequence longer.

## 3

We may use the Floyd-Warshall algorithm to find the shortest paths
between all pairs of nodes in a weighted graph. Here is the
algorithm.

1. Initialize a 2D array, called the `distance`, to store
the shortest distances between pairs of cities. Initialize the
matrix with the length of the roads, and zero distance for each
city to itself, and `+inf` for other places.
2. For each pair of cities `i` and `j`, and each city `k`, check if
the path from city `i` to city `j` through city `k` has a smaller
distance than the current distance between `i` and `j`. If so,
update the distance with the smaller distance. In other words, for
each pair of cities `(i, j)`, consider all possible intermediate
cities and check if going through that intermediate city yields a
shorter path.
3. After the algorithm finishes, the distance matrix will contain 
the shortest distances between all pairs of nodes.

The python implementation can be found in [3.py](3.py).

## 4

Assume that there are two empty boxes for thieves in the museum. We
must split all thieves into two groups, such that the sum of times
thieves need in each group is less than `G`. We can solve this
using dynamic programming techniques. The implementation is
available in [4.py](4.py).