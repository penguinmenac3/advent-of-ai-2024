package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
)

type HashEntry struct {
	key   int
	value int
}

type HashMap struct {
	entries [1000]HashEntry // Initial size for collision resolution
	size    int
}

func (m *HashMap) init() {
	for i := range m.entries {
		m.entries[i].key = -1
	}
	m.size = 0
}

func hash(key int) int {
	return abs(key) % 1000
}

func (m *HashMap) insert(key, value int) {
	index := hash(key)
	for m.entries[index].key != -1 && m.entries[index].key != key {
		index = (index + 1) % 1000 // Linear probing
	}
	m.entries[index].key = key
	m.entries[index].value = value
}

func (m *HashMap) find(key int) int {
	index := hash(key)
	for m.entries[index].key != -1 && m.entries[index].key != key {
		index = (index + 1) % 1000 // Linear probing
	}
	if m.entries[index].key == key {
		return m.entries[index].value
	}
	return 0
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func main() {
	var left, right int
	leftList := make([]int, 0)
	rightList := make([]int, 0)
	frequencyMap := new(HashMap)
	frequencyMap.init()

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		fmt.Sscanf(scanner.Text(), "%d %d", &left, &right)
		leftList = append(leftList, left)
		rightList = append(rightList, right)
		frequencyMap.insert(right, frequencyMap.find(right)+1)
	}

	sort.Ints(leftList)
	sort.Ints(rightList)

	totalDistance := 0
	for i := 0; i < len(leftList) && i < len(rightList); i++ {
		totalDistance += abs(leftList[i] - rightList[i])
	}

	similarityScore := int64(0)
	for _, num := range leftList {
		count := frequencyMap.find(num)
		if count > 0 {
			similarityScore += int64(num) * int64(count)
		}
	}

	fmt.Printf("Total Distance: %d\n", totalDistance)
	fmt.Printf("Similarity Score: %d\n", similarityScore)
}