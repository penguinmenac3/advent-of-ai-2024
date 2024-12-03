import sys
from collections import Counter

def parse_input():
    # Read the input from the stdinput
    lines = sys.stdin.readlines()

    # Initialize two lists for left and right numbers
    left_numbers = []
    right_numbers = []

    # Parse the input into the two lists
    for line in lines:
        if line.strip():  # Ensure we don't process empty lines
            left, right = map(int, line.split())
            left_numbers.append(left)
            right_numbers.append(right)

    return left_numbers, right_numbers

def calculate_total_distance(left_numbers, right_numbers):
    # Sort both lists
    left_numbers.sort()
    right_numbers.sort()

    # Calculate the total distance
    total_distance = sum(abs(l - r) for l, r in zip(left_numbers, right_numbers))

    return total_distance

def calculate_similarity_score(left_numbers, right_numbers):
    # Count occurrences of each number in the right list
    right_count = Counter(right_numbers)

    # Calculate the total similarity score
    total_similarity_score = sum(l * right_count[l] for l in left_numbers)

    return total_similarity_score

def main():
    left_numbers, right_numbers = parse_input()

    total_distance = calculate_total_distance(left_numbers, right_numbers)
    print(f"The total distance between the lists is: {total_distance}")

    total_similarity_score = calculate_similarity_score(left_numbers, right_numbers)
    print(f"The total similarity score between the lists is: {total_similarity_score}")

if __name__ == "__main__":
    main()
