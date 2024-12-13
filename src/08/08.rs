use std::collections::{HashSet, HashMap};
use std::io::{self, Read}; // Add this line

fn parse_input() -> Vec<Vec<char>> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    input.trim().lines()
        .map(|line| line.chars().collect())
        .collect()
}

fn find_antinodes(grid: &Vec<Vec<char>>) -> (HashSet<(usize, usize)>, HashSet<(usize, usize)>) {
    let mut antinode_positions = HashSet::new();
    let mut antinode_positions_with_harmonics = HashSet::new();
    let mut freq_to_positions = HashMap::new();

    // Populate the frequency dictionary with antenna positions
    let rows = grid.len();
    let cols = grid[0].len();
    for i in 0..rows {
        for j in 0..cols {
            let char = grid[i][j];
            if char != '.' {
                freq_to_positions.entry(char).or_insert(vec![]).push((i, j));
            }
        }
    }

    // Calculate antinodes for each frequency
    for positions in freq_to_positions.values() {
        for i in 0..positions.len() {
            let (x1, y1) = positions[i];
            for j in i + 1..positions.len() {
                let (x2, y2) = positions[j];

                // Calculate differences
                let dx = x2 - x1;
                let dy = y2 - y1;

                // Check if one is twice as far away in any direction
                let antinode_pos1 = (x1 - dx, y1 - dy);
                let antinode_pos2 = (x2 + dx, y2 + dy);

                if antinode_pos1.0 < rows && antinode_pos1.1 < cols {
                    antinode_positions.insert(antinode_pos1);
                }
                if antinode_pos2.0 < rows && antinode_pos2.1 < cols {
                    antinode_positions.insert(antinode_pos2);
                }

                let mut antinode_pos = (x1, y1);
                while antinode_pos.0 < rows && antinode_pos.1 < cols {
                    antinode_positions_with_harmonics.insert(antinode_pos);
                    antinode_pos = (antinode_pos.0 - dx, antinode_pos.1 - dy);
                }

                let mut antinode_pos = (x2, y2);
                while antinode_pos.0 < rows && antinode_pos.1 < cols {
                    antinode_positions_with_harmonics.insert(antinode_pos);
                    antinode_pos = (antinode_pos.0 + dx, antinode_pos.1 + dy);
                }
            }
        }
    }

    (antinode_positions, antinode_positions_with_harmonics)
}

fn main() {
    let grid = parse_input();
    let (part1, part2) = find_antinodes(&grid);
    println!("{}", part1.len());
    println!("{}", part2.len());
}