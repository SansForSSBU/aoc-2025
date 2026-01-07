import numpy as np
from math import prod

def solve_problem(problem, presents):
    dims, nums = problem
    total_space = dims[0]*dims[1]
    min_occupied = sum([v*sum(sum(presents[i])) for i,v in enumerate(nums)])
    if min_occupied > total_space:
        return False
    
    max_occupied = [prod(present.shape) for present in presents]
    if total_space >= sum([num * max_occupied[i] for i, num in enumerate(nums)]):
        return True
    
    raise Exception("Naive solution won't work.")

def main(input_file):
    sections = input_file.split("\n\n")
    present_text = sections[:-1]
    problems_text = sections[-1]
    n = 0
    presents = []
    for present in present_text:
        present_idx, present_shape = present.split(":\n")
        present_idx = int(present_idx)
        present_shape_lines = present_shape.split("\n")
        present_shape = np.array([[1 if chr == '#' else 0 for chr in line] for line in present_shape_lines])
        presents.append(present_shape)

    problems = []
    for problem in [p for p in problems_text.split("\n") if len(p) > 0]:
        spec, amounts = problem.split(": ")
        dims = [int(x) for x in spec.split("x")]
        amounts = [int(x) for x in amounts.split(" ")]
        problems.append((dims, amounts))

    for problem in problems:
        if solve_problem(problem, presents):
            n += 1

    return (n,)