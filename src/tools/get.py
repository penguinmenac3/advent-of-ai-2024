#!/usr/bin/env python3
import os
import requests
import argparse
from bs4 import BeautifulSoup


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))


def get_advent_of_code_input(year, day, session_cookie):
    base_url = f'https://adventofcode.com/{year}/day/{day}'
    
    task_description = None
    if not os.path.exists(os.path.join(BASE_DIR, f'{day:02d}', 'task.txt')):
        # Fetch the page content
        response = requests.get(base_url, cookies={'session': session_cookie})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all article elements
        articles = soup.find_all('article')
        task_description = '\n\n'.join(article.get_text() for article in articles)
    else:
        print(f"{os.path.join(BASE_DIR, f'{day:02d}', 'task.txt')} already exists, skipping download.")
    
    puzzle_input = None
    if not os.path.exists(os.path.join(BASE_DIR, f'{day:02d}', 'input.txt')):
        # Extract the puzzle input
        input_url = base_url + '/input'
        input_response = requests.get(input_url, cookies={'session': session_cookie})
        puzzle_input = input_response.text.strip()
    else:
        print(f"{os.path.join(BASE_DIR, f'{day:02d}', 'input.txt')} already exists, skipping download.")
    
    return task_description, puzzle_input


def write_files(day, task_description, puzzle_input):
    # Ensure the directories exist
    os.makedirs(os.path.join(BASE_DIR, f'{day:02d}'), exist_ok=True)
    
    # Write the task description and puzzle input to files
    if task_description is not None:
        with open(os.path.join(BASE_DIR, f'{day:02d}', 'task.txt'), 'w') as task_file:
            task_file.write(task_description)
        print(f"Task description written to {os.path.join(BASE_DIR, f'{day:02d}', 'task.txt')}")
    
    if puzzle_input is not None:
        with open(os.path.join(BASE_DIR, f'{day:02d}', 'input.txt'), 'w') as data_file:
            data_file.write(puzzle_input)
        print(f"Puzzle input written to {os.path.join(BASE_DIR, f'{day:02d}', 'input.txt')}")


def main(day):
    from config import session_cookie
    year = 2024
    task_description, puzzle_input = get_advent_of_code_input(year, day, session_cookie)
    write_files(day, task_description, puzzle_input)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Advent of Code input and task description.')
    parser.add_argument('day', type=int, help='The day of the Advent of Code puzzle (1-25).')
    
    args = parser.parse_args()
    main(args.day)
