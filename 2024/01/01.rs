use std::collections::HashMap;
use std::fs;

fn main() -> std::io::Result<()> {
    // Read the content of the file
    let contents = fs::read_to_string("./input.txt")?;
    
    // Split the input into lines and parse into vectors
    let mut left_list: Vec<i32> = Vec::new();
    let mut right_list: Vec<i32> = Vec::new();
    for line in contents.trim().lines() {
        let parts: Vec<&str> = line.split_whitespace().collect();
        
        if parts.len() != 2 {
            eprintln!("Error: Each line must contain exactly two integers.");
            return Err(std::io::Error::new(std::io::ErrorKind::Other, "Invalid input format"));
        }
        
        let left_value: i32 = parts[0].parse().expect("Failed to parse integer for left value");
        let right_value: i32 = parts[1].parse().expect("Failed to parse integer for right value");
        
        left_list.push(left_value);
        right_list.push(right_value);
    }
    
    // Sort both lists
    left_list.sort_unstable();
    right_list.sort_unstable();
    
    // Calculate the total distance
    let mut total_distance = 0;
    for (a, b) in left_list.iter().zip(right_list.iter()) {
        total_distance += (a - b).abs();
    }
    
    // Print the result
    println!("The total distance between the lists is: {}", total_distance);

    // Count the occurrences of each number in the right list
    let mut right_count_map = HashMap::new();
    for &num in &right_list {
        *right_count_map.entry(num).or_insert(0) += 1;
    }
    
    // Calculate the similarity score
    let mut similarity_score = 0;
    for &left_value in &left_list {
        if let Some(&count) = right_count_map.get(&left_value) {
            similarity_score += left_value * count;
        }
    }
    
    // Print the result
    println!("The similarity score between the lists is: {}", similarity_score);
    
    Ok(())
}