with open("puzzle9/input.txt", "r") as f:
    input_text = f.read()

def get_rectangle_area(coord1, coord2):
    return (abs(coord1[0] - coord2[0]) + 1) * (abs(coord1[1] - coord2[1]) + 1)

def solve_pt1(coordinate_list):
    best_area = 0
    for i in range(len(coordinate_list)):
        for j in range(i+1, len(coordinate_list)):
            area = get_rectangle_area(coordinate_list[i], coordinate_list[j])
            if area > best_area:
                best_area = area
    return best_area

def get_direction(coord1, coord2):
    if coord1[0] == coord2[0]:
        if coord1[1] < coord2[1]:
            return "North"
        elif coord1[1] > coord2[1]:
            return "South"
    elif coord1[1] == coord2[1]:
        if coord1[0] < coord2[0]:
            return "East"
        elif coord1[0] > coord2[0]:
            return "West"
    raise ValueError

def get_rotation(direction1, direction2):
    # +1 for Right, -1 for Left
    if direction1 == "North":
        if direction2 == "East":
            return 90
        elif direction2 == "West":
            return -90
    elif direction1 == "South":
        if direction2 == "West":
            return 90
        if direction2 == "East":
            return -90
    elif direction1 == "East":
        if direction2 == "South":
            return 90
        elif direction2 == "North":
            return -90
    elif direction1 == "West":
        if direction2 == "North":
            return 90
        elif direction2 == "South":
            return -90
    raise ValueError

def get_turning_number(coordinate_list):
    directions = []
    for coord1_idx in range(len(coordinate_list)):
        coord2_idx = coord1_idx + 1
        if coord2_idx >= len(coordinate_list):
            coord2_idx = 0
        directions.append(get_direction(coordinate_list[coord1_idx], coordinate_list[coord2_idx]))
    turning_number = 0
    for coord1_idx in range(len(directions)):
        coord2_idx = coord1_idx + 1
        if coord2_idx >= len(directions):
            coord2_idx = 0
        turning_number += get_rotation(directions[coord1_idx], directions[coord2_idx])
    return turning_number

def get_enclosed_dir(coordinate_list):
    turning_number = get_turning_number(coordinate_list)
    if turning_number == -360:
        return "Left"
    elif turning_number == +360:
        return "Right"
    raise ValueError

def solve_pt2(coordinate_list):
    enclosed_dir = get_enclosed_dir(coordinate_list)
    pass

coordinate_list = [tuple([int(x) for x in l.split(",")]) for l in input_text.split("\n") if len(l) > 0]
print("Part 1 ans:", solve_pt1(coordinate_list))
print("Part 2 ans:", solve_pt2(coordinate_list))
pass