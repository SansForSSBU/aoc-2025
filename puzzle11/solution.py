with open("puzzle11/input.txt") as f:
    input_text = f.read()
lines = [l for l in input_text.split("\n") if len(l) > 0]

connections = {}
for line in lines:
    in_node, out_nodes = line.split(": ")
    out_nodes = out_nodes.split(" ")
    connections[in_node] = out_nodes


def find_n_routes(graph, start, end):
    # 599
    # TODO: Optimize
    unexplored_routes = [start]
    num_routes = {start: 1}
    routes = set()
    idx = 0
    while len(unexplored_routes) > 0:
        node = unexplored_routes.pop(0)
        if node == "out":
            continue
        outputs = graph[node]
        for output in outputs:
            num_routes[output] = num_routes.get(output,0) + num_routes[node]
            unexplored_routes.append(output)
        if node == end:
            continue
        num_routes[node] = 0
    return num_routes[end]

def solve_pt1(graph):
    return find_n_routes(graph, "you", "out")
    

def solve_pt2(graph):
    n1 = find_n_routes(graph, "svr", "fft")
    n2 = find_n_routes(graph, "fft", "dac")
    n3 = find_n_routes(graph, "dac", "out")

    n4 = find_n_routes(graph, "svr", "dac")
    n5 = find_n_routes(graph, "dac", "fft")
    n6 = find_n_routes(graph, "fft", "out")

    return n1*n2*n3 + n4*n5*n6

print("Part 1 ans:", solve_pt1(connections))
print("Part 2 ans:", solve_pt2(connections))