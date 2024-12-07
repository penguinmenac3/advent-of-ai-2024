from itertools import product

def calculate_total_calibration_result(input_lines, include_concat=False):
    total_calibration_result = 0
    
    for line in input_lines:
        test_value, numbers_str = line.split(': ')
        test_value = int(test_value)
        
        # Extract digits from the concatenated numbers string
        numbers = [int(digit) for digit in numbers_str.split(" ")]
        
        if include_concat:
            operators = ['+', '*', '||']
        else:
            operators = ['+', '*']
        
        # Generate all combinations of operators for N-1 positions
        operator_combinations = list(product(operators, repeat=len(numbers)-1))
        
        for combination in operator_combinations:
            result = numbers[0]
            index = 0
            
            while index < len(combination):
                if combination[index] == '+':
                    result += numbers[index + 1]
                elif combination[index] == '*':
                    result *= numbers[index + 1]
                else:  # '||'
                    # Concatenate the current number with the next
                    result = int(str(result) + str(numbers[index + 1]))
                
                index += 1
            
            if result == test_value:
                total_calibration_result += test_value
                break  # No need to check further combinations for this line
    
    return total_calibration_result

if __name__ == "__main__":
    import sys
    input_lines = sys.stdin.read().strip().split('\n')
    
    # Calculate results for both parts
    part1_result = calculate_total_calibration_result(input_lines, include_concat=False)
    print(f"Part 1 Result: {part1_result}")

    part2_result = calculate_total_calibration_result(input_lines, include_concat=True)
    print(f"Part 2 Result: {part2_result}")