#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to search for a word in the grid in a specific direction
int search(char** grid, int rows, int cols, const char* word, int x, int y, int dx, int dy) {
    for (int i = 0; word[i] != '\0'; ++i) {
        int nx = x + dx * i;
        int ny = y + dy * i;
        if (nx < 0 || nx >= rows || ny < 0 || ny >= cols) {
            return 0;
        }
        if (grid[nx][ny] != word[i]) {
            return 0;
        }
    }
    return 1;
}

// Function to count occurrences of a word in the grid
int count_word(char** grid, int rows, int cols, const char* word) {
    int count = 0;

    // Directions for word search: horizontal, vertical, and diagonal
    int directions[8][2] = {
        {0, 1},   // right
        {1, 0},   // down
        {1, 1},   // diagonal down-right
        {-1, 0},  // up
        {0, -1},  // left
        {-1, -1}, // diagonal up-left
        {1, -1},  // diagonal down-left
        {-1, 1}   // diagonal up-right
    };

    for (int x = 0; x < rows; ++x) {
        for (int y = 0; y < cols; ++y) {
            if (grid[x][y] == word[0]) { // Check first character of the word
                for (int i = 0; i < 8; ++i) {
                    int dx = directions[i][0];
                    int dy = directions[i][1];
                    if (search(grid, rows, cols, word, x, y, dx, dy)) {
                        count++;
                    }
                }
            }
        }
    }

    return count;
}

// Function to count occurrences of X-MAS shapes in the grid
int count_xmas_shapes(char** grid, int rows, int cols) {
    int count = 0;

    // Generate all possible orientations of the X-MAS kernel
    char kernels[4][3][3] = {
        {{'S', '.', 'M'},
         {'.', 'A', '.'},
         {'S', '.', 'M'}},
        
        {{'M', '.', 'M'},
         {'.', 'A', '.'},
         {'S', '.', 'S'}},
        
        {{'M', '.', 'S'},
         {'.', 'A', '.'},
         {'M', '.', 'S'}},
        
        {{'S', '.', 'S'},
         {'.', 'A', '.'},
         {'M', '.', 'M'}}
    };

    // Slide the kernel over the grid
    for (int i = 0; i < rows - 2; ++i) {
        for (int j = 0; j < cols - 2; ++j) { // Adjusted to cols - 3 to prevent out-of-bounds errors
            for (int k = 0; k < 4; ++k) {
                int match = 1;
                for (int ki = 0; ki < 3 && match; ++ki) {
                    for (int kj = 0; kj < 3 && match; ++kj) {
                        if (!(kernels[k][ki][kj] == '.' || grid[i + ki][j + kj] == kernels[k][ki][kj])) {
                            match = 0;
                        }
                    }
                }
                if (match) {
                    count++;
                }
            }
        }
    }

    return count;
}

int main() {
    char* line = NULL;
    size_t len = 0;
    ssize_t read;
    int rows = 0, cols = 0;
    char** grid = NULL;

    // Read the grid from stdin
    while ((read = getline(&line, &len, stdin)) != -1) {
        if (read > 1 && line[read - 1] == '\n') {
            line[read - 1] = '\0';
            read--;
        }
        if (cols == 0 && read > 0) {
            cols = read;
        }
        grid = realloc(grid, (rows + 1) * sizeof(char*));
        grid[rows] = malloc(cols * sizeof(char));
        strncpy(grid[rows], line, cols);
        rows++;
    }

    free(line);

    const char* word = "XMAS";
    int part1_result = count_word(grid, rows, cols, word);
    int part2_result = count_xmas_shapes(grid, rows, cols);

    printf("Part 1: %d\n", part1_result);
    printf("Part 2: %d\n", part2_result);

    // Free allocated memory
    for (int i = 0; i < rows; ++i) {
        free(grid[i]);
    }
    free(grid);

    return 0;
}