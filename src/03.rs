use std::io::{self, BufRead};

fn main() {
    let mut result = 0;
    let mut result_all = 0;
    let mut mul_enabled = true; // Initially, all mul instructions are enabled

    for line in io::stdin().lock().lines() {
        let input = line.unwrap();
        let bytes = input.as_bytes();

        let mut p = 0;
        while p < bytes.len() {
            if bytes[p] == b'd' && p + 1 < bytes.len() && bytes[p + 1] == b'o' {
                // Enable multiplication or disable multiplication
                if p + 3 < bytes.len() && bytes[p + 2] == b'(' && bytes[p + 3] == b')' {
                    mul_enabled = true;
                    p += 4; // Move past "do("
                } else if p + 6 < bytes.len() && bytes[p + 2] == b'n' && bytes[p + 3] == b'\'' && bytes[p + 4] == b't' && bytes[p + 5] == b'(' && bytes[p + 6] == b')' {
                    mul_enabled = false;
                    p += 7; // Move past "don't()"
                } else {
                    p += 2;
                }
            } else if bytes[p] == b'm' && p + 1 < bytes.len() && bytes[p + 1] == b'u' && p + 2 < bytes.len() && bytes[p + 2] == b'l' {
                // Check if 'mul' is followed by '('
                p += 3; // Move past "mul"
                if p < bytes.len() && bytes[p] == b'(' {
                    p += 1; // Skip '('

                    // Find the first number
                    let mut num1 = 0;
                    while p < bytes.len() && bytes[p].is_ascii_digit() {
                        num1 = num1 * 10 + (bytes[p] - b'0') as i32;
                        p += 1;
                    }

                    // Check for comma
                    if p < bytes.len() && bytes[p] == b',' {
                        p += 1; // Skip ','

                        // Find the second number
                        let mut num2 = 0;
                        while p < bytes.len() && bytes[p].is_ascii_digit() {
                            num2 = num2 * 10 + (bytes[p] - b'0') as i32;
                            p += 1;
                        }

                        // Check for closing parenthesis
                        if p < bytes.len() && bytes[p] == b')' {
                            let product = num1 * num2;
                            result_all += product;
                            if mul_enabled {
                                result += product;
                            }
                            p += 1; // Skip ')'
                        } else {
                            // Malformed input, skip to the next potential 'm', 'd', or end of line
                            while p < bytes.len() && bytes[p] != b'm' && bytes[p] != b'd' {
                                p += 1;
                            }
                        }
                    } else {
                        // Malformed input, skip to the next potential 'm', 'd', or end of line
                        while p < bytes.len() && bytes[p] != b'm' && bytes[p] != b'd' {
                            p += 1;
                        }
                    }
                } else {
                    // Malformed input, skip to the next potential 'm', 'd', or end of line
                    while p < bytes.len() && bytes[p] != b'm' && bytes[p] != b'd' {
                        p += 1;
                    }
                }
            } else {
                p += 1;
            }
        }
    }

    println!("The sum of all multiplication results is: {}", result_all);
    println!("The sum of all enabled multiplication results is: {}", result);
}