#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ROWS 131
#define MAX_COLS 131
#define TRAJECTORY_START_SIZE 20

typedef struct {
    int x;
    int y;
    int direction;
} Position;

typedef struct {
    Position* data;
    int length;
    int _data_size;
} Trajectory;

void simulate_guard(char map_data[MAX_ROWS][MAX_COLS], int rows, int cols, Position start_pos, int obstacle_x, int obstacle_y, int visited[MAX_ROWS * MAX_COLS][4], int* is_loop, Trajectory* trajectory) {
    int x = start_pos.x, y = start_pos.y, direction = start_pos.direction;
    int flat_visited_size = rows * cols;

    // Directions: up, right, down, left
    static const int dx[] = {-1, 0, 1, 0};
    static const int dy[] = {0, 1, 0, -1};

    // Allocate initial trajectory array
    if (trajectory->length == 0) {
        trajectory->length = 1;
        trajectory->data = (Position*)malloc(TRAJECTORY_START_SIZE * sizeof(Position));
        trajectory->_data_size = TRAJECTORY_START_SIZE;
        trajectory->data[0] = start_pos;
    }

    for (int idx = 0; idx < trajectory->length; idx++) {
        Position elem = trajectory->data[idx];
        visited[elem.x * cols + elem.y][elem.direction] = 1;
    }

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

                // Add new position to trajectory
                int idx = trajectory->length++;
                if (trajectory->length > trajectory->_data_size) {
                    trajectory->_data_size = trajectory->_data_size * 2;
                    trajectory->data = (Position*)realloc(trajectory->data, trajectory->_data_size * sizeof(Position));
                }
                trajectory->data[idx].x = x;
                trajectory->data[idx].y = y;
                trajectory->data[idx].direction = direction;
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
    Trajectory trajectory;
    trajectory.length = 0;
    trajectory._data_size = 0;
    trajectory.data = NULL;

    simulate_guard(map_data, rows, cols, start_pos, -1, -1, visited, NULL, &trajectory);

    // Find the number of reachable positions
    int reachable_positions_count = 0;
    int trajectory_length = trajectory.length;
    Position* reachable_positions = (Position*)malloc(trajectory_length * sizeof(Position));
    int* trajectory_lengths = (int*)malloc(trajectory_length * sizeof(int));
    memset(visited, 0, sizeof(visited));
    for (int i = 0; i < trajectory_length; i++) {
        Position current_pose = trajectory.data[i];
        int flat_index = current_pose.x * cols + current_pose.y;

        if (!visited[flat_index][0]) {
            visited[flat_index][0] = 1;
            reachable_positions[reachable_positions_count] = current_pose;
            trajectory_lengths[reachable_positions_count] = i;
            reachable_positions_count++;
        }
    }

    printf("Number of reachable positions: %d\n", reachable_positions_count);

    // Count loop-inducing positions
    int loop_count = 0;
    for (int i = reachable_positions_count-1; i > 0; i--) {
        int is_loop = 0;
        trajectory.length = trajectory_lengths[i];
        memset(visited, 0, sizeof(visited));
        simulate_guard(map_data, rows, cols, trajectory.data[trajectory_lengths[i]-1], reachable_positions[i].x, reachable_positions[i].y, visited, &is_loop, &trajectory);
        if (is_loop) {
            loop_count++;
        }
    }

    printf("Number of positions where obstacles would create loops: %d\n", loop_count);

    // Free allocated memory
    free(trajectory.data);
    free(reachable_positions);

    return 0;
}