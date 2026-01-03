with open("puzzle3/input.txt", "r") as f:
    input_text = f.read()
lines = [l for l in input_text.split("\n") if len(l)>0]

def get_max_joltage(line, bulbs):
    nums = [int(x) for x in list(line)]
    ret = ""
    for digit in range(bulbs, 0, -1):
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

print("Part 1 answer:", sum([get_max_joltage(l,2) for l in lines]))
print("Part 2 answer:", sum([get_max_joltage(l,12) for l in lines]))
