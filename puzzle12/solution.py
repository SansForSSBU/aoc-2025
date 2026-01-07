import numpy as np
with open("puzzle12/input.txt") as f:
    input_text = f.read()

sections = input_text.split("\n\n")
present_text = sections[:-1]
problems_text = sections[-1]

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
pass

def solve_problem(problem):
    dims, nums = problem
    total_space = dims[0]*dims[1]
    total_occupied = sum([v*sum(sum(presents[i])) for i,v in enumerate(nums)])
    if total_occupied > total_space:
        return False
    
    if total_space >= 9 * sum(nums):
        return True
    
    raise Exception("Naive solution won't work.")

n = 0
for problem in problems:
    if solve_problem(problem):
        n += 1
print(n)