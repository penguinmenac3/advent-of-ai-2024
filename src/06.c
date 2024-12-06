#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ROWS 131
#define MAX_COLS 131

typedef struct {
    int x;
    int y;
    int direction;
} Position;

void simulate_guard(char map_data[MAX_ROWS][MAX_COLS], int rows, int cols, Position start_pos, int obstacle_x, int obstacle_y, int visited[MAX_ROWS * MAX_COLS][4], int* is_loop) {
    int x = start_pos.x, y = start_pos.y, direction = start_pos.direction;
    int flat_visited_size = rows * cols;

    // Directions: up, right, down, left
    static const int dx[] = {-1, 0, 1, 0};
    static const int dy[] = {0, 1, 0, -1};

    visited[x * cols + y][direction] = 1;
    while (1) {
        int nx = x + dx[direction];
        int ny = y + dy[direction];

        if (!(nx >= 0 && nx < rows && ny >= 0 && ny < cols)) {
            // Out of bounds, stop simulation
            break;
        }

        if ((map_data[nx][ny] == '#' || (nx == obstacle_x && ny == obstacle_y))) {
            // Turn right: increment direction by 1 and take modulo 4
            direction = (direction + 1) % 4;
        } else {
            // Move forward
            x = nx;
            y = ny;
            int flat_index_new = x * cols + y;

            if (visited[flat_index_new][direction]) {
                // Loop detected, stop simulation
                if (is_loop != NULL) {
                    *is_loop = 1;
                }
                break;
            } else {
                visited[flat_index_new][direction] = 1;
            }
        }
    }
}

int main() {
    char map_data[MAX_ROWS][MAX_COLS];
    int rows = 0, cols = 0;

    char *buffer = NULL;
    size_t len = 0;
    while ((getline(&buffer, &len, stdin)) != -1) {
        if (cols == 0) {
            for (int i = 0; buffer[i] != '\n'; i++) {
                cols++;
            }
        }
        strncpy(map_data[rows], buffer, cols);
        rows++;
    }

    // Find guard's initial position and direction
    Position start_pos;
    int found_guard = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (map_data[i][j] == '^') {
                start_pos.x = i;
                start_pos.y = j;
                start_pos.direction = 0;
                found_guard = 1;
                break;
            }
        }
        if (found_guard) {
            break;
        }
    }

    if (!found_guard) {
        printf("No guard found!\n");
        return 1;
    }

    // Find all reachable positions
    int visited[MAX_ROWS * MAX_COLS][4] = {0};
    simulate_guard(map_data, rows, cols, start_pos, -1, -1, visited, NULL);

    // Find the number of reachable positions
    int reachable_positions_count = 0;
    for (int i = 0; i < rows * cols; i++) {
        if (visited[i][0] || visited[i][1] || visited[i][2] || visited[i][3]) {
            reachable_positions_count++;
        }
    }
    printf("Number of reachable positions: %d\n", reachable_positions_count);

    // Extract all unique (x, y) positions that were visited
    Position* reachable_positions = (Position*)malloc(reachable_positions_count * sizeof(Position));
    reachable_positions_count = 0;
    for (int i = 0; i < rows * cols; i++) {
        if (visited[i][0] || visited[i][1] || visited[i][2] || visited[i][3]) {
            reachable_positions[reachable_positions_count].x = i / cols;
            reachable_positions[reachable_positions_count].y = i % cols;
            reachable_positions_count++;
        }
    }

    // Count loop-inducing positions
    int loop_count = 0;
    for (int i = 0; i < reachable_positions_count; i++) {
        int is_loop = 0;
        memset(visited, 0, sizeof(visited));
        simulate_guard(map_data, rows, cols, start_pos, reachable_positions[i].x, reachable_positions[i].y, visited, &is_loop);
        if (is_loop) {
            loop_count++;
        }
    }

    printf("Number of positions where obstacles would create loops: %d\n", loop_count);

    // Free allocated memory
    free(reachable_positions);

    return 0;
}