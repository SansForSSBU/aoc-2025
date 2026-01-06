with open("puzzle11/input.txt") as f:
    input_text = f.read()
lines = [l for l in input_text.split("\n") if len(l) > 0]

connections = {}
for line in lines:
    in_node, out_nodes = line.split(": ")
    out_nodes = out_nodes.split(" ")
    connections[in_node] = out_nodes


def solve_pt1(graph):
    # 354300185 too high
    unexplored_routes = [("you", "you")]
    out_routes = set()
    while len(unexplored_routes) > 0:
        route, node = unexplored_routes.pop(0)
        if node == "out":
            out_routes.add(route)
            continue
        outputs = graph[node]
        for output in outputs:
            unexplored_routes.append((f"{route}{node}", output))
    return len(out_routes)

print("Part 1 ans:", solve_pt1(connections))