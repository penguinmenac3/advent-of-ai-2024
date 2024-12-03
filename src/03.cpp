#include <iostream>
#include <string>
#include <regex>

std::pair<int, int> extract_and_sum_multiplications(std::istream& input) {
    // Read the content from the stream
    std::string content((std::istreambuf_iterator<char>(input)), std::istreambuf_iterator<char>());

    // Regular expression pattern for valid mul(X,Y) instructions and do()/don't() instructions
    std::regex pattern(R"(mul\((\d+),(\d+)\)|do\(\)|don\'t\(\))");

    // Find all matches in the content
    auto words_begin = std::sregex_iterator(content.begin(), content.end(), pattern);
    auto words_end = std::sregex_iterator();

    // Initialize the sum of results for both cases
    int total_sum_unconditional = 0;
    int total_sum_conditional = 0;

    // Flag to track if mul instructions are enabled
    bool is_enabled = true;

    // Process matches
    for (std::sregex_iterator i = words_begin; i != words_end; ++i) {
        std::smatch match = *i;
        std::string match_str = content.substr(match.position(), match.length());

        if (match_str == "do()") {
            is_enabled = true;
        } else if (match_str == "don't()") {
            is_enabled = false;
        } else {
            // Extract numbers from the match
            int x, y;
            std::sscanf(match_str.c_str(), "mul(%d,%d)", &x, &y);
            total_sum_unconditional += x * y;
            if (is_enabled) {
                total_sum_conditional += x * y;
            }
        }
    }

    return {total_sum_unconditional, total_sum_conditional};
}

int main() {
    try {
        // Calculate the sum of all multiplication results and conditional sums
        auto [unconditional_result, conditional_result] = extract_and_sum_multiplications(std::cin);

        // Print the result
        std::cout << "The sum of all multiplication results is: " << unconditional_result << std::endl;
        std::cout << "The sum of all enabled multiplication results is: " << conditional_result << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}