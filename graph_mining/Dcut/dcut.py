import math
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import random
import numpy as np

import sklearn.metrics as met

G = None  # Original graph


class Tree:
    def __init__(self, root=None, connections=None):
        if root is not None:
            self.root = root
            self.elements = [root]
            self.connections = {}
        elif connections is not None:
            self.connections = connections
            self.elements = set()
            for k in self.connections:
                self.elements.add(k[0])
                self.elements.add(k[1])
            self.elements = list(self.elements)

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def add(self, q, p, dens):
        self.elements.append(q)
        li = [q, p]
        li.sort()
        self.connections[tuple(li)] = round(dens, 5)

    def __str__(self):
        return "-> Tree with {} nodes <-\n".format(len(self)) + "".join(
            ["{} => {}: {} \n".format(k[0], k[1], v) for k, v in self.connections.items()])

    def __eq__(self, other):
        return True if type(other) == Tree and self.connections == other.connections else False

    def __ne__(self, other):
        return not self.__eq__(other)

    def difference(self, other):
        d = []
        for k, v in self.connections.items():
            if k not in other.connections.keys():
                d.append((k, v))
            elif other.connections[k] != v:
                d.append((k, v))
        return d

    def cut_edge_of(self, q, p):
        backup = self.connections.copy()
        li = [q, p]
        li.sort()
        backup.pop(tuple(li))
        first = {}
        second = {}
        f_elements = self.walk_along_path(backup, q, [])
        s_elements = self.walk_along_path(backup, p, [])
        for k, v in backup.items():
            for e in f_elements:
                if e in k:
                    first[k] = v
            for e in s_elements:
                if e in k:
                    second[k] = v

        if len(first) == 0 and len(f_elements) == 1:
            fi = Tree(root=f_elements[0])
        else:
            fi = Tree(connections=first)
        if len(second) == 0 and len(s_elements) == 1:
            se = Tree(root=s_elements[0])
        else:
            se = Tree(connections=second)
        return fi, se

    @staticmethod
    def walk_along_path(conn, q, visited):
        found = [q]
        for i in [list(k).pop(list(k).index(q) - 1) for k in conn.keys() if q in k]:
            if i not in visited:
                found += Tree.walk_along_path(conn, i, visited + [q])
        return found


def get_neighbours(a):
    """ Neighbours in the graph """
    global G
    return set(list(G.neighbors(a)) + [a])  # Neighbors of a


def coeff(u, v):
    """ Jaccard Coefficient """
    n_u = get_neighbours(u)
    n_v = get_neighbours(v)
    return len(n_u.intersection(n_v)) / len(n_u.union(n_v))


def get_weight(u, v):
    """ Unweighted so return 1"""
    return 1


def dcut(tree):
    """ Find lowest density in density-connected tree and cut this edge """

    def density(a, b):
        """ Return weight of an edge """
        return [d["weight"] for u, v, d in weight_g.edges(data=True) if a in (u, v) and b in (u, v) and a != b][0]

    # Get density-connected tree as weighted graph
    weight_g = create_graph(tree)
    mini = math.inf
    best_n = tuple()
    # Go through all edges and calculate dcut value
    for n1, n2 in tree.connections.keys():
        c1, c2 = tree.cut_edge_of(n1, n2)
        cal = density(n1, n2) / min(len(c1), len(c2))
        # Save smallest
        if cal < mini:
            best_n = (n1, n2)
            mini = cal

    # Return two trees, cut at the calculated edge
    return tree.cut_edge_of(*best_n), mini, best_n


def cut_until(k, tree):
    """ Cut the graph until k-clusters are created """
    tree_collection = [tree]
    cutted = []
    while len(tree_collection) < k:
        mini = math.inf
        min_trees = []
        for t in tree_collection:
            ts, cal, cut_nodes = dcut(t)
            if cal < mini:
                mini = cal
                min_trees = [t, (ts[0], ts[1])]
                true_cut = cut_nodes
        print("Cut at: {} -- {} --> {}".format(true_cut[0], true_cut[1], mini))
        cutted.append(true_cut)
        tree_collection.remove(min_trees[0])
        tree_collection += min_trees[1]

    return tree_collection, [t.elements for t in tree_collection], cutted


def dct():
    """ Create density-connected tree """

    def s(a, b):
        """ Similarity """
        return coeff(a, b) * get_weight(a, b)

    global G
    # Start with random node
    T = Tree(root=random.choice(list(G.nodes())))
    checked = [T.root]
    # Run until all nodes are in the DCT
    while len(T) < len(G.nodes()):
        maxv, p, q = -1, None, None
        for u in T:
            if len(T) == 2220:
                print("Hi")
            for v in get_neighbours(u):
                if v not in checked and s(u, v) > maxv:
                    maxv = s(u, v)
                    p = v
                    q = u
        checked.append(p)
        # Add node p with is connected to q to the tree bind with density maxv
        try:
            T.add(p, q, maxv)
        except Exception as e:
            print(e)
            print(len(checked))
            print(len(T))
            print(maxv)
            raise
    return T


def correct_graph_data(_path, multi=False):
    """ Sometimes the networkx reader has problems with the formatting of gml files so correct if error occure """
    tmp = "tmp.gml"
    # Open graph file and temporary file where the corrected graph is in
    with open(_path) as f:
        with open("tmp.gml", "w") as out:
            is_open = False
            in_graph = False
            for line in f:
                # Add multigraph tag if needed
                if line.startswith("graph") and multi:
                    in_graph = True
                # Remove newline after edge, graph and node and set the bracket directly afterwards
                if is_open and "[" in line:
                    out.write(" " + line.lstrip())
                    if in_graph:
                        out.write("  multigraph 1 \n")
                        in_graph = False
                elif len(list(filter(None, [i in line for i in ("node", "graph", "edge")]))) > 0:
                    out.write(line.rstrip("\n"))
                    is_open = True
                else:
                    out.write(line)
                    is_open = False

    return tmp


def create_graph(tree):
    """ Create a directed networkx graph with weights out of the DCT
        Use density between nodes as weights """
    # Create graph
    new = nx.DiGraph()
    for c in tree.elements:
        new.add_node(c)
    for c, w in tree.connections.items():
        new.add_edge(c[0], c[1], weight=w)
    return new


def equality_test():
    """ Test 20 times if two generated trees are equal"""
    for i in range(20):
        tree_1 = dct()
        tree_2 = dct()
        if tree_1 != tree_2:
            # print("Not in tree_2: ", tree_1.difference(tree_2))
            # print("Not in tree_1: ", tree_2.difference(tree_1))
            return False
    return True


def draw_tree(tree, show=True):
    """ Draw DCT """
    new = create_graph(tree)

    # Draw
    plt.axis("off")
    pos = nx.spring_layout(new, iterations=100)

    options = {
        'node_color': 'red',
        'node_size': 150,
    }  # Draw edges corresponding to weight
    edgewidth = [d['weight'] + 0.3 for (u, v, d) in new.edges(data=True)]
    nx.draw_networkx_nodes(new, pos, **options)
    nx.draw_networkx_edges(new, pos, width=edgewidth, arrows=True)
    nx.draw_networkx_labels(new, pos, font_size=10, font_weight="bold")

    if show:
        plt.show()


def draw_clusters_in_graph(tree_collection, clusters, cutted):
    plt.axis('off')
    pos = nx.spring_layout(G, iterations=100)
    num = 0
    for e, c in zip(tree_collection, clusters):
        # Colors
        rgb = colors.hsv_to_rgb((((360 / len(clusters)) * num + 60) / 360, 0.7, 1))
        nx.draw_networkx_nodes(G, pos, c, node_color=rgb, node_size=150)
        nx.draw_networkx_edges(G, pos, list(e.connections.keys()), edge_color=[rgb for _ in e.connections.keys()])
        nx.draw_networkx_labels(G, pos)
        num += 1

    nx.draw_networkx_edges(G, pos, cutted, edge_color='black')


def read_labels(path):
    is_data = False
    labels = []
    with open(path) as f:
        for line in f:
            if line.startswith("*vertices"):
                is_data = True
            elif is_data:
                labels.append(int(line.strip()))
    return labels


def generate_labels(cluster):
    print(sum([len(c) for c in cluster]))
    labels = [0 for _ in range(sum([len(c) for c in cluster]))]
    print(len(labels))
    return labels


def purity_score(true_labels, labels):
    """
    Calculate the purity score for the given cluster assignments and ground truth classes
    """

    A = np.c_[(labels, true_labels)]

    n_accurate = 0.

    for j in np.unique(A[:, 0]):
        z = A[A[:, 0] == j, 1]
        x = np.argmax(np.bincount(z))
        n_accurate += len(z[z == x])

    return n_accurate / A.shape[0]


def karate():
    """ karate data set """
    global G
    print("==> karate data set <==")
    path = r"data\karate.gml"
    try:
        G = nx.read_gml(path, "id")
    except nx.NetworkXError:
        print("Correction format of data")
        G = nx.read_gml(correct_graph_data(path), "id")

    # Test if DCT's are equal
    print("Equality test result: ", equality_test())
    """
    For my implementation the density-connected tree is not equal every time I generate it.
    Between 1 and 3 edges/links are different so the Theorem 1 does not apply her 
    """


def football():
    """ football data set """
    global G
    print("==> football data set <==")
    path = r"data\football.gml"
    try:
        G = nx.read_gml(path, "id")
    except nx.NetworkXError:
        print("Correction format of data")
        G = nx.read_gml(correct_graph_data(path, multi=True), "id")

    # Calculate trees
    t = dct()
    trees, cluster, cutted = cut_until(12, t)
    size = 4
    for i, t in enumerate(trees):
        plt.subplot(size, len(trees) // size, i + 1)
        draw_tree(t, False)
    plt.show()

    draw_clusters_in_graph(trees, cluster, cutted)
    plt.show()


def yeast():
    global G
    print("==> yeast data set <==")
    path = r"data\Yeast.paj"
    label_path = r"data\Yeast.clu"
    G = nx.read_pajek(path)

    _, cluster, _ = cut_until(12, dct())

    correct_labels = read_labels(label_path)
    my_labels = generate_labels(cluster)

    pur = purity_score(correct_labels, my_labels)
    mutal = met.adjusted_mutual_info_score(correct_labels, my_labels)
    rand = met.adjusted_rand_score(correct_labels, my_labels)

    print("Purity:", pur)
    print("Mutal info:", mutal)
    print("Rand:", rand)


def main():
    """ Do every task """

    # ------- karate data set --------
    # karate()

    # ------- Football data set -------
    # football()

    # ------- Yeast data set -------
    yeast()


if __name__ == "__main__":
    main()
