




cities = list(map(int, input().split()))
oil_capacity = int(input())
lpkm = float(input())


selected = []
s = 0
for i in range(len(cities)-1):
    if (cities[i+1] + s) * lpkm > oil_capacity:
        selected.append(i+1)
        s = 0
    else:
        s += cities[i]

print(selected)

