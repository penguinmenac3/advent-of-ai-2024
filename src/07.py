from typing import List


def backtrack(
    index: int,
    current_result: int,
    test_value: int,
    numbers: List[int],
    operators: List[str]
) -> None:
    if index >= len(numbers):
        if current_result == test_value:
            return True
        return False
    
    matches = False
    for operator in operators:
        new_result = current_result
        
        if operator == '+':
            new_result += numbers[index]
        elif operator == '*':
            new_result *= numbers[index]
        else:  # '||'
            new_result = int(str(new_result) + str(numbers[index]))
        
        if new_result > test_value:
            continue
        
        matches |= backtrack(index + 1, new_result, test_value, numbers, operators)
    return matches


def calculate_total_calibration_result(
    input_lines: List[str],
    include_concat: bool = False
) -> int:
    total_calibration_result: int = 0
    
    for line in input_lines:
        test_value, numbers_str = line.split(': ')
        test_value = int(test_value)
        
        # Extract digits from the concatenated numbers string
        numbers: List[int] = [int(digit) for digit in numbers_str.split(" ")]
        
        if include_concat:
            operators: List[str] = ['+', '*', '||']
        else:
            operators: List[str] = ['+', '*']
        
        # Start backtracking from the second number
        if (backtrack(1, numbers[0], test_value, numbers, operators)):
            total_calibration_result += test_value
    
    return total_calibration_result


if __name__ == "__main__":
    import sys
    input_lines: List[str] = sys.stdin.read().strip().split('\n')
    
    # Calculate results for both parts
    part1_result: int = calculate_total_calibration_result(input_lines, include_concat=False)
    print(f"Part 1 Result: {part1_result}")

    part2_result: int = calculate_total_calibration_result(input_lines, include_concat=True)
    print(f"Part 2 Result: {part2_result}")
