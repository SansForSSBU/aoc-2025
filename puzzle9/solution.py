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
    
coordinate_list = [tuple([int(x) for x in l.split(",")]) for l in input_text.split("\n") if len(l) > 0]
print("Part 1 ans:", solve_pt1(coordinate_list))
pass