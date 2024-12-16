use std::io::{self, BufRead};

type Length = i32;
type BlockType = i32;
type FileId = i32;

fn parse_disk_map(disk_map: &str) -> Vec<(Length, bool)> {
    let mut lengths = Vec::new();
    let mut is_file = true;

    for ch in disk_map.chars() {
        if ch.is_digit(10) {
            let length: Length = ch.to_digit(10).unwrap_or(0) as i32;
            lengths.push((length, is_file));
            is_file = !is_file; // Alternate between file and free space
        }
    }

    lengths
}

fn compact_disk_by_block(lengths: Vec<(Length, bool)>) -> Vec<BlockType> {
    let mut blocks = Vec::new();
    let mut file_id: i32 = 0;

    for (length, file_type) in lengths {
        if file_type {
            blocks.extend(vec![file_id; length as usize]);
            file_id += 1;
        } else {
            blocks.extend(vec![-1; length as usize]);
        }
    }

    let mut lidx = 0;
    let mut ridx = blocks.len() - 1;

    while ridx > lidx {
        if blocks[ridx] != -1 {
            while lidx < blocks.len() && blocks[lidx] != -1 {
                lidx += 1;
            }
            if lidx >= ridx {
                break;
            }
            // Swap the rightmost block with the leftmost free space
            blocks.swap(lidx, ridx);
            lidx += 1;
        }
        ridx -= 1;
    }

    blocks.truncate(ridx + 1);
    blocks
}

fn compact_disk_by_files(lengths: Vec<(Length, bool)>) -> Vec<(FileId, Length, Length)> {
    let mut files: Vec<(FileId, Length, Length)> = Vec::new();
    let mut free_space = Vec::new();
    let mut file_id = 0;
    let mut start = 0;

    for (length, file_type) in lengths {
        if file_type {
            files.push((file_id, start, length));
            file_id += 1;
        } else {
            free_space.push((start, length));
        }
        start += length;
    }

    for fid in (0..files.len()).rev() {
        let fstart = files[fid].1;
        let flen = files[fid].2;
        for sid in 0..free_space.len() {
            let (sstart, slen) = free_space[sid];
            if fstart < sstart {
                break;
            }
            if flen <= slen {
                files[fid] = (files[fid].0, sstart, flen);
                if slen - flen > 0 {
                    free_space[sid] = (sstart + flen, slen - flen);
                } else {
                    free_space.remove(sid);
                }
                break;
            }
        }
    }

    files
}

fn calculate_checksum(compact_disk: &[BlockType]) -> i64 {
    let mut checksum: i64 = 0;
    for (i, &elem) in compact_disk.iter().enumerate() {
        if elem != -1 {
            checksum += i as i64 * elem as i64;
        }
    }
    checksum
}

fn calculate_checksum_files(files: &[(FileId, Length, Length)]) -> i64 {
    let mut checksum: i64 = 0;
    for &(fid, fstart, flen) in files.iter() {
        for i in fstart..fstart + flen {
            checksum += i as i64 * fid as i64;
        }
    }
    checksum
}

fn main() -> io::Result<()> {
    let stdin = io::stdin();
    let mut handle = stdin.lock();
    let mut disk_map = String::new();
    handle.read_line(&mut disk_map)?;

    let lengths = parse_disk_map(disk_map.trim());
    
    // Compact the disk by block
    let compacted_disk = compact_disk_by_block(lengths.clone());
    let checksum = calculate_checksum(&compacted_disk);
    println!("{}", checksum);

    // Compact the disk by file
    let files = compact_disk_by_files(lengths);
    let checksum = calculate_checksum_files(&files);
    println!("{}", checksum);

    Ok(())
}