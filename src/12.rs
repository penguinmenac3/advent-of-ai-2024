use std::io::{self, BufRead};

const DEBUG: bool = false;

fn accumulate_region(grid: &Vec<Vec<char>>, visited: &mut Vec<Vec<bool>>, x: usize, y: usize) -> (usize, usize, usize) {
    let n = grid.len();
    let m = grid[0].len();
    let directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]; // up, down, left, right
    let mut area = 1;
    let mut perimeter = 0;
    let mut sides: Vec<Vec<(usize, usize)>> = vec![vec![]; directions.len()];

    let mut stack: Vec<(usize, usize)> = vec![(x, y)];
    while !stack.is_empty() {
        let (cx, cy) = stack.pop().unwrap();
        visited[cx][cy] = true;

        for idx in 0..directions.len() {
            let (dx, dy) = directions[idx];
            let nx = cx as isize + dx;
            let ny = cy as isize + dy;
            if nx >= 0 && nx < n as isize && ny >= 0 && ny < m as isize {
                let nx = nx as usize;
                let ny = ny as usize;
                if grid[nx][ny] == grid[cx][cy] {
                    if !visited[nx][ny] && !stack.contains(&(nx, ny)) {
                        stack.push((nx, ny));
                        area += 1;
                    }
                } else {
                    perimeter += 1;
                    sides[idx].push((cx, cy));
                }
            } else {
                perimeter += 1;
                sides[idx].push((cx, cy));
            }
        }
    }

    let mut merged_sides: Vec<(usize, Vec<(usize, usize)>)> = vec![];
    for idx in 0..directions.len() {
        if sides[idx].is_empty() {
            continue;
        }

        if directions[idx].0 == 0 {
            sides[idx].sort_by(|a, b| a.0.cmp(&b.0));
            sides[idx].sort_by(|a, b| a.1.cmp(&b.1));
        } else {
            sides[idx].sort_by(|a, b| a.1.cmp(&b.1));
            sides[idx].sort_by(|a, b| a.0.cmp(&b.0));
        }

        let mut current_segment = vec![sides[idx][0]];
        for i in 1..sides[idx].len() {
            if (directions[idx].0 == 0 && current_segment.last().unwrap().0 + 1 == sides[idx][i].0 && current_segment.last().unwrap().1 == sides[idx][i].1)
                || (directions[idx].1 == 0 && current_segment.last().unwrap().1 + 1 == sides[idx][i].1 && current_segment.last().unwrap().0 == sides[idx][i].0)
            {
                current_segment.push(sides[idx][i]);
            } else {
                merged_sides.push((idx, current_segment.clone()));
                current_segment = vec![sides[idx][i]];
            }
        }
        if !current_segment.is_empty() {
            merged_sides.push((idx, current_segment));
        }
    }

    if DEBUG {
        println!("Region: {}, Area: {}, Perimeter: {}, Sides: {}", grid[x][y], area, perimeter, merged_sides.len());
    }
    (area, perimeter, merged_sides.len())
}

fn count_regions(grid: &Vec<Vec<char>>) -> (usize, usize) {
    let n = grid.len();
    let m = grid[0].len();
    let mut visited = vec![vec![false; m]; n];

    let mut total_cost_perimeter = 0;
    let mut total_cost_sides = 0;
    for i in 0..n {
        for j in 0..m {
            if !visited[i][j] {
                let (area, perimeter, sides) = accumulate_region(grid, &mut visited, i, j);
                total_cost_perimeter += area * perimeter;
                total_cost_sides += area * sides;
            }
        }
    }

    (total_cost_perimeter, total_cost_sides)
}

fn main() {
    let stdin = io::stdin();
    let mut input_data: Vec<String> = stdin.lock().lines().map(|line| line.unwrap()).collect();

    let map_data: Vec<Vec<char>> = input_data.iter_mut().map(|row| row.chars().collect()).collect();

    let (a, b) = count_regions(&map_data);

    println!("{}", a);
    println!("{}", b);
}