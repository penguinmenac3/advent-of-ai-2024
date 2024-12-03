#include <iostream>
#include <string>
#include <cctype>

int main() {
    std::string input;
    
    int result = 0;
    int resultAll = 0;
    bool mul_enabled = true; // Initially, all mul instructions are enabled

    while (std::getline(std::cin, input)) {
        size_t i = 0;
        while (i < input.length()) {
            if (input.substr(i, 3) == "do(") {
                // Enable multiplication
                mul_enabled = true;
                i += 2; // Move index past 'do('
            } else if (input.substr(i, 7) == "don't()") {
                // Disable multiplication
                mul_enabled = false;
                i += 6; // Move index past 'don't()'
            } else if (input.substr(i, 3) == "mul") {
                // Check if 'mul' is followed by '('
                size_t j = i + 3;
                if (j < input.length() && input[j] == '(') {
                    ++j; // Skip '('

                    // Find the first number
                    int num1 = 0;
                    while (j < input.length() && std::isdigit(input[j])) {
                        num1 = num1 * 10 + (input[j] - '0');
                        ++j;
                    }

                    // Check for comma
                    if (j < input.length() && input[j] == ',') {
                        ++j; // Skip ','

                        // Find the second number
                        int num2 = 0;
                        while (j < input.length() && std::isdigit(input[j])) {
                            num2 = num2 * 10 + (input[j] - '0');
                            ++j;
                        }

                        // Check for closing parenthesis
                        if (j < input.length() && input[j] == ')') {
                            if (mul_enabled) {
                                result += num1 * num2;
                            }
                            resultAll += num1 * num2;
                        }
                    }
                }
                i += 3; // Move index past 'mul'
            } else {
                ++i; // Move to the next character
            }
        }
    }

    std::cout << "The sum of all multiplication results is: " << resultAll << std::endl;
    std::cout << "The sum of all enabled multiplication results is: " << result << std::endl;
    return 0;
}