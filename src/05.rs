use std::collections::{HashMap};
use std::io::{self, Read};

fn read_input() -> (Vec<(i32, i32)>, Vec<Vec<i32>>) {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("Failed to read input");

    let input_data: Vec<&str> = input.split("\n\n").collect();
    if input_data.len() != 2 {
        panic!("Input must be split into two sections: rules and updates");
    }

    // Parse the rules
    let mut rules = vec![];
    for line in input_data[0].lines() {
        let parts: Vec<i32> = line.split('|').map(|x| x.trim().parse().expect("Invalid number")).collect();
        if parts.len() != 2 {
            panic!("Each rule must be two numbers separated by '|'");
        }
        rules.push((parts[0], parts[1]));
    }

    // Parse the updates
    let mut updates = vec![];
    for line in input_data[1].lines() {
        let pages: Vec<i32> = line.split(',').map(|x| x.trim().parse().expect("Invalid number")).collect();
        updates.push(pages);
    }

    (rules, updates)
}

fn is_correct_order(update: &[i32], rules: &[(i32, i32)]) -> bool {
    let page_index_map: HashMap<i32, usize> = update.iter().enumerate().map(|(idx, &page)| (page, idx)).collect();

    for &(x, y) in rules {
        if let (Some(&index_x), Some(&index_y)) = (page_index_map.get(&x), page_index_map.get(&y)) {
            if index_x >= index_y {
                return false;
            }
        }
    }
    true
}

fn topological_sort(rules: &[(i32, i32)], pages: &[i32]) -> Vec<i32> {
    use std::collections::VecDeque;

    let mut graph = HashMap::new();
    let mut indegree = HashMap::new();

    for &(x, y) in rules {
        if pages.contains(&x) && pages.contains(&y) {
            graph.entry(x).or_insert_with(Vec::new).push(y);
            *indegree.entry(y).or_insert(0) += 1;
        }
    }

    let mut queue = VecDeque::new();
    for &page in pages {
        if indegree.get(&page).unwrap_or(&0) == &0 {
            queue.push_back(page);
        }
    }

    let mut sorted_order = vec![];

    while let Some(node) = queue.pop_front() {
        sorted_order.push(node);

        if let Some(neighbors) = graph.get(&node) {
            for &neighbor in neighbors {
                *indegree.entry(neighbor).or_insert(0) -= 1;
                if indegree[&neighbor] == 0 {
                    queue.push_back(neighbor);
                }
            }
        }
    }

    sorted_order
}

fn main() {
    let (rules, updates) = read_input();
    let mut total_middle_sum_correct = 0;
    let mut total_middle_sum_incorrect = 0;

    for update in updates {
        if is_correct_order(&update, &rules) {
            let middle_page = update[update.len() / 2];
            total_middle_sum_correct += middle_page;
        } else {
            let sorted_update = topological_sort(&rules, &update);
            let middle_page = sorted_update[sorted_update.len() / 2];
            total_middle_sum_incorrect += middle_page;
        }
    }

    println!("{}", total_middle_sum_correct);
    println!("{}", total_middle_sum_incorrect);
}