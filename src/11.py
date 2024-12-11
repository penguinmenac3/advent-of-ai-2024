import sys

def split_number(n):
    """Split a number into two halves."""
    s = str(n)
    mid = len(s) // 2
    left = int(s[:mid])
    right = int(s[mid:])
    return left, right

def transform_stones(stones):
    """Transform the list of stones according to the rules."""
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            left, right = split_number(stone)
            new_stones.extend([left, right])
        else:
            new_stones.append(stone * 2024)
    return new_stones

def main():
    # Read input from stdin
    stones = list(map(int, sys.stdin.read().strip().split()))
    
    # Perform the transformation for 25 blinks
    for _ in range(25):
        stones = transform_stones(stones)
    print(len(stones))

    for _ in range(50):
        stones = transform_stones(stones)
    print(len(stones))

if __name__ == "__main__":
    main()