with open("puzzle11/input.txt") as f:
    input_text = f.read()
lines = [l for l in input_text.split("\n") if len(l) > 0]

connections = {}
for line in lines:
    in_node, out_nodes = line.split(": ")
    out_nodes = out_nodes.split(" ")
    connections[in_node] = out_nodes

def get_upstream_nodes(graph, node):
    return [k for k,v in graph.items() if node in v]

def find_n_routes(graph, start, end):
    kv = {end: 1}
    routes = [(end, 0)]
    while len(routes) > 0:
        routes.sort(key=lambda x: x[1])
        node, depth = routes.pop(0)
        upstream_nodes = get_upstream_nodes(graph, node)
        for up in upstream_nodes:
            if not up in kv.keys():
                routes.append((up, depth+1))
            kv[up] = kv.get(up,0) + kv[node]
    
    return kv.get(start, 0)


def solve_pt1(graph):
    return find_n_routes(graph, "you", "out")
    

def solve_pt2(graph):
    # 11350111374360 too low
    n1 = find_n_routes(graph, "svr", "fft")
    n2 = find_n_routes(graph, "fft", "dac")
    n3 = find_n_routes(graph, "dac", "out")

    n4 = find_n_routes(graph, "svr", "dac")
    n5 = find_n_routes(graph, "dac", "fft")
    n6 = find_n_routes(graph, "fft", "out")

    return n1*n2*n3 + n4*n5*n6

print("Part 1 ans:", solve_pt1(connections))
print("Part 2 ans:", solve_pt2(connections))