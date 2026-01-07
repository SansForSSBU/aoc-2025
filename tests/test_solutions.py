import pytest
from solutions.puzzle1.solution import main

def test_solution1():
    input_path = "tests/my_inputs/1.txt"
    with open(input_path, "r") as f:
        input_text = f.read()
    pt1_ans, pt2_ans = main(input_text)
    assert pt1_ans == 1052
    assert pt2_ans == 6295