#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

bool backtrack(int index, long long current_result, long long test_value, const long long *numbers, int length, bool include_concat) {
    if (current_result > test_value) {
        return false;
    }

    if (index >= length) {
        return current_result == test_value;
    }

    bool matches = backtrack(index + 1, current_result + numbers[index], test_value, numbers, length, include_concat)
        || backtrack(index + 1, current_result * numbers[index], test_value, numbers, length, include_concat);

    if (include_concat) {
        long long mul = 1;
        long long tmp = numbers[index];
        while (tmp > 0) {
            tmp /= 10;
            mul *= 10;
        }
        long long concatenated_result = current_result * mul + numbers[index];
        return matches || backtrack(index + 1, concatenated_result, test_value, numbers, length, include_concat);
    }

    return matches;
}

long long calculate_total_calibration_result(const char *input_lines[], int num_lines, bool include_concat) {
    long long total_calibration_result = 0;

    for (int i = 0; i < num_lines; ++i) {
        const char *line = input_lines[i];

        const char *delim = strchr(line, ':');
        if (!delim) continue;

        // Extract test value
        long long test_value = strtoll(line, NULL, 10);

        // Extract digits from the concatenated numbers string
        const char *start = delim + 2;
        int count = 0;
        long long numbers[32]; // Assuming a reasonable number of numbers per line
        
        while (sscanf(start, "%lld", &numbers[count]) == 1) {
            
            // Move the start pointer to the end of the current number
            char num_str[32];
            snprintf(num_str, sizeof(num_str), "%lld", numbers[count]);
            start += strlen(num_str);
            
            // Skip any whitespace after the current number
            while (*start && (*start == ' ' || *start == '\t')) {
                ++start;
            }
            
            ++count;
        }

        // Start backtracking from the second number
        if (count > 0) { // Ensure there are enough numbers to start backtracking
            if (backtrack(1, numbers[0], test_value, numbers, count, include_concat)) {
                total_calibration_result += test_value;
            }
        } else {
            printf("No valid numbers found for line %d\n", i + 1);
        }
    }

    return total_calibration_result;
}

int main() {
    char input_buffer[4096];
    int num_lines = 0;
    char *input_lines[1000]; // Assuming a reasonable number of lines

    // Read all lines from standard input
    while (fgets(input_buffer, sizeof(input_buffer), stdin) != NULL) {
        // Remove newline character if present
        size_t len = strlen(input_buffer);
        if (len > 0 && input_buffer[len - 1] == '\n') {
            input_buffer[len - 1] = '\0';
        }

        // Tokenize the line into words
        char *line = strtok(input_buffer, "\n");
        while (line) {
            input_lines[num_lines++] = strdup(line); // Duplicate the string to avoid issues with input_buffer reuse
            line = strtok(NULL, "\n");
        }
    }

    // Calculate results for both parts
    long long part1_result = calculate_total_calibration_result((const char **)input_lines, num_lines, false);
    printf("Part 1 Result: %lld\n", part1_result);

    long long part2_result = calculate_total_calibration_result((const char **)input_lines, num_lines, true);
    printf("Part 2 Result: %lld\n", part2_result);

    // Free dynamically allocated memory
    for (int i = 0; i < num_lines; ++i) {
        free(input_lines[i]);
    }

    return 0;
}