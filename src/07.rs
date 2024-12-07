use std::io::{self, Read};

fn backtrack(
    index: usize,
    current_result: i64,
    test_value: i64,
    numbers: &[i64],
    include_concat: bool,
) -> bool {
    if current_result > test_value {
        return false;
    }

    if index >= numbers.len() {
        return current_result == test_value;
    }

    let matches = backtrack(index + 1, current_result + numbers[index], test_value, numbers, include_concat)
        || backtrack(index + 1, current_result * numbers[index], test_value, numbers, include_concat);

    if include_concat {
        let mut mul: i64 = 1;
        let mut tmp: i64 = numbers[index];
        while tmp > 0 {
            tmp /= 10;
            mul *= 10;
        }
        let concatenated_result: i64 = current_result * mul + numbers[index];
        return matches || backtrack(index + 1, concatenated_result, test_value, numbers, include_concat);
    }

    matches
}

fn calculate_total_calibration_result(
    input_lines: Vec<&str>,
    include_concat: bool,
) -> i64 {
    let mut total_calibration_result = 0;

    for line in input_lines {
        let parts: Vec<&str> = line.split(": ").collect();
        let test_value: i64 = parts[0].parse().unwrap();

        // Extract digits from the concatenated numbers string
        let numbers: Vec<i64> = parts[1].split_whitespace()
            .map(|digit| digit.parse().unwrap())
            .collect();

        // Start backtracking from the second number
        if backtrack(1, numbers[0], test_value, &numbers, include_concat) {
            total_calibration_result += test_value;
        }
    }

    total_calibration_result
}

fn main() -> io::Result<()> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;

    let input_lines: Vec<&str> = input.trim().split('\n').collect();

    // Calculate results for both parts
    let part1_result = calculate_total_calibration_result(input_lines.clone(), false);
    println!("Part 1 Result: {}", part1_result);

    let part2_result = calculate_total_calibration_result(input_lines, true);
    println!("Part 2 Result: {}", part2_result);

    Ok(())
}