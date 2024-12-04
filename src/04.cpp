#include <iostream>
#include <vector>
#include <string>

using namespace std;

bool search(const vector<vector<char>>& grid, const string& word, int x, int y, int dx, int dy) {
    for (int i = 0; i < word.length(); ++i) {
        int nx = x + dx * i;
        int ny = y + dy * i;
        if (nx < 0 || nx >= grid.size() || ny < 0 || ny >= grid[0].size()) {
            return false;
        }
        if (grid[nx][ny] != word[i]) {
            return false;
        }
    }
    return true;
}

int count_word(const vector<vector<char>>& grid, const string& word) {
    int rows = grid.size();
    int cols = grid[0].size();
    int count = 0;

    // Directions for word search: horizontal, vertical, and diagonal
    vector<pair<int, int>> directions = {
        {0, 1},   // right
        {1, 0},   // down
        {1, 1},   // diagonal down-right
        {-1, 0},  // up
        {0, -1},  // left
        {-1, -1}, // diagonal up-left
        {1, -1},  // diagonal down-left
        {-1, 1}   // diagonal up-right
    };

    for (int x = 0; x < rows; ++x) {
        for (int y = 0; y < cols; ++y) {
            if (grid[x][y] == word[0]) { // Check first character of the word
                for (const auto& [dx, dy] : directions) {
                    if (search(grid, word, x, y, dx, dy)) {
                        count++;
                    }
                }
            }
        }
    }

    return count;
}

int count_xmas_shapes(const vector<vector<char>>& grid) {
    int rows = grid.size();
    int cols = grid[0].size();
    int count = 0;

    // Generate all possible orientations of the X-MAS kernel
    vector<vector<vector<char>>> kernels = {
        { {'S', '.', 'M'},
          {'.', 'A', '.'},
          {'S', '.', 'M'} },
        
        { {'M', '.', 'M'},
          {'.', 'A', '.'},
          {'S', '.', 'S'} },
        
        { {'M', '.', 'S'},
          {'.', 'A', '.'},
          {'M', '.', 'S'} },
        
        { {'S', '.', 'S'},
          {'.', 'A', '.'},
          {'M', '.', 'M'} }
    };

    // Slide the kernel over the grid
    for (int i = 0; i < rows - 2; ++i) {
        for (int j = 0; j < cols - 2; ++j) { // Adjusted to cols - 3 to prevent out-of-bounds errors
            for (const auto& kernel : kernels) {
                bool match = true;
                for (int ki = 0; ki < 3 && match; ++ki) {
                    for (int kj = 0; kj < 3 && match; ++kj) {
                        if (!(kernel[ki][kj] == '.' || grid[i + ki][j + kj] == kernel[ki][kj])) {
                            match = false;
                        }
                    }
                }
                if (match) {
                    count++;
                }
            }
        }
    }

    return count;
}

int main() {
    std::ios::sync_with_stdio(false); // Disable synchronization between C++ and C I/O streams
    std::cin.tie(nullptr);             // Untie cin from cout to allow asynchronous reading

    vector<vector<char>> grid; // Declare the grid variable
    string input;

    while (getline(cin, input)) {
        // Assuming the input is read from stdin and each line represents a row of the grid
        if (input.empty()) break; // Stop reading on empty line or EOF
        vector<char> row(input.begin(), input.end());
        grid.push_back(row);
    }

    string word = "XMAS";
    int part_one_count = count_word(grid, word);
    cout << "Part One: " << part_one_count << endl;

    int part_two_count = count_xmas_shapes(grid);
    cout << "Part Two: " << part_two_count << endl;

    return 0;
}