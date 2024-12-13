#!/usr/bin/env python3
import sys

def read_input():
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

def topological_sort(rules, pages):
    from collections import defaultdict, deque
    
    # Create a graph
    graph = defaultdict(list)
    indegree = defaultdict(int)
    
    for x, y in rules:
        if x in pages and y in pages:
            graph[x].append(y)
            indegree[y] += 1

    # Find nodes with no incoming edges
    queue = deque([page for page in pages if indegree[page] == 0])
    sorted_order = []

    while queue:
        node = queue.popleft()
        sorted_order.append(node)
        
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_order

def main():
    rules, updates = read_input()
    total_middle_sum_correct = 0
    total_middle_sum_incorrect = 0
    
    for update in updates:
        if is_correct_order(update, rules):
            middle_page = update[len(update) // 2]
            total_middle_sum_correct += middle_page
        else:
            sorted_update = topological_sort(rules, update)
            middle_page = sorted_update[len(sorted_update) // 2]
            total_middle_sum_incorrect += middle_page

    print(total_middle_sum_correct)
    print(total_middle_sum_incorrect)

if __name__ == "__main__":
    main()