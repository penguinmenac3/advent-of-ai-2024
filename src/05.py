import sys

def read_input():
    import sys
    rules = []
    updates = []

    # Read all input lines
    input_data = sys.stdin.read().strip().split('\n\n')
    if len(input_data) != 2:
        raise ValueError("Input must be split into two sections: rules and updates")

    # Parse the rules
    for line in input_data[0].splitlines():
        x, y = map(int, line.split('|'))
        rules.append((x, y))

    # Parse the updates
    for line in input_data[1].splitlines():
        pages = list(map(int, line.split(',')))
        updates.append(pages)

    return rules, updates

def is_correct_order(update, rules):
    page_index_map = {page: idx for idx, page in enumerate(update)}
    
    for x, y in rules:
        if x in page_index_map and y in page_index_map:
            if page_index_map[x] >= page_index_map[y]:
                return False
    return True

def main():
    rules, updates = read_input()
    total_middle_sum = 0
    
    for update in updates:
        if is_correct_order(update, rules):
            middle_page = update[len(update) // 2]
            total_middle_sum += middle_page

    print(total_middle_sum)

if __name__ == "__main__":
    main()