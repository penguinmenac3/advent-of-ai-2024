from itertools import product

def calculate_total_calibration_result(input_lines):
    total_calibration_result = 0
    
    for line in input_lines:
        test_value, numbers_str = line.split(': ')
        test_value = int(test_value)
        
        # Extract digits from the concatenated numbers string
        numbers = [int(digit) for digit in numbers_str.split(" ")]
        
        # Generate all combinations of operators for N-1 positions
        operator_combinations = list(product(['+', '*'], repeat=len(numbers)-1))
        print(operator_combinations)
        
        for combination in operator_combinations:
            result = numbers[0]
            index = 0
            
            for number in numbers[1:]:
                if combination[index] == '+':
                    result += number
                else:  # *
                    result *= number
                index += 1
            
            if result == test_value:
                total_calibration_result += test_value
                break  # No need to check further combinations for this line
    
    return total_calibration_result

if __name__ == "__main__":
    import sys
    input_lines = sys.stdin.read().strip().split('\n')
    print(calculate_total_calibration_result(input_lines))