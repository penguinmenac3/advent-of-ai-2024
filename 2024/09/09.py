#!/usr/bin/env python3
import sys

def parse_disk_map(disk_map):
    # Parse the disk map into a list of lengths and types (file or free space)
    lengths = []
    is_file = True
    
    for char in disk_map:
        if char.isdigit():
            length = int(char)
            lengths.append((length, is_file))
            is_file = not is_file  # Alternate between file and free space
    return lengths

def compact_disk_by_block(lengths):
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
    
    # Two pointers to manage the leftmost free space and the rightmost block
    lidx = 0
    ridx = len(blocks) - 1
    
    while ridx > lidx:
        if blocks[ridx] != '.':
            while lidx < len(blocks) and blocks[lidx] != '.':
                lidx += 1
            if lidx >= ridx:
                break
            # Swap the rightmost block with the leftmost free space
            blocks[lidx], blocks[ridx] = blocks[ridx], blocks[lidx]
            lidx += 1
        ridx -= 1
    
    return blocks[:ridx + 1]

def compact_disk_by_files(lengths):
    files = []
    free_space = []
    file_id = 0
    start = 0
    for length, file_type in lengths:
        if file_type:
            files.append((file_id, start, length))
            file_id += 1
        else:
            free_space.append((start, length))
        start += length
    
    for fid in range(len(files)-1, 0, -1):
        fid, fstart, flen = files[fid]
        for sid in range(len(free_space)):
            sstart, slen = free_space[sid]
            if fstart < sstart:
                break
            if flen <= slen:
                files[fid] = (fid, sstart, flen)
                if slen - flen > 0:
                    free_space[sid] = (sstart + flen, slen - flen)
                else:
                    del free_space[sid]
                break
    return files


def calculate_checksum(compact_disk):
    checksum = 0
    for i, elem in enumerate(compact_disk):
        if elem != ".":
            checksum += i * elem
    return checksum

def calculate_checksum_files(files):
    checksum = 0
    for fid, fstart, flen in files:
        for i in range(fstart, fstart+flen):
            checksum += i * fid
    return checksum


if __name__ == "__main__":
    # Read input from stdin
    disk_map = sys.stdin.read().strip()

    # Parse the disk map into a list of lengths and types (file or free space)
    lengths = parse_disk_map(disk_map)
    
    # Compact the disk by block
    compacted_disk = compact_disk_by_block(lengths)
    checksum = calculate_checksum(compacted_disk)
    print(checksum)

    # Compact the disk by file
    files = compact_disk_by_files(lengths)
    checksum = calculate_checksum_files(files)
    print(checksum)
