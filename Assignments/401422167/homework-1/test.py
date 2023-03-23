import random
import sys
import time
import typing

from main import mul

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def gen_random(length):
    return ''.join(random.choice(DIGITS) for _ in range(length))


def run_and_measure(f: typing.Callable, *args):
    start = time.process_time_ns()
    result = f(*args)
    taken_time = time.process_time_ns() - start
    return result, taken_time


def main():
    if len(sys.argv) != 2:
        print("this script needs exactly one arguments.")
        exit()

    n = int(sys.argv[1])
    a, b = gen_random(n), gen_random(n)
    print(f"a = {a}")
    print(f"b = {b}\n")

    # run and measure python implementation
    _, time_python = run_and_measure(lambda x, y: x * y, int(a), int(b))
    print(f"python took: {time_python}ns")

    # run and measure our implementation
    _, time_mul = run_and_measure(mul, a, b)
    print(f"mul took: {time_mul}ns")


if __name__ == "__main__":
    main()
