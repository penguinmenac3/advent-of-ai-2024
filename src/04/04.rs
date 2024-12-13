use std::io::{self, Read};

fn count_word(grid: &Vec<Vec<char>>, word: &str) -> usize {
    fn search(grid: &Vec<Vec<char>>, word: &str, x: isize, y: isize, dx: isize, dy: isize) -> bool {
        for i in 0..word.len() as isize {
            let nx = x + dx * i;
            let ny = y + dy * i;
            if !(nx >= 0 && nx < grid.len() as isize && ny >= 0 && ny < grid[0].len() as isize) {
                return false;
            }
            if grid[nx as usize][ny as usize] != word.chars().nth(i as usize).unwrap() {
                return false;
            }
        }
        true
    }

    let mut count = 0;
    let first_letter = word.chars().next().unwrap();
    let directions = [
        (1, 0),   // right
        (-1, 0),  // left
        (0, 1),   // down
        (0, -1),  // up
        (1, 1),   // diagonal down-right
        (-1, -1), // diagonal up-left
        (1, -1),  // diagonal down-left
        (-1, 1)   // diagonal up-right
    ];

    for x in 0..grid.len() {
        for y in 0..grid[0].len() {
            if grid[x][y] == first_letter {
                for (dx, dy) in directions {
                    if search(grid, word, x as isize, y as isize, dx, dy) {
                        count += 1;
                    }
                }
            }
        }
    }

    count
}

fn count_xmas_shapes(grid: &Vec<Vec<char>>) -> usize {
    let rows = grid.len();
    let cols = grid[0].len();
    let mut count = 0;

    // Generate all possible orientations of the X-MAS kernel
    let kernels = vec![
        vec![
            vec!['S', '.', 'M'],
            vec!['.', 'A', '.'],
            vec!['S', '.', 'M']
        ],
        vec![
            vec!['M', '.', 'M'],
            vec!['.', 'A', '.'],
            vec!['S', '.', 'S']
        ],
        vec![
            vec!['M', '.', 'S'],
            vec!['.', 'A', '.'],
            vec!['M', '.', 'S']
        ],
        vec![
            vec!['S', '.', 'S'],
            vec!['.', 'A', '.'],
            vec!['M', '.', 'M']
        ],
    ];

    // Slide the kernel over the grid
    for i in 0..rows - 2 {
        for j in 0..cols - 2 { // Adjusted to cols - 3 to prevent out-of-bounds errors
            for kernel in &kernels {
                let mut match_found = true;
                for ki in 0..3 {
                    for kj in 0..3 {
                        if !(kernel[ki][kj] == '.' || grid[i + ki][j + kj] == kernel[ki][kj]) {
                            match_found = false;
                            break;
                        }
                    }
                    if !match_found {
                        break;
                    }
                }
                if match_found {
                    count += 1;
                }
            }
        }
    }

    count
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("Failed to read input");

    // Split the input into lines and convert each line into a list of characters
    let grid: Vec<Vec<char>> = input.trim().lines()
        .map(|line| line.chars().collect())
        .collect();

    let word = "XMAS";
    let part_one_count = count_word(&grid, word);
    println!("Part One: {}", part_one_count);

    let part_two_count = count_xmas_shapes(&grid);
    println!("Part Two: {}", part_two_count);
}