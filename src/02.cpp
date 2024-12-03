#include <iostream>
#include <sstream>
#include <vector>
#include <optional>
#include <stdexcept>

bool is_safe(const std::vector<int>& report) {
    if (report.size() < 2) {
        return true;
    }

    std::optional<bool> direction; // Use std::optional to represent None in Python
    for (size_t i = 1; i < report.size(); ++i) {
        int diff = report[i] - report[i - 1];
        
        if (!(1 <= abs(diff) && abs(diff) <= 3)) {
            return false;
        }
        
        bool current_direction = diff > 0;
        if (!direction.has_value()) {
            direction = current_direction;
        } else if (direction.value() != current_direction) {
            return false;
        }
    }

    return true;
}

bool is_safe_with_dampener(const std::vector<int>& report) {
    for (size_t i = 0; i < report.size(); ++i) {
        // Create a view without the element at index i
        auto modified_report = std::vector<int>(report.begin(), report.begin() + i);
        if (i + 1 < report.size()) {
            modified_report.insert(modified_report.end(), report.begin() + i + 1, report.end());
        }
        
        if (is_safe(modified_report)) {
            return true;
        }
    }
    return false;
}

std::pair<int, int> count_safe_reports(std::istream& input) {
    int safe_count = 0;
    int safe_with_dampener_count = 0;
    
    std::string line;
    while (std::getline(input, line)) {
        std::istringstream iss(line);
        int number;
        std::vector<int> levels;
        
        while (iss >> number) {
            levels.push_back(number);
        }
        
        if (is_safe(levels)) {
            safe_count += 1;
        }
        if (is_safe(levels) || is_safe_with_dampener(levels)) {
            safe_with_dampener_count += 1;
        }
    }
    
    return {safe_count, safe_with_dampener_count};
}

int main() {
    try {
        // Enable buffered I/O for faster processing
        std::ios_base::sync_with_stdio(false);
        std::cin.tie(nullptr);

        auto [safe_count, safe_with_dampener_count] = count_safe_reports(std::cin);
        std::cout << "Safe reports: " << safe_count << std::endl;
        std::cout << "Safe reports with dampener: " << safe_with_dampener_count << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }
    
    return 0;
}