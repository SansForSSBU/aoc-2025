with open("puzzle11/input.txt") as f:
    input_text = f.read()
lines = [l for l in input_text.split("\n") if len(l) > 0]

connections = {}
for line in lines:
    in_node, out_nodes = line.split(": ")
    out_nodes = out_nodes.split(" ")
    connections[in_node] = out_nodes


def find_n_routes(graph, start, end):
    # TODO: Optimize
    unexplored_routes = [(start, start)]
    routes = set()
    while len(unexplored_routes) > 0:
        route, node = unexplored_routes.pop(0)
        if node == end:
            routes.add(route)
            continue
        outputs = graph[node]
        for output in outputs:
            unexplored_routes.append((f"{route},{node}", output))
    return len(routes)

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