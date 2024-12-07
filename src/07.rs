use std::io::{self, BufRead};

fn calculate_total_calibration_result(input_lines: Vec<&str>, include_concat: bool) -> i64 {
    let mut total_calibration_result = 0;

    for line in input_lines {
        // Split the line into two parts: test_value and numbers_str
        let parts: Vec<&str> = line.trim().split(':').collect();
        
        if parts.len() != 2 {
            eprintln!("Invalid line format: {}", line);
            continue; // Skip invalid lines
        }
        
        let test_value: i64 = parts[0].trim().parse().unwrap_or_else(|e| {
            eprintln!("Failed to parse test value in line '{}': {}", line, e);
            0
        });
        let numbers_str: Vec<&str> = parts[1].trim().split_whitespace().collect();

        let numbers: Result<Vec<i64>, _> = numbers_str.iter()
            .map(|&s| s.trim().parse::<i64>())
            .collect();
        
        if let Err(e) = numbers {
            eprintln!("Failed to parse number in line '{}': {}", line, e);
            continue;
        }
        let numbers = numbers.unwrap();

        let mut operators = vec!['+', '*'];
        if include_concat {
            operators.push('|');
        }

        let num_combinations = operators.len().pow((numbers.len() - 1) as u32);

        for i in 0..num_combinations {
            let mut result = numbers[0].to_string();
            let mut combination = Vec::new();

            // Generate the current combination by determining the index of each operator
            let mut temp = i;
            for _ in 0..numbers.len() - 1 {
                combination.push(operators[temp % operators.len()]);
                temp /= operators.len();
            }

            for j in 0..combination.len() {
                match combination[j] {
                    '+' => result = (result.parse::<i64>().unwrap() + numbers[j + 1]).to_string(),
                    '*' => result = (result.parse::<i64>().unwrap() * numbers[j + 1]).to_string(),
                    '|' => result = format!("{}{}", result, numbers[j + 1]),
                    _ => unreachable!(),
                }
            }

            if let Ok(res) = result.parse::<i64>() {
                if res == test_value {
                    total_calibration_result += test_value;
                    break; // No need to check further combinations for this line
                }
            } else {
                eprintln!("Failed to parse result in line '{}': {}", line, result);
            }
        }
    }

    total_calibration_result
}

fn main() {
    let stdin = io::stdin();
    let input_lines: Vec<String> = stdin.lock().lines().map(|l| l.unwrap()).collect();

    // Calculate results for both parts
    let part1_result = calculate_total_calibration_result(input_lines.iter().map(|s| s.as_str()).collect(), false);
    println!("Part 1 Result: {}", part1_result);

    let part2_result = calculate_total_calibration_result(input_lines.iter().map(|s| s.as_str()).collect(), true);
    println!("Part 2 Result: {}", part2_result);
}