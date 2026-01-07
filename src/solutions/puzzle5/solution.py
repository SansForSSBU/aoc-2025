def is_fresh(ranges, ingredient_id):
    for r in ranges:
        if ingredient_id in r:
            return True
    return False

def solve_pt1(ranges, ingredients):
    ans = 0
    for ingredient in ingredients:
        if is_fresh(ranges, ingredient):
            ans += 1
    return ans

def merge_ranges(r1, r2):
    # Check if the two ranges overlap
    if not (r1[0] in r2 or r1[-1] in r2):
        return False
    return range(min(r1[0], r2[0]), max(r1[-1], r2[-1])+1)

def solve_pt2(ranges):
    n = 0
    while n < len(ranges):
        r1 = ranges.pop(0)
        dels = []
        for idx, r2 in enumerate(ranges):
            merged = merge_ranges(r1,r2)
            if merged:
                r1 = merged
                dels.append(idx)
        if len(dels) == 0:
            n += 1
        else:
            n = 0
        for deletion in sorted(dels, reverse=True):
            del ranges[deletion]
        ranges.append(r1)
    return sum([len(r) for r in ranges])

def main(input_file):
    (ranges, ingredients) = input_file.split("\n\n")
    ranges = [[int(x) for x in r.split("-")] for r in ranges.split("\n")]
    ranges = [range(r[0], r[1]+1) for r in ranges]
    ingredients = [int(x) for x in ingredients.split("\n") if len(x) > 0]

    pt1_ans = solve_pt1(ranges, ingredients)
    pt2_ans = solve_pt2(ranges)
    return (pt1_ans, pt2_ans)