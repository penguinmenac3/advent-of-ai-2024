#!/usr/bin/env python3
def parse_input():
    grid = []
    while True:
        try:
            line = input().strip()
            if not line:
                break
            grid.append(list(map(int, line)))
        except EOFError:
            break
    return grid

def is_valid_move(x, y, grid, visited, current_height):
    rows, cols = len(grid), len(grid[0])
    if 0 <= x < rows and 0 <= y < cols and not visited[x][y] and grid[x][y] == current_height + 1:
        return True
    return False

def dfs(x, y, grid, visited, bitmasks):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    rows, cols = len(grid), len(grid[0])
    
    if grid[x][y] == 9:
        # Mark the path in the bitmask for height 9
        key = x * cols + y
        bitmasks[grid[x][y]][key] = bitmasks[grid[x][y]].get(key, 0) + 1
        return
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid_move(nx, ny, grid, visited, grid[x][y]):
            visited[nx][ny] = True
            dfs(nx, ny, grid, visited, bitmasks)
            visited[nx][ny] = False

def calculate_trailhead_score_and_rating(trailhead, grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    bitmasks = [{} for _ in range(10)]  # Bitmask for each height from 0 to 9
    
    visited[trailhead[0]][trailhead[1]] = True
    dfs(trailhead[0], trailhead[1], grid, visited, bitmasks)
    
    score = sum(len(bitmask) for bitmask in bitmasks[1:])  # Count distinct paths reaching heights 1 to 9
    rating = sum(sum(bitmask.values()) for bitmask in bitmasks)  # Sum of all distinct paths
    
    return score, rating

def main():
    grid = parse_input()
    trailheads = [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 0]
    
    total_score = 0
    total_rating = 0
    
    for trailhead in trailheads:
        score, rating = calculate_trailhead_score_and_rating(trailhead, grid)
        total_score += score
        total_rating += rating
    
    print(total_score)  # Sum of scores
    print(total_rating)  # Sum of ratings

if __name__ == "__main__":
    main()