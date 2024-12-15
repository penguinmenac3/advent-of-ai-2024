#!/usr/bin/env python3
import os
import sys
import time
import subprocess


def run_binary(binary, day, solution, debug, N = 10, N_warmup=5):
    infile = f"../{day:02d}/input.txt"
    status = "FAILED"
    if debug:
        infile = f"../{day:02d}/input_example.txt"

    start_time = time.perf_counter_ns()
    try:
        result = subprocess.run(f"{binary} < {infile}", check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True).stdout
    except subprocess.CalledProcessError as e:
        result = e.stdout
    end_time = time.perf_counter_ns()
    result = result.strip()
    if solution is None:
        print(result)
        status = "UNKNOWN"
    elif solution[0] in result and solution[1] in result:
        status = "PASSED"
    else:
        status = f"{result}\nExpected Result: {solution[0]}, {solution[1]}\nFAILED"
    if (end_time - start_time) / 1e6 > 1000:
        status = f"{status} (slow)"
        return (end_time-start_time) / 1e6, status
    elif status != "PASSED":
        return (end_time-start_time) / 1e6, status

    try:
        cmd = ["./test.run", binary, infile, str(N), str(N_warmup)]
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Parse the output to get the measured time
        average_time = float(result.stdout.strip().split(" ")[0])

        return average_time, status

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the C++ program: {e.stderr}")
        return -1, status


def measure_compilation_time(lang, src, binary):
    start_time = time.perf_counter_ns()
    if lang == "c":
        os.system(f"gcc {src} -march=x86-64 -Ofast -o {binary}")
    elif lang == "cpp":
        os.system(f"g++ {src} -march=x86-64 -Ofast -o {binary}")
    elif lang == "rs":
        os.system(f"rustc {src} --target x86_64-unknown-linux-gnu -C opt-level=3 -o {binary}")
    elif lang == "rs":
        os.system(f"go build -o {binary} -ldflags='-s -w {src}")
    elif lang == "py":
        os.system(f"chmod +x {binary}")
    end_time = time.perf_counter_ns()
    return (end_time - start_time) / 1e6


def load_solution(day):
    fname = f"../{day:02d}/solution.txt"
    if not os.path.exists(fname):
        return None
    
    with open(fname, "r") as f:
        solution = [
            line.strip()
            for line in f.read().split("\n")
        ]
    return solution


def test_day(day, debug=False):
    measure_compilation_time("cpp", "./test.cpp", "./test.run")
    solution = load_solution(day)
    print(f"# Testing day: {day}")
    languages = [f.split(".")[-1] for f in os.listdir(f"../{day:02d}") if f.startswith(f"{day:02d}") and not f.endswith(".run")]
    for lang in languages:
        src = f"../{day:02d}/{day:02d}.{lang}"
        binary = f"../{day:02d}/{day:02d}-{lang}.run"
        if lang == "py":
            binary = src
        if os.path.exists(src):
            print(f"\nTesting: {src}")
            compilation_time = measure_compilation_time(lang, src, binary)
            binary_execution_time, status = run_binary(binary, day, solution, debug=debug)
            print(f"{status} - Total: {(binary_execution_time + compilation_time):.2f}ms, Compile: {compilation_time:.2f}ms, Execution: {binary_execution_time:.2f}ms")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        test_day(int(sys.argv[1]))
    elif len(sys.argv) == 3 and sys.argv[2] == "debug":
        test_day(int(sys.argv[1]), debug=True)
    else:
        print("ERROR: Specify no argument to run all days or a single number for a day.")
        print("    Examples:")
        print("    python test.py  # for all tests")
        print("    python test.py 1  # to test only day one")
        exit(1)
