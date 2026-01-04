with open("puzzle9/input.txt", "r") as f:
    input_text = f.read()


class Edge():
    def __init__(self, coordinate1, coordinate2, include_corners=True):
        self.x = range(*sorted([coordinate1[0], coordinate2[0]+1]))
        self.y = range(*sorted([coordinate1[1], coordinate2[1]+1]))
        if len(self.x) == 1:
            self.x = self.x[0]
            self.orientation = "vertical"
            if not include_corners:
                self.y = range(self.y[1], self.y[-1])
        if len(self.y) == 1:
            self.y = self.y[0]
            self.orientation = "horizontal"
            if not include_corners:
                self.x = range(self.x[1], self.x[-1])
        pass
    
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
    
    def vertices(self):
        va = (min(self.v1[0], self.v2[0]), min(self.v1[1], self.v2[1]))
        vb = (max(self.v1[0], self.v2[0]), min(self.v1[1], self.v2[1]))
        vc = (max(self.v1[0], self.v2[0]), max(self.v1[1], self.v2[1]))
        vd = (min(self.v1[0], self.v2[0]), max(self.v1[1], self.v2[1]))
        return (va,vb,vc,vd)
    
    def edges(self):
        return get_edges(self.vertices(), include_corners=False)

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

def get_edges(coordinate_list, include_corners=True):
    edges = []
    for idx1 in range(len(coordinate_list)):
        idx2 = idx1 + 1
        if idx2 >= len(coordinate_list):
            idx2 = 0
        edges.append(Edge(coordinate_list[idx1], coordinate_list[idx2], include_corners=include_corners))
    return edges

def do_edges_intersect(edge1, edge2):
    x = sorted([edge1.x, edge2.x], key=lambda a: isinstance(a, range))
    y = sorted([edge1.y, edge2.y], key=lambda a: isinstance(a, range))
    return x[0] in x[1] and y[0] in y[1]

def is_rectangle_legal(rectangle, edges):
    verticals = [edge for edge in edges if edge.orientation == "vertical"]
    horizontals = [edge for edge in edges if edge.orientation == "horizontal"]
    if rectangle.area() == 2393897350:
        # TODO: Figure out why this rectangle is not valid
        pass
    intersections = []
    for rectEdge in rectangle.edges():
        if rectEdge.orientation == "vertical":
            wallEdges = horizontals
        elif rectEdge.orientation == "horizontal":
            wallEdges = verticals
        for wallEdge in wallEdges:
            if do_edges_intersect(rectEdge, wallEdge):
                intersections.append(wallEdge)
    
    return len(intersections) == 0

def checkProgress():
    progress = 0
    try:
        with open("puzzle9/progress.txt", "r") as f:
            progress = int(f.read())
    except Exception:
        pass
    return progress

def saveProgress(idx):
    with open("puzzle9/progress.txt", "w") as f:
        f.write(str(idx))

def solve_pt2(coordinate_list):
    # 2393897350 too high
    progress = checkProgress()
    edges = get_edges(coordinate_list)
    rectangles = get_best_rectangles(coordinate_list)
    for idx in range(progress, len(rectangles)):
        rectangle = rectangles[idx]
        if is_rectangle_legal(rectangle, edges):
            return rectangle.area()
        if idx % 100 == 0:
            saveProgress(idx)

coordinate_list = [tuple([int(x) for x in l.split(",")]) for l in input_text.split("\n") if len(l) > 0]
print("Part 1 ans:", solve_pt1(coordinate_list))
print("Part 2 ans:", solve_pt2(coordinate_list))
pass