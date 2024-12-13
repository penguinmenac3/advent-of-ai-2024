use std::collections::HashMap;
use std::io::{self, Read};

fn split_number(n: u64) -> (u64, u64) {
    let s = n.to_string();
    let mid = s.len() / 2;
    let left = s[..mid].parse::<u64>().unwrap();
    let right = s[mid..].parse::<u64>().unwrap();
    (left, right)
}

fn transform_stones(stones: Vec<u64>, steps: u32) -> u64 {
    let mut stones_dict: HashMap<u64, u64> = HashMap::new();
    for &stone in &stones {
        *stones_dict.entry(stone).or_insert(0) += 1;
    }

    for _ in 0..steps {
        let mut new_stones: HashMap<u64, u64> = HashMap::new();
        for (&stone, &count) in &stones_dict {
            if stone == 0 {
                *new_stones.entry(1).or_insert(0) += count;
            } else {
                let s = stone.to_string(); // Correctly get the string representation of the stone
                if s.len() % 2 == 0 {
                    let (left, right) = split_number(stone);
                    *new_stones.entry(left).or_insert(0) += count;
                    *new_stones.entry(right).or_insert(0) += count;
                } else {
                    *new_stones.entry(stone * 2024).or_insert(0) += count;
                }
            }
        }
        stones_dict = new_stones;
    }

    stones_dict.values().sum()
}

fn main() -> io::Result<()> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;
    let stones: Vec<u64> = input.trim().split_whitespace().map(|s| s.parse::<u64>().unwrap()).collect();

    println!("{}", transform_stones(stones.clone(), 25));
    println!("{}", transform_stones(stones, 75));

    Ok(())
}