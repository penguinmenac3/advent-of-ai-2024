01.run: 01.cpp
	g++ $< -o $@

# Clean rule to remove the executable
clean:
	rm -f *.run

.PHONY: clean
