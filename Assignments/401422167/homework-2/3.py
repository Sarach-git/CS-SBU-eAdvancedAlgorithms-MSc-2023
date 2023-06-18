class FloydWarshallGraph:
    def __init__(self, n):
        self._n = n
        self._d = [
            {
                j: 0 if i == j else float("inf")
                for j in range(i, n)
            }
            for i in range(n)
        ]

    def set_d(self, i, j, d):
        if j < i:
            i, j = j, i
        self._d[i][j] = d

    def get_d(self, i, j):
        if j < i:
            i, j = j, i
        return self._d[i][j]

    def calculate_distances(self):
        for k in range(self._n):
            for i in range(self._n):
                for j in range(self._n):
                    new_d = self.get_d(i, k) + self.get_d(k, j)
                    if new_d < self.get_d(i, j):
                        self.set_d(i, j, new_d)

    def get_sum_d(self):
        return sum([self.get_d(i, j) for i in range(self._n) for j in range(i, self._n)])


def main():
    n, m = map(int, input().split())

    g = FloydWarshallGraph(n)

    for _ in range(m):
        a, b, c = map(int, input().split())
        g.set_d(a - 1, b - 1, 2 ** c)

    g.calculate_distances()

    print(bin(g.get_sum_d())[2:])


if __name__ == "__main__":
    main()
