def read_graph(path, graph, graph_in):
    f = open(path + ".csv", 'r')
    l = f.readline().strip()

    while l != "":
        line = l.split(",")

        node1 = line[0]
        name = line[1]

        graph[node1] = []
        graph_in[node1] = []
        l = f.readline().strip()

    f.close()

    f = open(path + ".rn", 'r')
    l = f.readline().strip()

    while l != "":
        line = l.split(",")

        node1 = line[0]
        node2 = line[1]
        mass = line[2]
        if node1 not in graph.keys():
            graph[node1] = [(node2, mass)]
        else:
            graph[node1].append((node2, mass))

        if node2 not in graph_in.keys():
            graph_in[node2] = [(node1, mass)]
        else:
            graph_in[node2].append((node1, mass))

        l = f.readline().strip()
    f.close()


def count_edge(graph):
    count = 0
    for k in graph.keys():
        count += len(graph[k])
    return count


def avarage_in_degree(graph):
    return count_edge(graph) / len(graph.keys())


def density(graph):
    return 2 * count_edge(graph) / (len(graph.keys()) * (len(graph.keys()) - 1))


def nodes_with_k_degrees(graph, graph_in, k):
    count_out = 0
    count_in = 0

    for node in graph.values():
        if len(node) == k:
            count_out += 1

    for node in graph_in.values():
        if len(node) == k:
            count_in += 1

    return count_out, count_in


def check_for_subgraphs(graph):
    nodes = []  # besuchte knoten
    edges = []  # noch nicht benutzte und ausgewählte kanten

    nodes.append(next(iter(graph)))

    for edge in graph[nodes[0]]:
        edges.append(edge[0])

    while len(edges) > 0:
        e = edges.pop(0)
        if e not in nodes:
            nodes.append(e)

            for edge in graph[e]:
                edges.append(edge[0])

    return len(nodes) == len(graph.keys()), len(nodes), len(graph.keys())


files = ["cora/cora_cite/cora_cite", "imb/imdb_all/imdb_all",
         "webkb/webkb_texas_cocite/WebKB-texas-cocite"]

for f in files:
    print("-------------------- ", f, " --------------------")
    graph = {}
    graph_in = {}

    read_graph(f, graph, graph_in)

    print("Avarage degree", avarage_in_degree(graph))
    print("density", density(graph))
    degree = 0
    print("nodes with degree", degree, ", ausgangsgrad, eingangsgrad", nodes_with_k_degrees(graph, graph_in, degree))
    print(check_for_subgraphs(graph))

    print("\n\n")
