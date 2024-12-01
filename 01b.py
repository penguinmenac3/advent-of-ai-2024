from collections import Counter

def calculate_similarity_score(filename):
    # Read the input from the file
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Initialize two lists for left and right numbers
    left_numbers = []
    right_numbers = []

    # Parse the input into the two lists
    for line in lines:
        if line.strip():  # Ensure we don't process empty lines
            left, right = map(int, line.split())
            left_numbers.append(left)
            right_numbers.append(right)

    # Count occurrences of each number in the right list
    right_count = Counter(right_numbers)

    # Calculate the total similarity score
    total_similarity_score = sum(l * right_count[l] for l in left_numbers)

    return total_similarity_score

# Assuming the input file is named '01.txt'
filename = '01.txt'
total_similarity_score = calculate_similarity_score(filename)
print(f"The total similarity score between the lists is: {total_similarity_score}")