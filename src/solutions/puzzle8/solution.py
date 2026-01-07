from copy import deepcopy
import functools
import math

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
    possible_connections = get_connection_costs(boxes)
    best_connections = sorted(possible_connections, key=lambda x: x[1])
    circuits = [{i} for i, _ in enumerate(boxes)]
    for (connection, cost) in best_connections[:1000]:
        update_circuits(connection, circuits)

    circuit_lengths = [len(circuit) for circuit in circuits]
    three_largest_lengths = sorted(circuit_lengths, reverse=True)[:3]
    return math.prod(three_largest_lengths)

def solve_pt2(boxes):
    possible_connections = sorted(get_connection_costs(boxes), key=lambda x: x[1])
    best_connections = sorted(possible_connections, key=lambda x: x[1])
    circuits = [{i} for i, _ in enumerate(boxes)]
    i = 0
    while True:
        (connection, cost) = best_connections[i]
        update_circuits(connection,circuits)
        i += 1
        if len(circuits) == 1:
            box1_x = boxes[connection[0]][0]
            box2_x = boxes[connection[1]][0]
            return box1_x*box2_x

def main(input_file):
    boxes = [tuple([int(n) for n in box.split(",")]) for box in input_file.split("\n") if len(box)>0]
    pt1_ans = solve_pt1(boxes)
    pt2_ans = solve_pt2(boxes)
    return (pt1_ans, pt2_ans)