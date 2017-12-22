from graph_mining.jonas.gspan_helper import run_gspan, graph_contains_pattern
from graph_mining.jonas.random_forest import run_random_forest
import random
import os

DATA_PATH = "data"


def split_data(graph_file, label_file):
    """ Shuffle input and split data in train data (2/3) and test data(1/3)"""
    with open(os.path.join(DATA_PATH, label_file)) as f:
        labels_origin = [line.split()[-1] for line in f]

    graphs = []
    labels = []
    index = -1
    with open(os.path.join(DATA_PATH, graph_file)) as f:
        for line in f:
            if line[0] == "t":
                index += 1
                labels.append(labels_origin[index])
                graphs.append("")
            graphs[index] += line

    indices = list(range(len(graphs)))
    random.shuffle(indices)
    s_point = int(len(indices) / 3 * 2)
    with open(os.path.join(DATA_PATH, "train_{}".format(graph_file)), "w") as graph_out:
        with open(r"data\train_{}".format(label_file), "w") as label_out:
            for index in indices[:s_point]:
                graph_out.writelines(graphs[index])
                label_out.write(labels[index] + "\n")
    with open(os.path.join(DATA_PATH, "test_{}".format(graph_file)), "w") as graph_out:
        with open(r"data\test_{}".format(label_file), "w") as label_out:
            for index in indices[s_point:]:
                graph_out.writelines(graphs[index])
                label_out.write(labels[index] + "\n")


def graph_mining(train_file, test_file, min_sup):
    """
        Run gSpan algorithm for frequent sup-graphs
        Create train and test matrix with graph x freq pattern
        and 1 if pattern in graph else 0
    """
    train, test, freq_pattern = run_gspan(train_file, test_file, min_sup)

    train_mat = [[0 for _ in range(len(freq_pattern))] for _ in range(len(train))]
    test_mat = [[0 for _ in range(len(freq_pattern))] for _ in range(len(test))]

    for i, graph in enumerate(train):
        for j, pattern in enumerate(freq_pattern):
            if graph_contains_pattern(graph, pattern[1]):
                train_mat[i][j] = 1

    for i, graph in enumerate(test):
        for j, pattern in enumerate(freq_pattern):
            if graph_contains_pattern(graph, pattern[1]):
                test_mat[i][j] = 1

    return train_mat, test_mat


def load_labels(filename, sep=","):
    """ Load labels for graphs """
    with open(os.path.join(DATA_PATH, filename)) as f:
        return [line.strip().split(sep)[-1] for line in f]


# split_data("bbp2.gsp", "bbp2.gt")

"""
train_labels = load_labels("train_bbp2.gt")
test_labels = load_labels("test_bbp2.gt")

train_matrix, test_matrix = graph_mining(os.path.join(path, "train_bbp2.gsp"),
                                         os.path.join(path, "test_bbp2.gsp"), 100)

score = run_random_forest(train_matrix, train_labels, test_matrix, test_labels)

print("bbp2: " + str(score))
"""

train_labels = load_labels("train_molecules.groundTruth", sep=" ")
test_labels = load_labels("test_molecules.groundTruth", sep=" ")

train_matrix, test_matrix = graph_mining(os.path.join(DATA_PATH, "train_molecules.gsp"),
                                         os.path.join(DATA_PATH, "test_molecules.gsp"), 150)

score = run_random_forest(train_matrix, train_labels, test_matrix, test_labels)

print("molecules: " + str(score))
