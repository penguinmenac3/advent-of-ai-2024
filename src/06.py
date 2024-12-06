import sys
from tqdm import tqdm

def get_neighbors(x, y):
    # Directions: up, right, down, left
    return [(x-1, y), (x, y+1), (x+1, y), (x, y-1)]

def turn_right(direction):
    # Directions are represented as indices in the neighbors list
    return (direction + 1) % 4

def simulate_guard(map_data, start_pos, obstacle_x, obstacle_y):
    rows = len(map_data)
    cols = len(map_data[0])
    x, y, direction = start_pos
    visited = {(x, y): [direction]}
    while True:
        nx, ny = get_neighbors(x, y)[direction]
        if not (0 <= nx < rows and 0 <= ny < cols):
            # Out of bounds, stop simulation
            break
        if map_data[nx][ny] == '#' or (nx, ny) == (obstacle_x, obstacle_y):
            # Turn right if there's an obstacle in front
            direction = turn_right(direction)
        else:
            # Move forward if no obstacle
            x, y = nx, ny
        if (x, y) in visited and direction in visited[(x, y)]:
            # Loop detected, stop simulation
            return True, visited
        if (x, y) not in visited:
            visited[(x, y)] = []
        visited[(x, y)].append(direction)
    return False, visited

def main():
    import sys
    input_data = sys.stdin.read().strip()
    map_data = input_data.split('\n')
    
    # Find guard's initial position and direction
    start_pos = None
    for i, row in enumerate(map_data):
        for j, char in enumerate(row):
            if char == '^':
                start_pos = (i, j, 0)
                break
        if start_pos:
            break
    
    if not start_pos:
        print("No guard found!")
        return
    
    # Find all reachable positions
    _, reachable_positions = simulate_guard(map_data, start_pos, -1, -1)
    print("Number of reachable positions:", len(reachable_positions))
    
    # Count loop-inducing positions
    loop_count = 0
    for obstacle_x, obstacle_y in tqdm(reachable_positions.keys(), desc="Placing Obstacles"):
        is_loop, _ = simulate_guard(map_data, start_pos, obstacle_x, obstacle_y)
        if is_loop:
            loop_count += 1
    
    print("Number of positions where obstacles would create loops:", loop_count)

if __name__ == "__main__":
    main()