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

def main(input_file):
    lines = [l for l in input_file.split("\n") if len(l)>0]
    pt1_ans = sum([get_max_joltage(l,2) for l in lines])
    pt2_ans = sum([get_max_joltage(l,12) for l in lines])
    return (pt1_ans, pt2_ans)
