with open("puzzle9/input.txt", "r") as f:
    input_text = f.read()


class Edge():
    def __init__(self, coordinate1, coordinate2):
        self.x = range(*sorted([coordinate1[0], coordinate2[0]+1]))
        self.y = range(*sorted([coordinate1[1], coordinate2[1]+1]))
    
    def __str__(self):
        return f"<Edge {self.x} {self.y}>"

    def __repr__(self):
        return self.__str__()

class Rectangle():
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    
    def area(self):
        return (abs(self.v1[0] - self.v2[0]) + 1) * (abs(self.v1[1] - self.v2[1]) + 1)
    

def get_best_rectangles(vertex_list):
    rectangles = []
    for i in range(len(vertex_list)):
        for j in range(i+1, len(vertex_list)):
            v1 = vertex_list[i]
            v2 = vertex_list[j]
            rectangles.append(Rectangle(v1, v2))
    rectangles.sort(key=lambda r: r.area(), reverse=True)
    return rectangles

def solve_pt1(coordinate_list):
    best_rectangle = get_best_rectangles(coordinate_list)[0]
    return best_rectangle.area()

def is_rectangle_legal(coord1, coord2):
    pass

def get_edges(coordinate_list):
    edges = []
    for idx1 in range(len(coordinate_list)):
        idx2 = idx1 + 1
        if idx2 >= len(coordinate_list):
            idx2 = 0
        edges.append(Edge(coordinate_list[idx1], coordinate_list[idx2]))
    return edges

def solve_pt2(coordinate_list):
    edges = get_edges(coordinate_list)
    pass

coordinate_list = [tuple([int(x) for x in l.split(",")]) for l in input_text.split("\n") if len(l) > 0]
print("Part 1 ans:", solve_pt1(coordinate_list))
print("Part 2 ans:", solve_pt2(coordinate_list))
pass