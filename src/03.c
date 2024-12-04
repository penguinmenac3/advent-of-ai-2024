#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int main() {
    int result = 0;
    int resultAll = 0;
    int mul_enabled = 1; // Initially, all mul instructions are enabled

    char* input = NULL;
    size_t len = 0;
    ssize_t read;

    while ((read = getline(&input, &len, stdin)) != -1) {
        const char* p = input;
        const char* end = input + read - 1; // Exclude the newline character

        while (p < end) {
            if (*p == 'd' && *(p+1) == 'o') {
                // Enable multiplication or disable multiplication
                if (*(p+2) == '(' && *(p+3) == ')') {
                    mul_enabled = 1;
                    p += 4; // Move past "do("
                } else if (*(p+2) == 'n' && *(p+3) == '\'' && *(p+4) == 't' && *(p+5) == '(' && *(p+6) == ')') {
                    mul_enabled = 0;
                    p += 7; // Move past "don't()"
                } else {
                    p += 2;
                }
            } else if (*p == 'm' && *(p+1) == 'u' && *(p+2) == 'l') {
                // Check if 'mul' is followed by '('
                p += 3; // Move past "mul"
                if (p < end && *p == '(') {
                    ++p; // Skip '('

                    // Find the first number
                    int num1 = 0;
                    while (p < end && isdigit(*p)) {
                        num1 = num1 * 10 + (*p - '0');
                        ++p;
                    }

                    // Check for comma
                    if (p < end && *p == ',') {
                        ++p; // Skip ','

                        // Find the second number
                        int num2 = 0;
                        while (p < end && isdigit(*p)) {
                            num2 = num2 * 10 + (*p - '0');
                            ++p;
                        }

                        // Check for closing parenthesis
                        if (p < end && *p == ')') {
                            int product = num1 * num2;
                            resultAll += product;
                            if (mul_enabled) {
                                result += product;
                            }
                            ++p; // Skip ')'
                        } else {
                            // Malformed input, skip to the next potential 'm', 'd', or end of line
                            while (p < end && *p != 'm' && *p != 'd') {
                                ++p;
                            }
                        }
                    } else {
                        // Malformed input, skip to the next potential 'm', 'd', or end of line
                        while (p < end && *p != 'm' && *p != 'd') {
                            ++p;
                        }
                    }
                } else {
                    // Malformed input, skip to the next potential 'm', 'd', or end of line
                    while (p < end && *p != 'm' && *p != 'd') {
                        ++p;
                    }
                }
            } else {
                ++p;
            }
        }
    }

    free(input); // Free dynamically allocated memory

    printf("The sum of all multiplication results is: %d\n", resultAll);
    printf("The sum of all enabled multiplication results is: %d\n", result);
    return 0;
}