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
        
        # Number of possible operator combinations is len(operators)^(len(numbers)-1)
        num_combinations = len(operators) ** (len(numbers) - 1)
        
        for i in range(num_combinations):
            result = numbers[0]
            combination = []
            
            # Generate the current combination by determining the index of each operator
            temp = i
            for _ in range(len(numbers) - 1):
                combination.append(operators[temp % len(operators)])
                temp //= len(operators)
            
            for j in range(len(combination)):
                if combination[j] == '+':
                    result += numbers[j + 1]
                elif combination[j] == '*':
                    result *= numbers[j + 1]
                else:  # '||'
                    result = int(str(result) + str(numbers[j + 1]))
            
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