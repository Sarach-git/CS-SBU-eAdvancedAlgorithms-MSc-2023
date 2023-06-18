def best(v, player, p1_max, p2_min, current_score):
    if len(v) == 0:
        return 0, ""

    if player == 1:
        # L
        a_l, s_l = best(v[1:], 2, p1_max, p2_min, current_score + v[0])
        a_l += v[0]

        l = a_l, "L" + s_l

        # update & prune
        p1_max = max(p1_max, a_l)

        if p1_max >= p2_min + current_score:
            return l

        # R
        a_r, s_r = best(v[:-1], 2, p1_max, p2_min, current_score + v[-1])
        a_r += v[-1]

        r = a_r, "R" + s_r

        # return max
        return l if a_l >= a_r else r
    else:
        # L
        a_l, s_l = best(v[1:], 1, p1_max, p2_min, current_score)
        l = a_l, "L" + s_l

        # update & prune
        p2_min = min(p2_min, a_l)

        if p1_max >= p2_min + current_score:
            return l

        # R
        a_r, s_r = best(v[:-1], 1, p1_max, p2_min, current_score)
        r = a_r, "R" + s_r

        # return min
        return l if a_l <= a_r else r


def main():
    v = list(map(int, input().split()))
    a, s = best(v, 1, float("-inf"), float("inf"), 0)
    print(a, s)


if __name__ == "__main__":
    main()
