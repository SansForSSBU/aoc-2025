import math

with open("puzzle2/input.txt", "r") as f:
    lines = f.read()

ranges = [[int(num) for num in line.split("-")] for line in lines.split(",")]
ranges = [range(r[0], r[1]+1) for r in ranges]

def get_num_digits(n):
    return math.ceil(math.log10(n))

def funky(n):
    x = int(math.pow(10,int(n/2)-1))
    for a in range(x, x*10):
        yield int(str(a)*2)
    pass

def find_invalid_nums(r):
    d1 = get_num_digits(r[0])
    d2 = get_num_digits(r[-1])
    dr = [n for n in list(range(d1,d2+1)) if n % 2 == 0]
    possibles = []
    for d in dr:
        possibles.extend(funky(d))
    possibles = [n for n in possibles if n in r]
    return possibles

invalids = []
for r in ranges:
    invalids.extend(find_invalid_nums(r))
print(sum(invalids))