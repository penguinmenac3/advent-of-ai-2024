def count_word(grid, word):
    def search(word, x, y, dx, dy):
        for i in range(len(word)):
            nx, ny = x + dx * i, y + dy * i
            if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
                return False
            if grid[nx][ny] != word[i]:
                return False
        return True

    count = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            # Check all possible directions: horizontal, vertical, and both diagonals
            directions = [
                (1, 0),   # right
                (-1, 0),  # left
                (0, 1),   # down
                (0, -1),  # up
                (1, 1),   # diagonal down-right
                (-1, -1), # diagonal up-left
                (1, -1),  # diagonal down-left
                (-1, 1)   # diagonal up-right
            ]
            for dx, dy in directions:
                if search(word, x, y, dx, dy):
                    count += 1

    return count


def count_xmas_shapes(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    # Generate all possible orientations of the X-MAS kernel
    kernels = [
        [['S', '.', 'M'],
        ['.', 'A', '.'],
        ['S', '.', 'M']],

        [['M', '.', 'M'],
        ['.', 'A', '.'],
        ['S', '.', 'S']],

        [['M', '.', 'S'],
        ['.', 'A', '.'],
        ['M', '.', 'S']],

        [['S', '.', 'S'],
        ['.', 'A', '.'],
        ['M', '.', 'M']],
    ]
    
    # Slide the kernel over the grid
    for i in range(rows - 2):
        for j in range(cols - 2):
            
            for kernel in kernels:
                valid = True
                for x in range(3):
                    for y in range(3):
                        if kernel[x][y] == '.':
                            continue
                        elif grid[i+x][j+y] != kernel[x][y]:
                            valid = False
                            break
                    if not valid:
                        break
                
                if valid:
                    count += 1
    
    return count


def main():
    import sys
    input = sys.stdin.read().strip()
    
    # Split the input into lines and convert each line into a list of characters
    grid = [list(line) for line in input.split('\n')]
    
    word = "XMAS"
    part_one_count = count_word(grid, word)
    print(f"Part One: {part_one_count}")
    
    part_two_count = count_xmas_shapes(grid)
    print(f"Part Two: {part_two_count}")


if __name__ == "__main__":
    main()
