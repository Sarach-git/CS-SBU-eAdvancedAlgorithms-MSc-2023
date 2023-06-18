def best(v, player):
    if len(v) == 0:
        return 0, ""

    if player == 1:
        # L
        a_l, s_l = best(v[1:], 2)
        a_l += v[0]

        l = a_l, "L" + s_l

        # R
        a_r, s_r = best(v[:-1], 2)
        a_r += v[-1]

        r = a_r, "R" + s_r

        # return max
        return l if a_l >= a_r else r
    else:
        # L
        a_l, s_l = best(v[1:], 1)
        l = a_l, "L" + s_l

        # R
        a_r, s_r = best(v[:-1], 1)
        r = a_r, "R" + s_r

        # return min
        return l if a_l <= a_r else r


def main():
    v = list(map(int, input().split()))
    a, s = best(v, 1)
    print(a, s)


if __name__ == "__main__":
    main()
