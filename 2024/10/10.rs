use std::collections::HashMap;
use std::io::{self, BufRead};

fn parse_input() -> Vec<Vec<i32>> {
    let stdin = io::stdin();
    let mut grid = vec![];

    for line in stdin.lock().lines() {
        let line = line.unwrap(); // Handle the Result returned by lines()
        if line.trim().is_empty() { // Check for empty or whitespace-only lines
            break;
        }
        grid.push(line.chars().map(|c| c.to_digit(10).unwrap() as i32).collect());
    }

    grid
}

fn is_valid_move(x: usize, y: usize, grid: &Vec<Vec<i32>>, visited: &mut Vec<Vec<bool>>, current_height: i32) -> bool {
    let rows = grid.len();
    let cols = grid[0].len();

    if x < rows && y < cols && !visited[x][y] && grid[x][y] == current_height + 1 {
        return true;
    }
    false
}

fn dfs(x: usize, y: usize, grid: &Vec<Vec<i32>>, visited: &mut Vec<Vec<bool>>, bitmasks: &mut [HashMap<usize, i32>; 10]) {
    let directions = [(0, 1), (1, 0), (0, -1), (-1, 0)];
    // Prefixing the unused variable with an underscore
    let _rows = grid.len();
    let cols = grid[0].len();

    if grid[x][y] == 9 {
        // Mark the path in the bitmask for height 9
        let key = x * cols + y;
        *bitmasks[grid[x][y] as usize].entry(key).or_insert(0) += 1;
        return;
    }

    for (dx, dy) in directions {
        let nx = x as isize + dx;
        let ny = y as isize + dy;

        if nx >= 0 && ny >= 0 && is_valid_move(nx as usize, ny as usize, grid, visited, grid[x][y]) {
            visited[nx as usize][ny as usize] = true;
            dfs(nx as usize, ny as usize, grid, visited, bitmasks);
            visited[nx as usize][ny as usize] = false;
        }
    }
}

fn calculate_trailhead_score_and_rating(trailhead: (usize, usize), grid: &Vec<Vec<i32>>) -> (i32, i32) {
    let _rows = grid.len(); // Prefixing the unused variable with an underscore
    let cols = grid[0].len();
    let mut visited = vec![vec![false; cols]; grid.len()];
    let mut bitmasks: [HashMap<usize, i32>; 10] = Default::default();

    visited[trailhead.0][trailhead.1] = true;
    dfs(trailhead.0, trailhead.1, grid, &mut visited, &mut bitmasks);

    let score = bitmasks.iter().skip(1).map(|b| b.len() as i32).sum();
    // Specify the type for sum to avoid ambiguity
    let rating: i32 = bitmasks.iter().map(|b| b.values().sum::<i32>()).sum();

    (score, rating)
}

fn main() {
    let grid = parse_input();
    let trailheads: Vec<(usize, usize)> = grid.iter().enumerate()
        .flat_map(|(i, row)| row.iter().enumerate()
            .filter(|&(_, &height)| height == 0)
            .map(move |(j, _)| (i, j)))
        .collect();

    let mut total_score = 0;
    let mut total_rating = 0;

    for trailhead in trailheads {
        let (score, rating) = calculate_trailhead_score_and_rating(trailhead, &grid);
        total_score += score;
        total_rating += rating;
    }

    println!("{}", total_score); // Sum of scores
    println!("{}", total_rating); // Sum of ratings
}