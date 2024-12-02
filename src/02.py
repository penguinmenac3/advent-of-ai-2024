def is_safe(report):
    if len(report) < 2:
        return True

    # Determine if the report is increasing or decreasing
    increasing = decreasing = None

    for i in range(1, len(report)):
        diff = report[i] - report[i - 1]
        
        # Check if the difference is within the allowed range (1 to 3)
        if abs(diff) < 1 or abs(diff) > 3:
            return False
        
        # Determine the direction of change
        if increasing is None and decreasing is None:
            if diff > 0:
                increasing = True
            elif diff < 0:
                decreasing = True
        else:
            if (increasing and diff <= 0) or (decreasing and diff >= 0):
                return False

    return True

def is_safe_with_dampener(report):
    # Try removing each level one by one and check if the remaining levels are safe
    for i in range(len(report)):
        modified_report = report[:i] + report[i+1:]
        if is_safe(modified_report):
            return True
    return False

def count_safe_reports(file_path):
    safe_count = 0
    safe_with_dampener_count = 0
    
    with open(file_path, 'r') as file:
        for line in file:
            levels = list(map(int, line.strip().split()))
            if is_safe(levels):
                safe_count += 1
            if is_safe(levels) or is_safe_with_dampener(levels):
                safe_with_dampener_count += 1
    
    return safe_count, safe_with_dampener_count

# Assuming the input is stored in a file named "02.txt"
safe_reports, safe_reports_with_dampener = count_safe_reports('./data/02.txt')
print(f"Number of safe reports: {safe_reports}")
print(f"Number of safe reports with dampener: {safe_reports_with_dampener}")
