#include <iostream>
#include <vector>
#include <algorithm>
#include <unordered_map>

int main() {
    std::ios::sync_with_stdio(false); // Disable synchronization between C++ and C I/O streams
    std::cin.tie(nullptr);             // Untie cin from cout to allow asynchronous reading

    int left, right;
    std::vector<int> leftList, rightList;
    std::unordered_map<int, int> frequencyMap;

    // Read each pair of numbers directly into variables
    while (std::cin >> left >> right) {
        leftList.push_back(left);
        rightList.push_back(right);
        frequencyMap[right]++;
    }

    // Sort both lists for total distance calculation
    std::sort(leftList.begin(), leftList.end());
    std::sort(rightList.begin(), rightList.end());

    // Calculate the total distance
    int totalDistance = 0;
    size_t size = leftList.size();
    for (size_t i = 0; i < size; ++i) {
        totalDistance += abs(leftList[i] - rightList[i]);
    }

    // Calculate the similarity score
    long long similarityScore = 0;
    for (int num : leftList) {
        if (frequencyMap.find(num) != frequencyMap.end()) {
            similarityScore += static_cast<long long>(num) * frequencyMap[num];
        }
    }

    // Output the results
    std::cout << "Total Distance: " << totalDistance << std::endl;
    std::cout << "Similarity Score: " << similarityScore << std::endl;

    return 0;
}