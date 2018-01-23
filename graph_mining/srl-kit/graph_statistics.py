def read_graph(path, graph):
    f = open(path, 'r')
    l = f.readline().strip()

    while l != "":
        line = l.split(",")

        node1 = int(line[0])
        node2 = int(line[1])
        mass = int(line[2])
        if node1 not in graph.keys():
            graph[node1] = [(node2, mass)]
        else:
            graph[node1].append((node2, mass))

        l = f.readline().strip()


def count_edge(graph):
    count = 0
    for k in graph.keys():
        count += len(graph[k])
    return count


def avarage_degree(graph):
    return count_edge(graph) / len(graph.keys())


def density(graph):
    return 2 * count_edge(graph) / (len(graph.keys()) * (len(graph.keys()) - 1))


graph = {}
read_graph("cora/cora_cite/cora_cite.rn", graph)

print(avarage_degree(graph))
print(density(graph))
