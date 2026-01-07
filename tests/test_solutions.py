import pytest
from solutions.puzzle1.solution import main as solution1

def test_solution1():
    input_path = "tests/my_inputs/1.txt"
    with open(input_path, "r") as f:
        input_text = f.read()
    answers = solution1(input_text)
    assert answers == (1052, 6295)