import os
import sys


BINARY_TYPES = [
    "cpp",
    "rs"
]


def test_all():
    for day in range(1, 25):
        test_day(day)


def test_day(day):
    print(f"# Testing day: {day}")
    fname = f"src/{day:02d}"
    if os.path.exists(fname + ".py"):
        print(f"\nRunning: {fname}.py")
        os.system(f"python {fname}.py")
    for lang in BINARY_TYPES:
        if os.path.exists(f"bin/{day:02d}-{lang}.run"):
            print(f"\nRunning: src/{day:02d}.{lang}")
            os.system(f"bin/{day:02d}-{lang}.run")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        os.system("make all")
        test_all()
    elif len(sys.argv) == 2:
        os.system("make all")
        test_day(int(sys.argv[1]))
    else:
        print("ERROR: Specify no argument to run all days or a single number for a day.")
        print("    Examples:")
        print("    python test.py  # for all tests")
        print("    python test.py 1  # to test only day one")
        exit(1)
