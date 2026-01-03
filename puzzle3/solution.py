with open("puzzle3/input.txt", "r") as f:
    input_text = f.read()
lines = [l for l in input_text.split("\n") if len(l)>0]

def get_max_joltage_pt2(line):
    nums = [int(x) for x in list(line)]
    ret = ""
    for digit in range(12, 0, -1):
        excluded_digits = digit-1
        if excluded_digits > 0:
            choices = nums[:-excluded_digits]
        else:
            choices = nums
        largest = max(choices)
        idx = nums.index(largest)
        nums = nums[idx+1:]
        ret = ret + str(largest)
    return int(ret)

def get_max_joltage_pt1(line):
    nums = [int(x) for x in list(line)]
    first_num = max(nums[:-1])
    second_num = max(nums[nums.index(first_num)+1:])
    return first_num*10+second_num

def solve_pt1(lines):
    ans = sum([get_max_joltage_pt1(l) for l in lines])
    print("Part 1 answer:", ans)

def solve_pt2(lines):
    ans = sum([get_max_joltage_pt2(l) for l in lines])
    print("Part 2 answer:", ans)

solve_pt1(lines)
solve_pt2(lines)