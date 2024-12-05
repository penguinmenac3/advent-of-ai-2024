import os
import sys
import time


USER_TOKEN = "c7328e8d-b1be-11ef-9f73-5a22572bfb24"

N = 10;
N_warmup = 5;

def test_all():
    for day in range(1, 25):
        test_day(day)


def run_binary(binary, day, debug):
    if binary.endswith("-py.run"):
        binary = f"python src/{day:02d}.py"
    infile = f"./data/{day:02d}.txt"
    if debug:
        infile = f"./data/{day:02d}_example.txt"
        
    os.system(f"{binary} < {infile}")
    for _ in range(N_warmup-1):
        os.system(f"{binary} < {infile} > /dev/null")
    start_time = time.perf_counter_ns()
    for _ in range(N):
        os.system(f"{binary} < {infile} > /dev/null")
    end_time = time.perf_counter_ns()
    return (end_time - start_time) / 1e6 / N_warmup


def measure_compilation_time(lang, src, binary):
    start_time = time.perf_counter_ns()
    if lang == "c":
        os.system(f"gcc {src} -march=x86-64 -Ofast -o {binary}")
    elif lang == "cpp":
        os.system(f"g++ {src} -march=x86-64 -Ofast -o {binary}")
    elif lang == "rs":
        os.system(f"rustc {src} --target x86_64-unknown-linux-gnu -C opt-level=3 -o {binary}")
    end_time = time.perf_counter_ns()
    return (end_time - start_time) / 1e6


def test_day(day, debug=False):
    print(f"# Testing day: {day}")
    languages = [f.split(".")[-1] for f in os.listdir("src") if f.startswith(f"{day:02d}")]
    for lang in languages:
        src = f"src/{day:02d}.{lang}"
        binary = f"bin/{day:02d}-{lang}.run"
        if os.path.exists(src):
            print(f"\nTesting: {src}")
            compilation_time = measure_compilation_time(lang, src, binary)
            binary_execution_time = run_binary(binary, day, debug=debug)
            print(f"Time for {lang}: {(binary_execution_time + compilation_time):.2f}ms (Compile: {compilation_time:.2f}ms, Execution: {binary_execution_time:.2f}ms)")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        test_all()
    elif len(sys.argv) == 2:
        test_day(int(sys.argv[1]))
    elif len(sys.argv) == 3 and sys.argv[2] == "debug":
        test_day(int(sys.argv[1]), debug=True)
    else:
        print("ERROR: Specify no argument to run all days or a single number for a day.")
        print("    Examples:")
        print("    python test.py  # for all tests")
        print("    python test.py 1  # to test only day one")
        exit(1)
