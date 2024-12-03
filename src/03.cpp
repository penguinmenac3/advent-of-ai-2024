#include <iostream>
#include <string>
#include <cctype>

int main() {
    std::ios::sync_with_stdio(false); // Disable synchronization between C++ and C I/O streams
    std::cin.tie(nullptr);             // Untie cin from cout to allow asynchronous reading

    std::string input;
    
    int result = 0;
    int resultAll = 0;
    bool mul_enabled = true; // Initially, all mul instructions are enabled

    while (std::getline(std::cin, input)) {
        const char* p = input.c_str();
        const char* end = p + input.length();

        while (p < end) {
            if (*p == 'd' && *(p+1) == 'o') {
                // Enable multiplication or disable multiplication
                if (*(p+2) == '(' && *(p+3) == ')') {
                    mul_enabled = true;
                    p += 4; // Move past "do("
                } else if (*(p+2) == 'n' && *(p+3) == '\'' && *(p+4) == 't' && *(p+5) == '(' && *(p+6) == ')') {
                    mul_enabled = false;
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
                    while (p < end && std::isdigit(*p)) {
                        num1 = num1 * 10 + (*p - '0');
                        ++p;
                    }

                    // Check for comma
                    if (p < end && *p == ',') {
                        ++p; // Skip ','

                        // Find the second number
                        int num2 = 0;
                        while (p < end && std::isdigit(*p)) {
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

    std::cout << "The sum of all multiplication results is: " << resultAll << std::endl;
    std::cout << "The sum of all enabled multiplication results is: " << result << std::endl;
    return 0;
}