import sys

def compact_disk(disk_map):
    # Parse the disk map into a list of lengths and types (file or free space)
    lengths = []
    is_file = True
    
    for char in disk_map:
        if char.isdigit():
            length = int(char)
            lengths.append((length, is_file))
            is_file = not is_file  # Alternate between file and free space
    
    # Initialize variables
    blocks = []
    file_id = 0
    
    # Create the initial block representation
    for length, file_type in lengths:
        if file_type:
            blocks.extend([file_id] * length)
            file_id += 1
        else:
            blocks.extend(['.'] * length)
    
    # Compact the disk by moving files to the leftmost free space
    lidx = 0
    ridx = len(blocks) - 1
    while ridx > lidx:
        if blocks[ridx] != '.':
            while blocks[lidx] != '.':
                if ridx <= lidx:
                    return blocks[:ridx]
                lidx += 1
            blocks[lidx] = blocks[ridx]
            blocks[ridx] = "."
            lidx += 1
        ridx -= 1
    
    return blocks[:ridx]

def calculate_checksum(compact_disk):
    checksum = 0
    for i, elem in enumerate(compact_disk):
        if elem != ".":
            checksum += i * elem
    return checksum

if __name__ == "__main__":
    # Read input from stdin
    disk_map = sys.stdin.read().strip()
    
    # Compact the disk
    compacted_disk = compact_disk(disk_map)

    # Calculate the checksum
    checksum = calculate_checksum(compacted_disk)
    
    # Print the result
    print(checksum)