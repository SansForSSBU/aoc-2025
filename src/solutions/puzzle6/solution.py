import math

def parse_input_pt1(input_text):
    lines = input_text.split("\n")
    lines = [[i for i in l.split(" ") if i != ""] for l in lines if len(l) > 0]

    operators = lines[-1]
    numbers = lines[:-1]
    numbers = [[int(n) for n in l] for l in numbers]
    problem_nums = []
    for idx, _ in enumerate(numbers[0]):
        problem_nums.append([n[idx] for n in numbers])
    return operators, problem_nums

def parse_input_pt2(input_text):
    lines = [l for l in input_text.split("\n") if len(l) > 0]
    numbers = lines[:-1]
    operators = [op for op in lines[-1].split(" ") if op != ""]
    cols = []
    for i in range(len(numbers[0])):
        cols.append("".join([number_line[i] for number_line in numbers]).strip())
    problem_nums = []
    problem = []
    for col in cols:
        if col == "":
            problem_nums.append(problem)
            problem = []
        else:
            problem.append(int(col))
    problem_nums.append(problem)
    numbers = problem_nums
    return operators, numbers

def solve_pt1(operators, numbers):
    ans = 0
    for operator, numberList in zip(operators,numbers):
        if operator == "*":
            ans += math.prod(numberList)
        elif operator == "+":
            ans += sum(numberList)
    return ans

def main(input_file):
    (operators, numbers) = parse_input_pt1(input_file)
    pt1_ans = solve_pt1(operators, numbers)
    (operators, numbers) = parse_input_pt2(input_file)
    pt2_ans = solve_pt1(operators, numbers)
    return (pt1_ans, pt2_ans)