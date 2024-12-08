import sys
from tqdm import tqdm


def simulate_guard(map_data, start_pos, obstacle_x, obstacle_y, trajectory=None):
    rows = len(map_data)
    cols = len(map_data[0])
    x, y, direction = start_pos
    
    if trajectory is None:
        trajectory = [(x, y, direction)]
    
    # Create a flattened index for the visited map
    flat_visited_size = rows * cols
    visited = [None] * flat_visited_size
    for (tx, ty, td) in trajectory:
        visited[tx * cols + ty] = [td]
    
    while True:
        # Directions: up, right, down, left
        if direction == 0:
            nx, ny = x - 1, y
        elif direction == 1:
            nx, ny = x, y + 1
        elif direction == 2:
            nx, ny = x + 1, y
        elif direction == 3:
            nx, ny = x, y - 1
        
        if not (0 <= nx < rows and 0 <= ny < cols):
            # Out of bounds, stop simulation
            break
        if map_data[nx][ny] == '#' or (nx, ny) == (obstacle_x, obstacle_y):
            # Turn right: increment direction by 1 and take modulo 4
            direction = (direction + 1) % 4
        else:
            # Move forward
            x, y = nx, ny
        
        trajectory.append((x, y, direction))
        flat_index_new = x * cols + y
        
        if visited[flat_index_new] is not None and direction in visited[flat_index_new]:
            # Loop detected, stop simulation
            return True, trajectory
        else:
            if visited[flat_index_new] is None:
                visited[flat_index_new] = []
            visited[flat_index_new].append(direction)
    
    return False, trajectory

def main():
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
    _, trajectory = simulate_guard(map_data, start_pos, -1, -1)
    
    # Extract all unique (x, y) positions that were visited
    reachable_positions = []
    reachable_poses = []
    trajectory_lengths = []
    for idx, pose in enumerate(trajectory):
        if pose[:2] not in reachable_positions:
            reachable_positions.append(pose[:2])
            reachable_poses.append(pose)
            trajectory_lengths.append(idx)
    
    print("Number of reachable positions:", len(reachable_positions))
    
    # Count loop-inducing positions
    loop_count = 0
    for idx in tqdm(range(len(reachable_poses)-1, 0, -1), desc="Placing Obstacles"):
        obstacle_x, obstacle_y = reachable_positions[idx][:2]
        if (obstacle_x, obstacle_y) == start_pos[:2]:
            continue
        is_loop, _ = simulate_guard(map_data, trajectory[trajectory_lengths[idx]-1], obstacle_x, obstacle_y, trajectory[:trajectory_lengths[idx]])
        if is_loop:
            loop_count += 1
    
    print("Number of positions where obstacles would create loops:", loop_count)

if __name__ == "__main__":
    main()