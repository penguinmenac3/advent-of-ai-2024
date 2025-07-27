use std::collections::HashMap;
use std::io::{self, Read};

const UP: (isize, isize) = (0, -1);
const DOWN: (isize, isize) = (0, 1);
const LEFT: (isize, isize) = (-1, 0);
const RIGHT: (isize, isize) = (1, 0);

fn parse_input(input_str: &str) -> (HashMap<(isize, isize), char>, Vec<(isize, isize)>) {
    let blocks: Vec<&str> = input_str.split("\n\n").collect();
    let lines: Vec<&str> = blocks[0].lines().collect();
    let mut map_dict = HashMap::new();

    for (y, line) in lines.iter().enumerate() {
        for (x, c) in line.chars().enumerate() {
            map_dict.insert((x as isize, y as isize), c);
        }
    }

    let steps: Vec<(isize, isize)> = blocks[1]
        .replace('\n', "")
        .chars()
        .map(|ch| match ch {
            '^' => UP,
            '<' => LEFT,
            '>' => RIGHT,
            'v' => DOWN,
            _ => (0, 0),
        })
        .collect();

    (map_dict, steps)
}

fn try_to_step(
    map_dict: &mut HashMap<(isize, isize), char>,
    robot_pos: &(isize, isize),
    direction: &(isize, isize),
) -> bool {
    let original_map = map_dict.clone();
    
    if *map_dict.get(robot_pos).unwrap() == '.' {
        return true;
    } else if *map_dict.get(robot_pos).unwrap() == 'O' || *map_dict.get(robot_pos).unwrap() == '@' {
        let new_pos = (robot_pos.0 + direction.0, robot_pos.1 + direction.1);
        if try_to_step(map_dict, &new_pos, direction) {
            map_dict.insert(new_pos, *map_dict.get(robot_pos).unwrap());
            map_dict.insert(*robot_pos, '.');
            return true;
        }
    } else if *map_dict.get(robot_pos).unwrap() == ']' {
        let new_pos = (robot_pos.0 - 1, robot_pos.1);
        return try_to_step(map_dict, &new_pos, direction);
    } else if *map_dict.get(robot_pos).unwrap() == '[' {
        let dir_x = direction.0;
        let dir_y = direction.1;

        if (dir_x, dir_y) == LEFT {
            let new_pos_1 = (robot_pos.0 - 1, robot_pos.1);
            if try_to_step(map_dict, &new_pos_1, direction) {
                map_dict.insert(new_pos_1, '[');
                map_dict.insert(*robot_pos, ']');
                map_dict.insert((robot_pos.0 + 1, robot_pos.1), '.');
                return true;
            }
        } else if (dir_x, dir_y) == RIGHT {
            let new_pos_2 = (robot_pos.0 + 2, robot_pos.1);
            if try_to_step(map_dict, &new_pos_2, direction) {
                map_dict.insert(*robot_pos, '.');
                map_dict.insert((robot_pos.0 + 1, robot_pos.1), '[');
                map_dict.insert(new_pos_2, ']');
                return true;
            }
        } else {
            let new_pos_1 = (robot_pos.0 + dir_x, robot_pos.1 + dir_y);
            let new_pos_2 = (robot_pos.0 + 1 + dir_x, robot_pos.1 + dir_y);

            if try_to_step(map_dict, &new_pos_1, direction) && try_to_step(map_dict, &new_pos_2, direction) {
                map_dict.insert(*robot_pos, '.');
                map_dict.insert((robot_pos.0 + 1, robot_pos.1), '.');
                map_dict.insert(new_pos_1, '[');
                map_dict.insert(new_pos_2, ']');
                return true;
            }
        }
    }

    *map_dict = original_map.clone();
    false
}

fn solve(input_str: &str) -> isize {
    let (mut map_dict, steps) = parse_input(input_str);
    let mut robot = map_dict.iter().find(|&(_, &c)| c == '@').unwrap().0;

    for direction in &steps {
        if try_to_step(&mut map_dict, &robot, direction) {
            robot.0 += direction.0;
            robot.1 += direction.1;
        }
    }

    let result: isize = map_dict
        .iter()
        .filter(|&(_, &c)| c == '[' || c == 'O')
        .map(|(&(x, y), _)| x + 100 * y)
        .sum();

    result
}

fn scale_up(input_str: &str) -> String {
    input_str
        .replace('#', "##")
        .replace('.', "..")
        .replace('O', "[]")
        .replace('@', "@.")
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();

    println!("{}", solve(&input));
    println!("{}", solve(&scale_up(&input)));
}