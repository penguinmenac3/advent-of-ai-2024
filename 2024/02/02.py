#!/usr/bin/env python3
import sys

def is_safe(report):
    if len(report) < 2:
        return True

    direction = None
    for i in range(1, len(report)):
        diff = report[i] - report[i - 1]
        
        if not (1 <= abs(diff) <= 3):
            return False
        
        current_direction = diff > 0
        if direction is None:
            direction = current_direction
        elif direction != current_direction:
            return False

    return True

def is_safe_with_dampener(report):
    for i in range(len(report)):
        if is_safe(report[:i] + report[i+1:]):
            return True
    return False

def count_safe_reports():
    safe_count = 0
    safe_with_dampener_count = 0
    
    for line in sys.stdin.readlines():
        levels = list(map(int, line.strip().split()))
        if is_safe(levels):
            safe_count += 1
        if is_safe(levels) or is_safe_with_dampener(levels):
            safe_with_dampener_count += 1
    return safe_count, safe_with_dampener_count
    
# Assuming the input is stored in a file named "02.txt"
safe_reports, safe_reports_with_dampener = count_safe_reports()
print(f"Number of safe reports: {safe_reports}")
print(f"Number of safe reports with dampener: {safe_reports_with_dampener}")
