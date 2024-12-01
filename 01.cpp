#include <iostream>
#include <fstream>
#include <vector>
#include <sstream>
#include <algorithm>
#include <unordered_map>

int main() {
    std::ifstream file("01.txt");
    if (!file.is_open()) {
        std::cerr << "Failed to open the file." << std::endl;
        return 1;
    }

    std::string line;
    std::vector<int> leftList, rightList;
    std::unordered_map<int, int> frequencyMap;

    // Read each line and extract pairs of numbers
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        int left, right;
        if (iss >> left >> right) {
            leftList.push_back(left);
            rightList.push_back(right);
            frequencyMap[right]++;
        }
    }

    // Sort both lists for total distance calculation
    std::sort(leftList.begin(), leftList.end());
    std::sort(rightList.begin(), rightList.end());

    // Calculate the total distance
    int totalDistance = 0;
    for (size_t i = 0; i < leftList.size(); ++i) {
        totalDistance += abs(leftList[i] - rightList[i]);
    }

    // Calculate the similarity score
    long long similarityScore = 0;
    for (int num : leftList) {
        similarityScore += num * frequencyMap[num];
    }

    // Output the results
    std::cout << "Total Distance: " << totalDistance << std::endl;
    std::cout << "Similarity Score: " << similarityScore << std::endl;

    return 0;
}