from enum import Enum
import math
import statistics
with open("puzzle9/input.txt", "r") as f:
    input_text = f.read()


class Side(Enum):
    LEFT=0
    RIGHT=1
class Orientation(Enum):
    VERTICAL=0
    HORIZONTAL=1

class Direction(Enum):
    NORTH=0
    EAST=1
    SOUTH=2
    WEST=3

    def turn_90_degrees(self, side):
        if side == Side.RIGHT:
            return self.__class__((self.value + 1) % 4)
        elif side == Side.LEFT:
            return self.__class__((self.value - 1) % 4)
        else:
            raise ValueError

class Edge():
    def __init__(self, coordinate1, coordinate2):
        x = sorted([coordinate1[0], coordinate2[0]])
        self.x = range(x[0], x[1]+1)
        y = sorted([coordinate1[1], coordinate2[1]])
        self.y = range(y[0], y[1]+1)
        if len(self.x) == 1:
            self.x = self.x[0]
            self.orientation = Orientation.VERTICAL
        elif len(self.y) == 1:
            self.y = self.y[0]
            self.orientation = Orientation.HORIZONTAL
        else:
            raise ValueError()
    
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
        return get_edges(self.vertices())
    
    def contains_point(self, point):
        x = [self.v1[0], self.v2[0]]
        x = range(min(x), max(x)+1)
        y = [self.v1[1], self.v2[1]]
        y = range(min(y), max(y)+1)
        return point[0] in x and point[1] in y
    
    def midpoint(self):
        return (int(statistics.mean([self.v1[0], self.v2[0]])), int(statistics.mean([self.v1[1], self.v2[1]])))

class Loop():
    def __init__(self, vertices):
        self.vertices = vertices
        self.enclosed_dir = self.get_loop_side(vertices)
        self.edges = []
        for idx2 in range(len(vertices)):
            idx1 = idx2 - 1
            v1 = vertices[idx1]
            v2 = vertices[idx2]
            direction = self.get_direction(v1,v2)
            inside_dir = direction.turn_90_degrees(self.enclosed_dir)
            edge = Edge(v1, v2)
            self.edges.append((edge, inside_dir))

    def get_turning_number(self, coordinate_list):
        directions = []
        for coord1_idx in range(len(coordinate_list)):
            coord2_idx = coord1_idx + 1
            if coord2_idx >= len(coordinate_list):
                coord2_idx = 0
            directions.append(self.get_direction(coordinate_list[coord1_idx], coordinate_list[coord2_idx]))
        turning_number = 0
        for coord1_idx in range(len(directions)):
            coord2_idx = coord1_idx + 1
            if coord2_idx >= len(directions):
                coord2_idx = 0
            turning_number += self.get_rotation(directions[coord1_idx], directions[coord2_idx])
        return turning_number
    
    def get_direction(self, coord1, coord2):
        if coord1[0] == coord2[0]:
            if coord1[1] < coord2[1]:
                return Direction.NORTH
            elif coord1[1] > coord2[1]:
                return Direction.SOUTH
            raise ValueError
        elif coord1[1] == coord2[1]:
            if coord1[0] < coord2[0]:
                return Direction.EAST
            elif coord1[0] > coord2[0]:
                return Direction.WEST
            raise ValueError

    def get_rotation(self, direction1, direction2):
        # +1 for Right, -1 for Left
        if direction1 == Direction.NORTH:
            if direction2 == Direction.EAST:
                return 90
            elif direction2 == Direction.WEST:
                return -90
        elif direction1 == Direction.SOUTH:
            if direction2 == Direction.WEST:
                return 90
            if direction2 == Direction.EAST:
                return -90
        elif direction1 == Direction.EAST:
            if direction2 == Direction.SOUTH:
                return 90
            elif direction2 == Direction.NORTH:
                return -90
        elif direction1 == Direction.WEST:
            if direction2 == Direction.NORTH:
                return 90
            elif direction2 == Direction.SOUTH:
                return -90
        raise ValueError
    
    def get_loop_side(self, coordinate_list):
        turning_number = self.get_turning_number(coordinate_list)
        if turning_number == -360:
            return Side.LEFT
        elif turning_number == +360:
            return Side.RIGHT
        raise ValueError

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

def get_edges(coordinate_list):
    edges = []
    for idx2 in range(len(coordinate_list)):
        idx1 = idx2 - 1
        v1 = coordinate_list[idx1]
        v2 = coordinate_list[idx2]
        edges.append(Edge(v1, v2))
    return edges

def do_edges_intersect(edge1, edge2):
    x = sorted([edge1.x, edge2.x], key=lambda a: isinstance(a, range))
    y = sorted([edge1.y, edge2.y], key=lambda a: isinstance(a, range))
    if isinstance(x[0], int) and isinstance(x[1], int):
        return False
    return x[0] in x[1] and y[0] in y[1]

def is_rectangle_legal(rectangle, corners, loop):
    # If rectangle 1-inside rectangle intersects any lines, false.
    v1, _, v2, _ = rectangle.vertices()
    v1 = (v1[0] + 1, v1[1] + 1)
    v2 = (v2[0] + 1, v2[1] + 1)
    shrunk_rect = Rectangle(v1,v2)
    shrunk_rect_edges = shrunk_rect.edges()
    for edge1 in shrunk_rect_edges:
        for edge2 in [e[0] for e in loop.edges]:
            if do_edges_intersect(edge1, edge2): # intersect
                return False
    # Raycast to verify midpoint is inside the loop
    midpoint = rectangle.midpoint()
    eligible_north_edges = [edge for edge in loop.edges if edge[1] in [Direction.SOUTH, Direction.NORTH]]
    eligible_north_edges = [edge for edge in eligible_north_edges if midpoint[0] in edge[0].x]
    eligible_north_edges = [edge for edge in eligible_north_edges if edge[0].y >= midpoint[1]]
    if len(eligible_north_edges) == 0: return False
    eligible_north_edges.sort(key=lambda x: x[0].y)
    if eligible_north_edges[0][1] == Direction.NORTH:
        return False
    return True





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
    # 242043982?
    # 2393897350 too high
    # 1470009489 incorrect
    progress = checkProgress()
    loop = Loop(coordinate_list)
    rectangles = get_best_rectangles(coordinate_list)
    for idx in range(progress, len(rectangles)):
        rectangle = rectangles[idx]
        if is_rectangle_legal(rectangle, coordinate_list, loop):
            return rectangle.area()
        if idx % 100 == 0:
            saveProgress(idx)

coordinate_list = [tuple([int(x) for x in l.split(",")]) for l in input_text.split("\n") if len(l) > 0]
print("Part 1 ans:", solve_pt1(coordinate_list))
print("Part 2 ans:", solve_pt2(coordinate_list))
pass