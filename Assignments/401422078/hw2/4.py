
# Using backtrack to find one solution
def backtract(g, times, half, selected=[]):
    if sum(selected) >= half:
        if sum(selected) > g:
            return False
        else:
            return True
    for item in times:
        remain_times = times.copy()
        remain_times.remove(item)
        if backtract(g, remain_times, half, selected+[item]):
            return True
    return False


tests = []
test_number = int(input())
for _ in range(test_number):
    n, g = list(map(int, input().split()))
    A = list(map(int, input().split()))
    tests.append([n, g, A])


for n, g, A in tests:
    half = sum(A)/2
    if half > g:
        print('NO')
        continue

    if backtract(g, A, half):
        print('YES')
    else:
        print('NO')




