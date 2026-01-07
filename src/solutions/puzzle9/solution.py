from enum import Enum
import math
from copy import deepcopy
import statistics
with open("inputs/9.txt", "r") as f:
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
    
    def length(self):
        return len([a for a in [self.x,self.y] if isinstance(a, range)][0])
    def __str__(self):
        return f"<Edge {self.x} {self.y}>"

    def __repr__(self):
        return self.__str__()

class Rectangle():
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.v1, _, self.v2, _ = self.vertices() # Hack to sort them
    
    def get_shrunk_rect(self, units=1):
        _v1, _, _v2, _ = self.vertices()
        v1 = (_v1[0] + units, _v1[1] + units)
        v2 = (_v2[0] - units, _v2[1] - units)
        _y_diff = _v2[1] - _v1[1]
        _x_diff = _v2[0] - _v1[0]
        y_diff = v2[1] - v1[1]
        x_diff = v2[0] - v1[0]
        return Rectangle(v1, v2)

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
        if direction1.turn_90_degrees(Side.RIGHT) == direction2:
            return 90
        elif direction1.turn_90_degrees(Side.LEFT) == direction2:
            return -90
        else:
            raise ValueError()
    
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

def is_rectangle_legal(rectangle, loop):
    # Method: Check if midpoint is inside the loop. If it isn't, return False.
    # If it is, check for any intersecting lines. 
    # If there are no intersecting lines, the rectangle must either be entirely inside the loop or entirely outside the loop.
    # Because the midpoint was inside the loop and the rectangle is either entirely inside or out, therefore the entire rectangle must be.
    
    # Raycast to verify midpoint is inside the loop
    midpoint = rectangle.midpoint()
    eligible_north_edges = [edge for edge in loop.edges if edge[1] in [Direction.SOUTH, Direction.NORTH]]
    eligible_north_edges = [edge for edge in eligible_north_edges if midpoint[0] in edge[0].x]
    eligible_north_edges = [edge for edge in eligible_north_edges if edge[0].y >= midpoint[1]]
    if len(eligible_north_edges) == 0: return False
    eligible_north_edges.sort(key=lambda x: x[0].y)
    if eligible_north_edges[0][1] == Direction.NORTH:
        return False
    # If rectangle 1-inside rectangle intersects any lines, false.
    shrunk_rect = rectangle.get_shrunk_rect()
    shrunk_rect_edges = shrunk_rect.edges()
    for edge1 in shrunk_rect_edges:
        intersects = []
        for edge2 in [e[0] for e in loop.edges]:
            if do_edges_intersect(edge1, edge2): # intersect
                pos = edge2.x if isinstance(edge2.x, int) else edge2.y
                intersects.append(pos)
        intersects.sort()
        for idx in range(len(intersects)-1):
            if abs(intersects[idx]-intersects[idx+1]) == 1:
                raise Exception("Assumption violated. Two parallel edges are next to each other.")
        if len(intersects) > 0:
            return False
    
    return True

def solve_pt2(coordinate_list):
    loop = Loop(coordinate_list)
    rectangles = get_best_rectangles(coordinate_list)
    for rectangle in rectangles:
        if is_rectangle_legal(rectangle, loop):
            return rectangle.area()

coordinate_list = [tuple([int(x) for x in l.split(",")]) for l in input_text.split("\n") if len(l) > 0]
print("Part 1 ans:", solve_pt1(coordinate_list))
print("Part 2 ans:", solve_pt2(coordinate_list))