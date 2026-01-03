from copy import deepcopy
import functools
import math

with open("puzzle8/input.txt", "r") as f:
    input_text = f.read()

def update_circuits(connection, circuits):
    circuitsConnected = []
    for idx, circuit in enumerate(circuits):
        if connection[0] in circuit or connection[1] in circuit:
            circuitsConnected.append(idx)
    if len(circuitsConnected) == 0:
        circuits.append(set(connection))
    elif len(circuitsConnected) == 1:
        circuits[circuitsConnected[0]].update(list(connection))
    elif len(circuitsConnected) == 2:
        circuits[circuitsConnected[0]].update(circuits[circuitsConnected[1]])
        del circuits[circuitsConnected[1]]
    else:
        raise ValueError("This should never happen")

def find_circuits(connections):
    circuits = []
    for connection in connections:
        update_circuits(connection, circuits)
    return circuits

def get_connection_costs(boxes):
    boxes = deepcopy(boxes)
    connections = []
    for i in range(len(boxes)):
        for j in range(i+1, len(boxes)):
            dist = math.dist(boxes[i], boxes[j])
            connections.append(((i,j), dist))
    return connections

def solve_pt1(boxes):
    connections = get_connection_costs(boxes)
    best_connections = [connection[0] for connection in sorted(connections, key=lambda x: x[1])[:1000]]
    circuits = find_circuits(best_connections)
    circuit_lengths = [len(circuit) for circuit in circuits]
    three_largest_lengths = sorted(circuit_lengths, reverse=True)[:3]
    return math.prod(three_largest_lengths)

def solve_pt2(boxes):
    connections = sorted(get_connection_costs(boxes), key=lambda x: x[1])
    pass


boxes = [tuple([int(n) for n in box.split(",")]) for box in input_text.split("\n") if len(box)>0]
print("Part 1 ans:", solve_pt1(boxes))
print("Part 2 ans:", solve_pt2(boxes))