import sys

def is_valid(x, y, n, m, visited):
    return 0 <= x < n and 0 <= y < m and not visited[x][y]

def get_neighbors(x, y):
    return [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

def calculate_region_cost(map_data, x, y, n, m, visited):
    region_area = 0
    region_perimeter = 0
    queue = [(x, y)]
    
    while queue:
        cx, cy = queue.pop()
        
        if visited[cx][cy]:
            continue
        
        visited[cx][cy] = True
        region_area += 1
        
        for nx, ny in get_neighbors(cx, cy):
            if is_valid(nx, ny, n, m, visited) and map_data[nx][ny] == map_data[cx][cy]:
                queue.append((nx, ny))
            else:
                # Check boundaries or different type of plot
                if 0 <= nx < n and 0 <= ny < m and map_data[nx][ny] != map_data[cx][cy]:
                    region_perimeter += 1
                elif not (0 <= nx < n and 0 <= ny < m):
                    region_perimeter += 1
    
    return region_area * region_perimeter

def main():
    input = sys.stdin.read().strip().split('\n')
    
    n = len(input)
    m = len(input[0])
    
    map_data = [list(row) for row in input]
    visited = [[False] * m for _ in range(n)]
    total_cost = 0
    
    for i in range(n):
        for j in range(m):
            if not visited[i][j]:
                region_cost = calculate_region_cost(map_data, i, j, n, m, visited)
                total_cost += region_cost
    
    print(total_cost)

if __name__ == "__main__":
    main()