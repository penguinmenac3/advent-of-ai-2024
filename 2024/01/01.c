#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int key;
    int value;
} HashEntry;

typedef struct {
    HashEntry entries[1000]; // Initial size for collision resolution
    size_t size;
} HashMap;

static inline void hashmap_init(HashMap* map) {
    memset(map->entries, -1, sizeof(map->entries)); // Mark all as unused
    map->size = 0;
}

static inline int hash(int key) {
    return abs(key) % 1000; // Use a fixed size for simplicity in this example
}

static inline void hashmap_insert(HashMap* map, int key, int value) {
    int index = hash(key);
    while (map->entries[index].key != -1 && map->entries[index].key != key) {
        index = (index + 1) % 1000; // Linear probing
    }
    map->entries[index].key = key;
    map->entries[index].value = value;
}

static inline int hashmap_find(HashMap* map, int key) {
    int index = hash(key);
    while (map->entries[index].key != -1 && map->entries[index].key != key) {
        index = (index + 1) % 1000; // Linear probing
    }
    return (map->entries[index].key == key) ? map->entries[index].value : 0;
}

int compare(const void* a, const void* b) {
    return (*(const int*)a - *(const int*)b);
}

int main() {
    int left, right;
    size_t leftSize = 0, rightSize = 0;
    int* leftList = NULL;
    int* rightList = NULL;
    HashMap frequencyMap;

    hashmap_init(&frequencyMap);

    // Read each pair of numbers directly into variables
    while (scanf("%d %d", &left, &right) == 2) {
        if (leftSize == 0) {
            leftList = malloc(sizeof(int));
        } else {
            leftList = realloc(leftList, (leftSize + 1) * sizeof(int));
        }
        leftList[leftSize++] = left;

        if (rightSize == 0) {
            rightList = malloc(sizeof(int));
        } else {
            rightList = realloc(rightList, (rightSize + 1) * sizeof(int));
        }
        rightList[rightSize++] = right;
        
        hashmap_insert(&frequencyMap, right, hashmap_find(&frequencyMap, right) + 1);
    }

    // Sort both lists for total distance calculation
    qsort(leftList, leftSize, sizeof(int), compare);
    qsort(rightList, rightSize, sizeof(int), compare);

    // Calculate the total distance
    int totalDistance = 0;
    for (size_t i = 0; i < leftSize && i < rightSize; ++i) {
        totalDistance += abs(leftList[i] - rightList[i]);
    }

    // Calculate the similarity score
    long long similarityScore = 0;
    for (size_t i = 0; i < leftSize; ++i) {
        int num = leftList[i];
        int count = hashmap_find(&frequencyMap, num);
        if (count > 0) {
            similarityScore += (long long)num * count;
        }
    }

    // Output the results
    printf("Total Distance: %d\n", totalDistance);
    printf("Similarity Score: %lld\n", similarityScore);

    // Free allocated memory
    free(leftList);
    free(rightList);

    return 0;
}