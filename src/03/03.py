#!/usr/bin/env python3
import re
import sys


def extract_and_sum_multiplications():
    # Read the content of the file
    content = sys.stdin.read()

    # Regular expression pattern for valid mul(X,Y) instructions and do()/don't() instructions
    pattern = r'mul\((\d+),(\d+)\)|do\(\)|don\'t\(\)'

    # Find all matches in the content
    matches = list(re.finditer(pattern, content))

    # Initialize the sum of results for both cases
    total_sum_unconditional = 0
    total_sum_conditional = 0

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
            total_sum_unconditional += x * y
            if is_enabled:
                total_sum_conditional += x * y

    return total_sum_unconditional, total_sum_conditional

# Calculate the sum of all multiplication results and conditional sums
unconditional_result, conditional_result = extract_and_sum_multiplications()

# Print the result
print(f"The sum of all multiplication results is: {unconditional_result}")
print(f"The sum of all enabled multiplication results is: {conditional_result}")