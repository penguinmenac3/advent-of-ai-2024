#include <iostream>
#include <sstream>
#include <vector>
#include <string>

bool backtrack(int index, long long current_result, long long test_value, const std::vector<long long>& numbers, bool include_concat) {
    if (current_result > test_value) {
        return false;
    }

    if (index >= numbers.size()) {
        return current_result == test_value;
    }

    bool matches = backtrack(index + 1, current_result + numbers[index], test_value, numbers, include_concat)
        || backtrack(index + 1, current_result * numbers[index], test_value, numbers, include_concat);

    if (include_concat) {
        std::string concatenated_result_str = std::to_string(current_result) + std::to_string(numbers[index]);
        long long concatenated_result = std::stoll(concatenated_result_str);
        return matches || backtrack(index + 1, concatenated_result, test_value, numbers, include_concat);
    }

    return matches;
}

long long calculate_total_calibration_result(const std::vector<std::string>& input_lines, bool include_concat) {
    long long total_calibration_result = 0;

    for (const auto& line : input_lines) {
        size_t delim_pos = line.find(':');
        if (delim_pos == std::string::npos) continue;

        // Extract test value
        long long test_value = std::stoll(line.substr(0, delim_pos));

        // Extract digits from the concatenated numbers string
        std::vector<long long> numbers;
        std::istringstream number_stream(line.substr(delim_pos + 2));
        std::string number_str;
        
        while (number_stream >> number_str) {
            long long num = std::stoll(number_str);
            numbers.push_back(num);
        }

        // Start backtracking from the second number
        if (!numbers.empty()) { // Ensure there are enough numbers to start backtracking
            if (backtrack(1, numbers[0], test_value, numbers, include_concat)) {
                total_calibration_result += test_value;
            }
        } else {
            std::cerr << "No valid numbers found" << std::endl;
        }
    }

    return total_calibration_result;
}

int main() {
    std::ios::sync_with_stdio(false); // Disable synchronization between C++ and C I/O streams
    std::cin.tie(nullptr);             // Untie cin from cout to allow asynchronous reading

    std::vector<std::string> input_lines;
    std::string line;

    // Read all lines from standard input
    while (std::getline(std::cin, line)) {
        if (!line.empty()) { // Ensure we don't add empty lines
            input_lines.push_back(line);
        }
    }

    // Calculate results for both parts
    long long part1_result = calculate_total_calibration_result(input_lines, false);
    std::cout << "Part 1 Result: " << part1_result << std::endl;

    long long part2_result = calculate_total_calibration_result(input_lines, true);
    std::cout << "Part 2 Result: " << part2_result << std::endl;

    return 0;
}