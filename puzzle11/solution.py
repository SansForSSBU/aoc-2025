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
    kv = {(end, 0): 1}
    routes = [(end, 0)]
    while len(routes) > 0:
        routes.sort(key=lambda x: x[1])
        node, depth = routes.pop(0)
        upstream_nodes = get_upstream_nodes(graph, node)
        for up in upstream_nodes:
            entry = (up, depth+1)
            if not entry in routes:
                routes.append(entry)
            kv[entry] = kv.get(entry,0) + kv[(node,depth)]
    
    ans = 0
    for k,v in kv.items():
        if k[0] == start:
            ans += v
    return ans

memo = {}
def find_n_routes2(graph, start, end):

    pass

def solve_pt1(graph):
    return find_n_routes(graph, "you", "out")
    

def solve_pt2(graph):
    # 11350111374360 too low
    # 13620133649232 too low
    # 247031466393430 total (no restrictions)
    # 21677843348293140 wrong
    # 393474305030400
    #n0 = find_n_routes(graph, "svr", "out")

    n1 = find_n_routes(graph, "svr", "fft")
    n2 = find_n_routes(graph, "fft", "dac")
    n3 = find_n_routes(graph, "dac", "out")

    n4 = find_n_routes(graph, "svr", "dac")
    n5 = find_n_routes(graph, "dac", "fft")
    n6 = find_n_routes(graph, "fft", "out")

    return n1*n2*n3+n4*n5*n6

print("Part 1 ans:", solve_pt1(connections))
print("Part 2 ans:", solve_pt2(connections))