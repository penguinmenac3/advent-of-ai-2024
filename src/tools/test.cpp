#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <chrono>
#include <filesystem>
#include <cstdlib>


double run_binary(std::string& binary, std::string& input, int N, int N_warmup) {
    for (int i = 0; i < N_warmup; ++i) {
        std::system((binary + " < " + input + " 1> /dev/null 2>& 1").c_str());
    }
    auto start_time = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i) {
        std::system((binary + " < " + input + " 1> /dev/null 2>& 1").c_str());
    }
    auto end_time = std::chrono::high_resolution_clock::now();

    return std::chrono::duration<double, std::milli>(end_time - start_time).count() / N;
}

int main(int argc, char* argv[]) {
    if (argc != 5) {
        std::cerr << "Usage: " << argv[0] << " <binary> <input> <N> <N_warmup>" << std::endl;
        return 1;
    }

    std::string binary = argv[1];
    std::string input = argv[2];

    // Convert N and N_warmup to integers
    int N, N_warmup;
    try {
        N = std::stoi(argv[3]);
        N_warmup = std::stoi(argv[4]);
    } catch (const std::invalid_argument& e) {
        std::cerr << "Error: N and N_warmup must be integers." << std::endl;
        return 1;
    }

    // Validate that N and N_warmup are non-negative
    if (N < 0 || N_warmup < 0) {
        std::cerr << "Error: N and N_warmup must be non-negative integers." << std::endl;
        return 1;
    }

    double average_time = run_binary(binary, input, N, N_warmup);
    std::cout << average_time << " ms" << std::endl;

    return 0;
}