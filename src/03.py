import re

def extract_and_sum_multiplications(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Regular expression pattern for valid mul(X,Y) instructions
    pattern = r'mul\((\d+),(\d+)\)'

    # Find all matches in the content
    matches = re.findall(pattern, content)

    # Initialize the sum of results
    total_sum = 0

    # Iterate over each match and compute the product
    for match in matches:
        x, y = map(int, match)
        result = x * y
        total_sum += result

    return total_sum

def extract_and_sum_multiplications_with_conditions(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Regular expression pattern for valid mul(X,Y) instructions and do()/don't() instructions
    pattern = r'mul\((\d+),(\d+)\)|do\(\)|don\'t\(\)'

    # Find all matches in the content
    matches = list(re.finditer(pattern, content))

    # Initialize the sum of results
    total_sum = 0

    # Flag to track if mul instructions are enabled
    is_enabled = True

    # Process matches
    for match in matches:
        match_str = content[match.start():match.end()]
        if match_str == 'do()':
            is_enabled = True
        elif match_str == "don't()":
            is_enabled = False
        else:
            x, y = map(int, re.findall(r'\d+', match_str))
            if is_enabled:
                total_sum += x * y

    return total_sum

# Path to the data file
file_path = './data/03.txt'

# Calculate the sum of all multiplication results
result = extract_and_sum_multiplications(file_path)

# Print the result
print(f"The sum of all multiplication results is: {result}")

# Calculate the sum of all multiplication results considering conditions
result = extract_and_sum_multiplications_with_conditions(file_path)

# Print the result
print(f"The sum of all enabled multiplication results is: {result}")