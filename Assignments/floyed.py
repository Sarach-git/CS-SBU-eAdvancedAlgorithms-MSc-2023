INF = float('inf')

# خواندن ورودی
N, M = map(int, input().split())

# ماتریس فواصل را با مقدار بی‌نهایت برای تمام جفت شهرها مقداردهی اولیه کنید
distances = [[INF] * N for _ in range(N)]

# فاصله بین هر شهر و خودش را برابر با صفر قرار دهید
for i in range(N):
    distances[i][i] = 0

# خواندن اطلاعات جاده‌ها و به‌روزرسانی ماتریس فواصل
for _ in range(M):
    Ai, Bi, Ci = map(int, input().split())
    distances[Ai - 1][Bi - 1] = 2 ** Ci
    distances[Bi - 1][Ai - 1] = 2 ** Ci

# الگوریتم فلوید-وارشال برای پیدا کردن حداقل فاصله بین تمام جفت شهرها
for k in range(N):
    for i in range(N):
        for j in range(N):
            distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])

# محاسبه مجموع حداقل فواصل
total_distance = sum(sum(distances[i]) for i in range(N))

# چاپ خروجی به صورت عدد دودویی
print(bin(total_distance)[2:])
