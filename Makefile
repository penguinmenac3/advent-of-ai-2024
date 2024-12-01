01.run: 01.cpp
	g++ $< -o $@

01.rust.run: 01.rs
	rustc $< -o $@

all: 01.run 01.rust.run

# Clean rule to remove the executable
clean:
	rm -f *.run

.PHONY: clean
