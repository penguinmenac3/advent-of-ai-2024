#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <chrono>
#include <filesystem>
#include <cstdlib>

const std::string USER_TOKEN = "c7328e8d-b1be-11ef-9f73-5a22572bfb24";

int N = 10;
int N_warmup = 5;

double run_binary(std::string& binary, const std::string& day, bool debug) {
    if (day == "06") {
        N = 1;
        N_warmup = 0;
    }
    std::string infile = "./data/" + day + ".txt";
    if (debug) {
        infile = "./data/" + day + "_example.txt";
    }
    if (binary == "bin/" + day + "-py.run") {
        binary = "python src/" + day + ".py";
    }

    std::system((binary + " < " + infile).c_str());
    for (int i = 0; i < N_warmup; ++i) {
        std::system((binary + " < " + infile + " 1> /dev/null 2>& 1").c_str());
    }
    auto start_time = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i) {
        std::system((binary + " < " + infile + " 1> /dev/null 2>& 1").c_str());
    }
    auto end_time = std::chrono::high_resolution_clock::now();

    return std::chrono::duration<double, std::milli>(end_time - start_time).count() / N;
}

double measure_compilation_time(const std::string& lang, const std::string& src, const std::string& binary) {
    auto start_time = std::chrono::high_resolution_clock::now();
    if (lang == "c") {
        std::system(("gcc " + src + " -march=x86-64 -Ofast -o " + binary).c_str());
    } else if (lang == "cpp") {
        std::system(("g++ " + src + " -march=x86-64 -Ofast -o " + binary).c_str());
    } else if (lang == "rs") {
        std::system(("rustc " + src + " --target x86_64-unknown-linux-gnu -C opt-level=3 -o " + binary).c_str());
    }
    auto end_time = std::chrono::high_resolution_clock::now();

    return std::chrono::duration<double, std::milli>(end_time - start_time).count();
}

void test_day(const std::string& day, bool debug = false) {
    std::cout << "# Testing day: " << day << "\n";

    std::vector<std::string> languages;
    for (const auto& entry : std::filesystem::directory_iterator("src")) {
        if (entry.is_regular_file()) {
            std::string filename = entry.path().filename().string();
            if (filename.substr(0, 2) == day) {
                languages.push_back(filename.substr(filename.find_last_of('.') + 1));
            }
        }
    }

    for (const auto& lang : languages) {
        std::string src = "src/" + day + "." + lang;
        std::string binary = "bin/" + day + "-" + lang + ".run";

        if (std::filesystem::exists(src)) {
            std::cout << "\nTesting: " << src << "\n";
            double compilation_time = measure_compilation_time(lang, src, binary);
            double binary_execution_time = run_binary(binary, day, debug);
            std::cout << "Time for " << lang << ": "
                      << (binary_execution_time + compilation_time) << "ms (Compile: "
                      << compilation_time << "ms, Execution: "
                      << binary_execution_time << "ms)\n";
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc == 2) {
        const std::string& day = argv[1];
        test_day(day);
    } else if (argc == 3 && std::string(argv[2]) == "debug") {
        const std::string& day = argv[1];
        test_day(day, true);
    } else {
        std::cerr << "ERROR: Specify no argument to run all days or a single number for a day.\n";
        std::cerr << "    Examples:\n";
        std::cerr << "    ./test 01  # to test only day one\n";
        return 1;
    }

    return 0;
}