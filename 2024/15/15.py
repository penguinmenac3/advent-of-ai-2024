#!/usr/bin/env python3
import sys

# Define direction constants using complex numbers
UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1

def parse_input(input_str):
    # Split input into blocks separated by two newlines
    blocks = input_str.split('\n\n')
    
    # Parse the map lines
    lines = blocks[0].split('\n')
    map_dict = {}
    
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            # Map each character to its position using complex numbers
            map_dict[x + y * DOWN] = lines[y][x]
    
    # Parse the steps from the second block
    steps = [UP if ch == '^' else LEFT if ch == '<' else RIGHT if ch == '>' else DOWN for ch in blocks[1].replace('\n', '')]
    return map_dict, steps

def try_to_step(map_dict, robot_pos, direction):
    # Save the original state of the map
    original_map = map_dict.copy()
    
    # Handle different types of characters on the map
    if map_dict[robot_pos] == '.':
        return True  # Empty space, can move
    elif map_dict[robot_pos] in ('O', '@'):
        # Move a box or robot
        if try_to_step(map_dict, robot_pos + direction, direction):
            map_dict[robot_pos + direction] = map_dict[robot_pos]
            map_dict[robot_pos] = '.'
            return True
    elif map_dict[robot_pos] == ']':
        # Handle right wall of a box
        return try_to_step(map_dict, robot_pos + LEFT, direction)
    elif map_dict[robot_pos] == '[':
        # Handle left wall of a box
        if direction == LEFT:
            if try_to_step(map_dict, robot_pos + LEFT, direction):
                map_dict[robot_pos + LEFT] = '['
                map_dict[robot_pos] = ']'
                map_dict[robot_pos + RIGHT] = '.'
                return True
        elif direction == RIGHT:
            if try_to_step(map_dict, robot_pos + 2 * RIGHT, direction):
                map_dict[robot_pos] = '.'
                map_dict[robot_pos + RIGHT] = '['
                map_dict[robot_pos + 2 * RIGHT] = ']'
                return True
        else:
            if (try_to_step(map_dict, robot_pos + direction, direction) and 
                try_to_step(map_dict, robot_pos + RIGHT + direction, direction)):
                map_dict[robot_pos] = '.'
                map_dict[robot_pos + RIGHT] = '.'
                map_dict[robot_pos + direction] = '['
                map_dict[robot_pos + direction + RIGHT] = ']'
                return True
    
    # If move is not possible, revert to original state
    map_dict.clear()
    map_dict.update(original_map)
    return False

def solve(input_str):
    # Parse the input and get the initial state of the map and steps
    map_dict, steps = parse_input(input_str)
    
    # Find the starting position of the robot
    robot = next(pos for pos, char in map_dict.items() if char == '@')
    
    # Process each step
    for direction in steps:
        if try_to_step(map_dict, robot, direction):
            robot += direction
    
    # Calculate the result based on the final positions of boxes and robots
    result = sum(box.real + 100 * box.imag for box in map_dict if map_dict[box] in ('[', 'O'))
    return int(result)

def scale_up(input_str):
    # Scale up the input by replacing characters with larger representations
    return input_str.replace('#', '##').replace('.', '..').replace('O', '[]').replace('@', '@.')

if __name__ == "__main__":
    inp = sys.stdin.read()
    print(solve(inp))  # Solve the original input
    print(solve(scale_up(inp)))  # Solve the scaled-up input