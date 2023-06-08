def split_is_possible(nums, target):
    sum_nums = sum(nums)

    if sum_nums >= 2 * target:
        return False

    n = len(nums)
    dp = [[False for _ in target + 1] for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = True

    for i in range(1, n + 1):
        for j in range(1, target + 1):
            dp[i][j] = dp[i - 1][j]
            if j >= nums[i - 1]:
                dp[i][j] = dp[i][j] or dp[i - 1][j - nums[i - 1]]

    if not dp[target][n]:
        return False

    return True


def main():
    results = []
    t = int(input())
    for _ in range(t):
        _, g = map(int, input().split())
        nums = map(int, input().split())
        results.append(
            "YES" if split_is_possible(nums, g) else "NO"
        )

    print("\n".join(results))


if __name__ == "__main__":
    main()
