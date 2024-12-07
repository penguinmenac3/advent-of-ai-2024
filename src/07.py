from typing import List


def backtrack(
    index: int,
    current_result: int,
    test_value: int,
    numbers: List[int],
    include_concat: bool
) -> bool:
    if current_result > test_value:
        return False

    if index >= len(numbers):
        return current_result == test_value
    
    matches = backtrack(index + 1, current_result + numbers[index], test_value, numbers, include_concat)
    matches |= backtrack(index + 1, current_result * numbers[index], test_value, numbers, include_concat)
    if include_concat:
        mul = 1;
        tmp = numbers[index];
        while (tmp > 0):
            tmp //= 10
            mul *= 10
        concatenated_result = current_result * mul + numbers[index];
        matches |= backtrack(index + 1, concatenated_result, test_value, numbers, include_concat)
    
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
        
        # Start backtracking from the second number
        if backtrack(1, numbers[0], test_value, numbers, include_concat):
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