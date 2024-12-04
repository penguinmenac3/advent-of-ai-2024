#include <stdio.h>
#include <stdlib.h>

#define MAX_SIZE 100000

typedef struct {
    int key;
    int value;
} HashEntry;

typedef struct {
    HashEntry entries[MAX_SIZE];
    size_t size;
} HashMap;

static inline void hashmap_init(HashMap* map) {
    for (size_t i = 0; i < MAX_SIZE; ++i) {
        map->entries[i].key = -1; // Mark as unused
    }
    map->size = 0;
}

static inline int hash(int key) {
    return abs(key) % MAX_SIZE;
}

static inline void hashmap_insert(HashMap* map, int key, int value) {
    int index = hash(key);
    while (map->entries[index].key != -1 && map->entries[index].key != key) {
        index = (index + 1) % MAX_SIZE; // Linear probing
    }
    map->entries[index].key = key;
    map->entries[index].value = value;
}

static inline int hashmap_find(HashMap* map, int key) {
    int index = hash(key);
    while (map->entries[index].key != -1 && map->entries[index].key != key) {
        index = (index + 1) % MAX_SIZE; // Linear probing
    }
    return (map->entries[index].key == key) ? map->entries[index].value : 0;
}

static inline void vector_init(int* arr, size_t* size) {
    *size = 0;
}

static inline void vector_push_back(int* arr, int value, size_t* size) {
    arr[(*size)++] = value;
}

int compare(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

int main() {
    int left, right;
    int leftList[MAX_SIZE], rightList[MAX_SIZE];
    size_t leftSize = 0, rightSize = 0;
    HashMap frequencyMap;

    hashmap_init(&frequencyMap);

    // Read each pair of numbers directly into variables
    while (scanf("%d %d", &left, &right) == 2) {
        vector_push_back(leftList, left, &leftSize);
        vector_push_back(rightList, right, &rightSize);
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

    return 0;
}