import sys

def split_number(n):
    """Split a number into two halves."""
    s = str(n)
    mid = len(s) // 2
    left = int(s[:mid])
    right = int(s[mid:])
    return left, right

def transform_stones(stones, steps=25):
    """Transform the list of stones according to the rules."""
    num_leafs = 0
    queue = [
        (v, 0)
        for v in stones
    ]
    while len(queue) > 0:
        val, step = queue.pop()
        while step < steps:
            step += 1
            if val == 0:
                val = 1
            elif len(str(val)) % 2 == 0:
                left, right = split_number(val)
                queue.append((right, step))
                val = left
            else:
                val *= 2024
        num_leafs += 1
    return num_leafs

def main():
    # Read input from stdin
    stones = list(map(int, sys.stdin.read().strip().split()))
    print(transform_stones(stones, steps=25))
    print(transform_stones(stones, steps=75))

if __name__ == "__main__":
    main()
