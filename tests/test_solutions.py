import pytest
from solutions.puzzle1.solution import main

def test_solution1():
    pt1_ans, pt2_ans = main()
    assert pt1_ans == 1052
    assert pt2_ans == 6295