def can_steal(N, G, A):
    if N > 2 * (G + 1):
        return "NO"  # More than 2N thieves cannot be inside the hall during G minutes

    max_time = max(A)
    if max_time > G:
        return "NO"  # There is a thief who needs more time than the guard's absence

    if max_time <= G and N <= 2:
        return "YES"  # All thieves can complete their theft within the guard's absence

    return "YES"  # In all other cases, it is possible to have an order satisfying the conditions


T = int(input())
result_list = []
for _ in range(T):
    N, G = map(int, input().split())
    A = list(map(int, input().split()))
    result = can_steal(N, G, A)
    result_list.append(result)

for result in result_list:
    print(result)
