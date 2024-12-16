#!/usr/bin/env python3
import heapq
import sys

def parse_input():
    maze = []
    start_position = None
    end_position = None
    
    for row_idx, line in enumerate(sys.stdin):
        line = line.strip()
        if not line:
            break
        maze.append(list(line))
        
        # Find start and end positions
        if 'S' in line:
            start_col = line.index('S')
            start_position = (row_idx, start_col)
        if 'E' in line:
            end_col = line.index('E')
            end_position = (row_idx, end_col)
    
    return maze, start_position, end_position

def move_forward(maze, row, col, direction):
    directions = {
        'N': (-1, 0),
        'E': (0, 1),
        'S': (1, 0),
        'W': (0, -1)
    }
    
    delta_row, delta_col = directions[direction]
    new_row = row + delta_row
    new_col = col + delta_col
    
    # Check bounds and avoid walls
    if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and maze[new_row][new_col] != '#':
        return (new_row, new_col)
    
    return None

def rotate(direction, rotation):
    directions = ['N', 'E', 'S', 'W']
    current_index = directions.index(direction)
    
    if rotation == 'L':
        new_index = (current_index - 1) % 4
    elif rotation == 'R':
        new_index = (current_index + 1) % 4
    
    return directions[new_index]

def find_min_score_and_tiles(maze, start_position, end_position):
    # Priority queue (min-heap)
    pq = []
    heapq.heappush(pq, (0, 'E', start_position, [start_position]))  # Initial score, direction, position
    
    # Visited set to avoid revisiting the same state
    visited = {}
    
    # Dictionary to keep track of tiles on paths with a specific score
    paths_num = {}
    paths = {}
    min_score = float('inf')
    
    while pq:
        score, direction, position, trajectory = heapq.heappop(pq)
        if score > min_score:
            continue

        if (position, direction) in visited:
            if visited[(position, direction)] < score:
                continue
        
        visited[(position, direction)] = score
        
        # Check if we have reached the end
        if position == end_position:
            min_score = min(min_score, score)
            if min_score not in paths:
                paths[min_score] = set()
                paths_num[min_score] = 0
            paths[min_score].update(trajectory)
            paths_num[min_score] += 1
            continue
        
        # Try rotating left and right without moving
        for rotation in ['L', 'R']:
            new_direction = rotate(direction, rotation)
            heapq.heappush(pq, (score + 1000, new_direction, position, list(trajectory)))
        
        # Try moving forward
        new_position = move_forward(maze, *position, direction)
        if new_position:
            heapq.heappush(pq, (score + 1, direction, new_position, list(trajectory) + [new_position]))
    
    # Find unique tiles on best paths with the minimum score
    tiles_on_best_paths = paths[min_score] if min_score in paths else []
    
    return min_score, len(tiles_on_best_paths)

def main():
    maze, start_position, end_position = parse_input()
    min_score, unique_tile_count = find_min_score_and_tiles(maze, start_position, end_position)
    
    print("Minimum score to reach the end:", min_score)
    print("Number of unique tiles on best paths:", unique_tile_count)

if __name__ == "__main__":
    main()