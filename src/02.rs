use std::fs::File;
use std::io::{self, BufRead};

fn is_safe(report: &[i32]) -> bool {
    if report.len() < 2 {
        return true;
    }

    let mut direction = None;

    for i in 1..report.len() {
        let diff = report[i] - report[i - 1];

        if !(1..=3).contains(&diff.abs()) {
            return false;
        }

        let current_direction = diff > 0;
        if direction.is_none() {
            direction = Some(current_direction);
        } else if direction != Some(current_direction) {
            return false;
        }
    }

    true
}

fn is_safe_with_dampener(report: &[i32]) -> bool {
    for i in 0..report.len() {
        let mut modified_report = report.to_vec();
        modified_report.remove(i);
        if is_safe(&modified_report) {
            return true;
        }
    }
    false
}

fn count_safe_reports(file_path: &str) -> io::Result<(usize, usize)> {
    let file = File::open(file_path)?;
    let reader = io::BufReader::new(file);

    let mut safe_count = 0;
    let mut safe_with_dampener_count = 0;

    for line in reader.lines() {
        let levels: Vec<i32> = line?
            .trim()
            .split_whitespace()
            .map(|s| s.parse().expect("Failed to parse integer"))
            .collect();

        if is_safe(&levels) {
            safe_count += 1;
        }
        if is_safe(&levels) || is_safe_with_dampener(&levels) {
            safe_with_dampener_count += 1;
        }
    }

    Ok((safe_count, safe_with_dampener_count))
}

fn main() -> io::Result<()> {
    let (safe_reports, safe_reports_with_dampener) = count_safe_reports("./data/02.txt")?;
    println!("Number of safe reports: {}", safe_reports);
    println!("Number of safe reports with dampener: {}", safe_reports_with_dampener);
    Ok(())
}
