01-cpp.run: src/01.cpp
	g++ $< -o bin/$@

01-rs.run: src/01.rs
	rustc $< -o bin/$@

02-cpp.run: src/02.cpp
	g++ $< -o bin/$@

02-rs.run: src/02.rs
	rustc $< -o bin/$@

03-cpp.run: src/03.cpp
	g++ $< -o bin/$@

all: 01-cpp.run 01-rs.run 02-cpp.run 02-rs.run 03-cpp.run

# Clean rule to remove the executable
clean:
	rm -f *.run

.PHONY: clean
