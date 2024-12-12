import sys
DEBUG = False


def accumulate_region(grid, visited, x, y):
    n, m = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    area = 1
    perimeter = 0
    sides = {
        k: []
        for k in range(len(directions))
    }

    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        visited[cx][cy] = True

        for idx, (dx, dy) in enumerate(directions):
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < n and 0 <= ny < m:
                if grid[nx][ny] == grid[cx][cy]:
                    if not visited[nx][ny] and (nx, ny) not in stack:
                        stack.append((nx, ny))
                        area += 1
                else:
                    perimeter += 1
                    sides[idx].append((cx, cy))
            else:
                perimeter += 1
                sides[idx].append((cx, cy))

    # print(f"Raw Sides: {sides}")
    # Sort and merge adjacent sides for each direction
    merged_sides = []
    for idx in range(len(directions)):
        if not sides[idx]:
            continue

        # Sort sides by their x or y coordinate based on the direction
        if directions[idx][0] == 0:  # left or right edge, sort by x then by y
            sides[idx].sort(key=lambda pos: pos[0])
            sides[idx].sort(key=lambda pos: pos[1])
        else:  # up or down edge, sort by y then by x
            sides[idx].sort(key=lambda pos: pos[1])
            sides[idx].sort(key=lambda pos: pos[0])

        current_segment = [sides[idx][0]]
        # print(idx, sides[idx][0])
        for i in range(1, len(sides[idx])):
            # print(idx, sides[idx][i])
            if (directions[idx][0] == 0 and current_segment[-1][0] + 1 == sides[idx][i][0] and current_segment[-1][1] == sides[idx][i][1]) or \
                (directions[idx][1] == 0 and current_segment[-1][1] + 1 == sides[idx][i][1] and current_segment[-1][0] == sides[idx][i][0]):
                current_segment.append(sides[idx][i])
            else:
                merged_sides.append((idx, current_segment))
                current_segment = [sides[idx][i]]
        merged_sides.append((idx, current_segment))
    # print(f"Merged ({len(merged_sides)}): {merged_sides}")
    if DEBUG:
        print(f"Region: {grid[x][y]}, Area: {area}, Perimeter: {perimeter}, Sides: {len(merged_sides)}")
    return area, perimeter, len(merged_sides)


def count_regions(grid):
    n, m = len(grid), len(grid[0])
    visited = [[False] * m for _ in range(n)]
    
    total_cost_perimeter = 0
    total_cost_sides = 0
    for i in range(n):
        for j in range(m):
            if not visited[i][j]:
                area, perimeter, sides = accumulate_region(grid, visited, i, j)
                total_cost_perimeter += area * perimeter
                total_cost_sides += area * sides     # For Part 2

    return total_cost_perimeter, total_cost_sides

def main():
    input = sys.stdin.read().strip().split('\n')
    
    map_data = [list(row) for row in input]
    
    a, b = count_regions(map_data)

    print(a)
    print(b)

if __name__ == "__main__":
    main()
