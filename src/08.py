import sys

def parse_input():
    lines = sys.stdin.read().strip().split('\n')
    grid = [list(line.strip()) for line in lines]
    return grid

def find_antinodes(grid):
    antinode_positions = set()
    antinode_positions_with_harmonics = set()
    freq_to_positions = {}

    # Populate the frequency dictionary with antenna positions
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            char = grid[i][j]
            if char != '.':
                if char not in freq_to_positions:
                    freq_to_positions[char] = []
                freq_to_positions[char].append((i, j))

    # Calculate antinodes for each frequency
    for freq, positions in freq_to_positions.items():
        for i in range(len(positions)):
            x1, y1 = positions[i]
            for j in range(i + 1, len(positions)):
                x2, y2 = positions[j]
                
                # Calculate differences
                dx, dy = x2 - x1, y2 - y1

                # Check if one is twice as far away in any direction
                antinode_pos1 = (x1 - dx, y1 - dy)
                antinode_pos2 = (x2 + dx, y2 + dy)
                
                if 0 <= antinode_pos1[0] < rows and 0 <= antinode_pos1[1] < cols:
                    antinode_positions.add(antinode_pos1)
                if 0 <= antinode_pos2[0] < rows and 0 <= antinode_pos2[1] < cols:
                    antinode_positions.add(antinode_pos2)

                antinode_pos = (x1, y1)
                while 0 <= antinode_pos[0] < rows and 0 <= antinode_pos[1] < cols:
                    antinode_positions_with_harmonics.add(antinode_pos)
                    antinode_pos = (antinode_pos[0] - dx, antinode_pos[1] - dy)
                
                antinode_pos = (x2, y2)
                while 0 <= antinode_pos[0] < rows and 0 <= antinode_pos[1] < cols:
                    antinode_positions_with_harmonics.add(antinode_pos)
                    antinode_pos = (antinode_pos[0] + dx, antinode_pos[1] + dy)

    return antinode_positions, antinode_positions_with_harmonics

def main():
    grid = parse_input()
    part1, part2 = find_antinodes(grid)
    print(len(part1))
    print(len(part2))

if __name__ == "__main__":
    main()