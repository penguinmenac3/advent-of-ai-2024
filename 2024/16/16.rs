use std::collections::{HashMap, HashSet};
use std::io::{self, BufRead};

fn parse_input() -> (Vec<Vec<char>>, (usize, usize), (usize, usize)) {
    let stdin = io::stdin();
    let mut maze: Vec<Vec<char>> = vec![];
    let mut start_position = None;
    let mut end_position = None;

    for (row_idx, line) in stdin.lock().lines().enumerate() {
        let line = line.expect("Failed to read line");
        if line.is_empty() {
            break;
        }
        maze.push(line.chars().collect());

        // Find start and end positions
        if let Some(col_idx) = line.find('S') {
            start_position = Some((row_idx, col_idx));
        }
        if let Some(col_idx) = line.find('E') {
            end_position = Some((row_idx, col_idx));
        }
    }

    (maze, start_position.expect("Start position not found"), end_position.expect("End position not found"))
}

fn move_forward(maze: &Vec<Vec<char>>, row: usize, col: usize, direction: char) -> Option<(usize, usize)> {
    let directions = match direction {
        'N' => (-1, 0),
        'E' => (0, 1),
        'S' => (1, 0),
        'W' => (0, -1),
        _ => return None,
    };

    let new_row = row as isize + directions.0;
    let new_col = col as isize + directions.1;

    if new_row >= 0 && new_row < maze.len() as isize
        && new_col >= 0 && new_col < maze[0].len() as isize
        && maze[new_row as usize][new_col as usize] != '#'
    {
        Some((new_row as usize, new_col as usize))
    } else {
        None
    }
}

fn rotate(direction: char, rotation: &str) -> char {
    let directions = vec!['N', 'E', 'S', 'W'];
    let current_index = directions.iter().position(|&d| d == direction).unwrap();
    let new_index = match rotation {
        "L" => (current_index + 3) % 4,
        "R" => (current_index + 1) % 4,
        _ => panic!("Invalid rotation"),
    };
    directions[new_index]
}

fn find_min_score_and_tiles(maze: &Vec<Vec<char>>, start_position: (usize, usize), end_position: (usize, usize)) -> (i32, usize) {
    use std::collections::BinaryHeap;

    #[derive(PartialEq, Eq)]
    struct State {
        score: i32,
        direction: char,
        position: (usize, usize),
        trajectory: Vec<(usize, usize)>,
    }

    impl Ord for State {
        fn cmp(&self, other: &Self) -> std::cmp::Ordering {
            self.score.cmp(&other.score).reverse()
        }
    }

    impl PartialOrd for State {
        fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
            Some(self.cmp(other))
        }
    }

    let mut pq = BinaryHeap::new();
    pq.push(State {
        score: 0,
        direction: 'E',
        position: start_position,
        trajectory: vec![start_position],
    });

    let mut visited: HashMap<(usize, usize, char), i32> = HashMap::new();
    let mut paths: HashMap<i32, HashSet<(usize, usize)>> = HashMap::new();

    let mut min_score = i32::MAX;

    while let Some(State { score, direction, position, trajectory }) = pq.pop() {
        if score > min_score {
            continue;
        }

        let key = (position.0, position.1, direction);
        if visited.contains_key(&key) && *visited.get(&key).unwrap() <= score {
            continue;
        }
        visited.insert(key, score);

        // Debug print current state
        println!("Position: {:?}, Direction: {}, Score: {}", position, direction, score);

        // Check if we have reached the end
        if position == end_position {
            min_score = min_score.min(score);
            paths.entry(min_score).or_insert_with(HashSet::new).extend(trajectory.iter().cloned());
            println!("Reached end with score {}, trajectory length: {}", score, trajectory.len());
        } else {
            // Try rotating left and right without moving
            for rotation in ["L", "R"] {
                let new_direction = rotate(direction, rotation);
                pq.push(State {
                    score: score + 1000,
                    direction: new_direction,
                    position,
                    trajectory: trajectory.clone(),
                });
            }

            // Try moving forward
            if let Some(new_position) = move_forward(maze, position.0, position.1, direction) {
                pq.push(State {
                    score: score + 1,
                    direction,
                    position: new_position,
                    trajectory: trajectory.iter().cloned().chain(std::iter::once(new_position)).collect(),
                });
            }
        }
    }

    let unique_tiles_on_best_paths = paths.get(&min_score).unwrap_or(&HashSet::new()).len();
    println!("Unique tiles on best paths: {}", unique_tiles_on_best_paths);
    (min_score, unique_tiles_on_best_paths)
}

fn main() {
    let (maze, start_position, end_position) = parse_input();
    let (min_score, unique_tile_count) = find_min_score_and_tiles(&maze, start_position, end_position);
    println!("Minimum score to reach the end: {}", min_score);
    println!("Number of unique tiles on best paths: {}", unique_tile_count);
}