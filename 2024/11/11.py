#!/usr/bin/env python3
import sys
from collections import defaultdict
from typing import List, Dict

def split_number(n: int) -> (int, int):
    """Split a number into two halves."""
    s = str(n)
    mid = len(s) // 2
    left = int(s[:mid])
    right = int(s[mid:])
    return left, right

def transform_stones(stones: List[int], steps: int = 25) -> int:
    """Transform the list of stones according to the rules using lazy evaluation and counting."""
    # Initialize the stones dictionary
    stones_dict: Dict[int, int] = defaultdict(int)
    for stone in stones:
        stones_dict[stone] += 1
    
    for _ in range(steps):
        new_stones: Dict[int, int] = defaultdict(int)
        for stone, count in stones_dict.items():
            if stone == 0:
                new_stones[1] += count
            elif len(str(stone)) % 2 == 0:
                left, right = split_number(stone)
                new_stones[left] += count
                new_stones[right] += count
            else:
                new_stones[stone * 2024] += count
        stones_dict = new_stones
    
    return sum(count for stone, count in stones_dict.items())

def main():
    # Read input from stdin
    stones: List[int] = list(map(int, sys.stdin.read().strip().split()))
    print(transform_stones(stones, steps=25))
    print(transform_stones(stones, steps=75))

if __name__ == "__main__":
    main()