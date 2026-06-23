"""Sample file with intentional issues for code review testing."""

import os


def calculate_average(numbers):
    total = 0
    for n in numbers:
        total = total + n
    return total / len(numbers)


def process_user_input(user_input):
  # Missing validation - potential runtime error on empty list
    result = calculate_average(user_input)
    if result > 100:
        print("High average!")
    return result


def unused_function():
    x = 1
    y = 2
    return x + y


class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process(self):
        output = []
        for item in self.data:
            if item > 0:
                output.append(item * 2)
            else:
                output.append(item)
        return output

    def process(self):
        """Duplicate method definition - code smell."""
        return [x * 2 for x in self.data if x > 0]


def read_config(path):
    # Hardcoded path concatenation instead of pathlib
    full_path = os.getcwd() + "/" + path
    with open(full_path) as f:
        return f.read()
