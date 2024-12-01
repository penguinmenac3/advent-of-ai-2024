01-cpp.run: src/01.cpp
	g++ $< -o bin/$@

01-rs.run: src/01.rs
	rustc $< -o bin/$@

all: 01-cpp.run 01-rs.run

# Clean rule to remove the executable
clean:
	rm -f *.run

.PHONY: clean
