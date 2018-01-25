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


def check_for_subgraphs(graph, graph_in):
    nodes = []  # besuchte knoten
    edges = []  # noch nicht benutzte und ausgewählte kanten
    size_subgraphs = []

    unused_nodes = [x for x in graph.keys()]


    count = 0
    while len(nodes) < len(graph.keys()):

        next_node = unused_nodes.pop()
        n = [next_node]
        nodes.append(next_node)

        for edge in graph[n[0]]:    # Füge alle ausgehenden kanten hinzu
            edges.append(edge[0])
        for edge in graph_in[n[0]]:  # Füge alle eingehende kanten hinzu
            edges.append(edge[0])


        while len(edges) > 0:
            e = edges.pop(0)
            if e not in nodes:
                nodes.append(e)
                n.append(e)
                unused_nodes.remove(e)

                for edge in graph[e]:       # Füge alle ausgehende Kanten hinzu
                    edges.append(edge[0])
                for edge in graph_in[e]:       # Füge alle eingehende Kanten hinzu
                    edges.append(edge[0])

        size_subgraphs.append(len(n))

    size_subgraphs.sort(reverse=True)

    return sum(size_subgraphs), len(size_subgraphs)== 1, size_subgraphs


files = ["cora/cora_cite/cora_cite", "imb/imdb_all/imdb_all",
         "webkb/webkb_texas_cocite/WebKB-texas-cocite"]

for f in files:
    print("-------------------- ", f, " --------------------")
    graph = {}
    graph_in = {}

    read_graph(f, graph, graph_in)

    print("size of graph", len(graph.keys()))
    print("Avarage degree", avarage_in_degree(graph))
    print("density", density(graph))
    degree = 0
    print("nodes with degree", degree, ", ausgangsgrad, eingangsgrad", nodes_with_k_degrees(graph, graph_in, degree))
    print("Full connected graph, size of the subgraphs",check_for_subgraphs(graph, graph_in))

    print("\n\n")
