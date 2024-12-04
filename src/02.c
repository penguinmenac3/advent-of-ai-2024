#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef struct {
    int* data;
    size_t size;
    size_t capacity;
} Vector;

void vector_init(Vector* vec) {
    vec->data = NULL;
    vec->size = 0;
    vec->capacity = 0;
}

void vector_push_back(Vector* vec, int value) {
    if (vec->size >= vec->capacity) {
        vec->capacity = (vec->capacity == 0) ? 1 : vec->capacity * 2;
        vec->data = realloc(vec->data, vec->capacity * sizeof(int));
    }
    vec->data[vec->size++] = value;
}

void vector_free(Vector* vec) {
    free(vec->data);
    vec->data = NULL;
    vec->size = 0;
    vec->capacity = 0;
}

int is_safe(const Vector* report) {
    if (report->size < 2) {
        return 1; // true
    }

    int direction = 0; // Use an integer to represent direction: 0=unset, -1=down, 1=up
    for (size_t i = 1; i < report->size; ++i) {
        int diff = report->data[i] - report->data[i - 1];
        
        if (!(1 <= abs(diff) && abs(diff) <= 3)) {
            return 0; // false
        }
        
        int current_direction = (diff > 0) ? 1 : -1;
        if (direction == 0) {
            direction = current_direction;
        } else if (direction != current_direction) {
            return 0; // false
        }
    }

    return 1; // true
}

int is_safe_with_dampener(const Vector* report) {
    for (size_t i = 0; i < report->size; ++i) {
        // Create a view without the element at index i
        Vector modified_report;
        vector_init(&modified_report);
        
        for (size_t j = 0; j < report->size; ++j) {
            if (j != i) {
                vector_push_back(&modified_report, report->data[j]);
            }
        }
        
        if (is_safe(&modified_report)) {
            vector_free(&modified_report);
            return 1; // true
        }
        
        vector_free(&modified_report);
    }
    return 0; // false
}

void count_safe_reports(FILE* input, int* safe_count, int* safe_with_dampener_count) {
    *safe_count = 0;
    *safe_with_dampener_count = 0;
    
    char line[256];
    while (fgets(line, sizeof(line), input)) {
        Vector levels;
        vector_init(&levels);
        
        char* token = strtok(line, " \t\n");
        while (token) {
            int number = atoi(token);
            vector_push_back(&levels, number);
            token = strtok(NULL, " \t\n");
        }
        
        if (is_safe(&levels)) {
            (*safe_count)++;
        }
        if (is_safe(&levels) || is_safe_with_dampener(&levels)) {
            (*safe_with_dampener_count)++;
        }
        
        vector_free(&levels);
    }
}

int main() {
    int safe_count = 0;
    int safe_with_dampener_count = 0;

    count_safe_reports(stdin, &safe_count, &safe_with_dampener_count);
    
    printf("Safe reports: %d\n", safe_count);
    printf("Safe reports with dampener: %d\n", safe_with_dampener_count);

    return 0;
}