def calculate_total_distance(filename):
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

    # Sort both lists
    left_numbers.sort()
    right_numbers.sort()

    # Calculate the total distance
    total_distance = sum(abs(l - r) for l, r in zip(left_numbers, right_numbers))

    return total_distance

# Assuming the input file is named '01.txt'
filename = '01.txt'
total_distance = calculate_total_distance(filename)
print(f"The total distance between the lists is: {total_distance}")