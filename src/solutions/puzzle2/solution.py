import math

def is_factor(factor, number):
    return number % factor == 0

def all_numbers_with_n_digits(n):
    return list(range(1, 10**n))

def make_invalids_with_n_digits(n, part1=False):
    invalids = []
    for totalLength in range(1,n+1):
        for repeatedLength in [number for number in list(range(1,totalLength)) if is_factor(number,totalLength)]:
            repeats = int(totalLength / repeatedLength)
            if part1 and repeats != 2:
                continue
            invalids.extend([int(str(x)*repeats) for x in all_numbers_with_n_digits(repeatedLength)])
    return list(set(invalids))

def solve_part(ranges, invalids):
    ans = 0
    for r in ranges:
        for invalid in invalids:
            if invalid in r:
                ans += invalid
    return ans

def main(input_file):
    ranges = [[int(num) for num in line.split("-")] for line in input_file.split(",")]
    ranges = [range(r[0], r[1]+1) for r in ranges]
    max_n_digits = math.ceil(math.log10(max([max(r) for r in ranges])))
    invalids_part1 = make_invalids_with_n_digits(max_n_digits, part1=True)
    invalids_part2 = make_invalids_with_n_digits(max_n_digits, part1=False)
    pt1_ans = solve_part(ranges, invalids_part1)
    pt2_ans = solve_part(ranges, invalids_part2)
    return (pt1_ans, pt2_ans)