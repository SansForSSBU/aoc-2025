import numpy as np

def get_input():
    with open("puzzle4/input.txt", "r") as f:
        input_text = f.read()

    grid = [list(l) for l in input_text.split("\n") if len(l) > 0]
    for line in grid:
        for idx, char in enumerate(line):
            if char == "@":
                line[idx] = 1
            elif char == ".":
                line[idx] = 0
            else:
                raise ValueError("Neither roll or air")
    grid = np.array(grid)
    return grid

def get_num_adjacent_rolls(grid, coords):
    num = 0
    adjacent_transforms = [(0,-1), (0,1), (-1,0), (1,0), (-1,-1), (-1,1), (1,-1), (1,1)]
    for transform in adjacent_transforms:
        x = coords[0] + transform[0]
        y = coords[1] + transform[1]
        num += get_coords(grid, (x,y))
    return num

def is_in_grid(grid, coords):
    (x, y) = coords
    return x in range(grid.shape[1]) and y in range(grid.shape[0])

def get_coords(grid, coords):
    (x, y) = coords
    if is_in_grid(grid,coords):
        return grid[y][x]
    else:
        return 0
    
def set_coords(grid, coords, value):
    (x, y) = coords
    if is_in_grid(grid,coords):
        grid[y][x] = value

def get_removable_rolls(grid):
    rolls = []
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            coords = (x,y)
            if get_coords(grid, coords) == 1:
                if get_num_adjacent_rolls(grid, coords) < 4:
                    rolls.append(coords)
    return rolls

def solve_pt1(grid):
    return len(get_removable_rolls(grid))

def solve_pt2(grid):
    ans = 0
    while True:
        removes = get_removable_rolls(grid)
        if len(removes) == 0:
            break
        ans += len(removes)
        for remove in removes:
            set_coords(grid, remove, 0)
    return ans


g = get_input()
print("Part 1 ans:", solve_pt1(g))
print("Part 2 ans:", solve_pt2(g))