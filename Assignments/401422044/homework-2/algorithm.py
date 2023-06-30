#!/usr/bin/env python
# coding: utf-8

# In[4]:


def max_score(nums):
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if length == 1:
                dp[i][j] = nums[i]
            else:
                dp[i][j] = max(nums[i] - dp[i + 1][j], nums[j] - dp[i][j - 1])

    max_score = dp[0][n - 1]
    sequence = construct_sequence(dp, nums, 0, n - 1)

    return max_score, sequence


def construct_sequence(dp, nums, i, j):
    if i == j:
        return ''

    if nums[i] - dp[i + 1][j] > nums[j] - dp[i][j - 1]:
        return 'L' + construct_sequence(dp, nums, i + 1, j)
    else:
        return 'R' + construct_sequence(dp, nums, i, j - 1)


nums = list(map(int, input().split()))
max_score, sequence = max_score(nums)
print(max_score)
print(sequence)


# In[ ]:


INF = float('inf')

def floyd_warshall(N, edges):
    # ساخت ماتریس فاصله با اندازه NxN و مقدار بی‌نهایت برای همه‌ی جفت رئوس
    dist = [[INF] * N for _ in range(N)]

    # تنظیم فواصل اولیه براساس وزن جاده‌ها
    for i in range(N):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = w
        dist[v][u] = w

    # اعمال الگوریتم فلوید-وارشال
    for k in range(N):
        for i in range(N):
            for j in range(N):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist

# خواندن ورودی
N, M = map(int, input().split())
edges = []
for _ in range(M):
    A, B, C = map(int, input().split())
    edges.append((A, B, C))

# حل مسئله با الگوریتم فلوید-وارشال
distances = floyd_warshall(N, edges)

# محاسبه مجموع حداقل فواصل بین جفت شهرها
total_distance = 0
for i in range(N):
    for j in range(i + 1, N):
        total_distance += distances[i][j]

# چاپ مجموع حداقل فواصل به صورت دودویی
print(bin(total_distance)[2:])


# In[ ]:


def is_order_possible(N, G, A, assigned_times, current_time):
    # بررسی اتمام حالت پایه (تمام سارقان در سالن حضور داشته‌باشند)
    if len(assigned_times) == N:
        return True
    
    # قرار دادن سارق در سالن
    for i in range(N):
        if i not in assigned_times:
            assigned_times.add(i)
            
            # بررسی شرایط حضور در سالن
            if current_time + A[i] <= G and is_order_possible(N, G, A, assigned_times, current_time + A[i]):
                return True
            
            assigned_times.remove(i)
    
    return False

# خواندن ورودی
T = int(input())

for _ in range(T):
    N, G = map(int, input().split())
    A = list(map(int, input().split()))
    
    # اجرای الگوریتم بازگشتی
    result = is_order_possible(N, G, A, set(), 0)
    
    # چاپ پاسخ
    if result:
        print("YES")
    else:
        print("NO")


# In[ ]:




