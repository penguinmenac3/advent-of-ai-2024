# Advent of AI

The code in this repository is 100% written with AI. It is an experiment to see how good AI is at solving simple coding problems in practice.

The human can guide the AI like a superviser and fix some syntax errors (if nescessary).

## Usage

* Open the project in a devcontainer (in vscode or docker)
* (Optional) Compile C++ tester `g++ test.cpp -o test.run`
* Develop Solution for a day (e.g. 01)
    * You can get the input and the task description using `python get.py 01` (replace 01 with the actual day)
    * Write your code in `./src/01.py` (replace 01 by actual day). You can also use `.c`, `.cpp` or `.rs`. (If you need more languages add support for them to the tester.)
    * Once you submitted your correct solution to part 1 on the website, remove the task description for the day and rerun the get.py so it can fetch part 2.
* Run/Benchmark code for a day:
    * Option A: Run using the native runner `./test.run 01`
    * Option B: Run using the python runner `python test.py 01`
