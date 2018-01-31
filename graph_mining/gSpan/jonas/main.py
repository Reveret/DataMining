import time
from gspan_helper import run_gspan, graph_contains_pattern
from random_forest import run_random_forest
from random import shuffle
from os.path import join as os_join
import subprocess
import numpy as np

DATA_PATH = "data"


def split_data(graph_file, label_file):
    """ Shuffle input and split data in train data (2/3) and test data(1/3)"""
    # Read in labels
    with open(os_join(DATA_PATH, label_file)) as f:
        labels_origin = [line.split()[-1] for line in f]

    graphs = []
    labels = []
    index = -1
    # Read in graphs as string
    with open(os_join(DATA_PATH, graph_file)) as f:
        for line in f:
            if line[0] == "t":
                index += 1
                labels.append(labels_origin[index])
                graphs.append("")
            graphs[index] += line

    # Shuffle indices of graphs
    indices = list(range(len(graphs)))
    shuffle(indices)
    s_point = int(len(indices) / 3 * 2)

    # Writen graphs and labels in separate files for train and test data
    with open(os_join(DATA_PATH, "train_{}".format(graph_file)), "w") as graph_out:
        with open(os_join(DATA_PATH, "train[]".format(label_file), "w")) as label_out:
            for index in indices[:s_point]:
                graph_out.writelines(graphs[index])
                label_out.write(labels[index] + "\n")
    with open(os_join(DATA_PATH, "test_{}".format(graph_file)), "w") as graph_out:
        with open(os_join(DATA_PATH, "test_{}".format(label_file), "w")) as label_out:
            for index in indices[s_point:]:
                graph_out.writelines(graphs[index])
                label_out.write(labels[index] + "\n")


def graph_mining(train_file, test_file, min_sup):
    """
        Run gSpan algorithm for frequent sup-graphs
        Create train and test matrix with graph x freq pattern
        and 1 if pattern in graph else 0
    """
    print("Min Support: " + str(min_sup))
    train, test, freq_pattern = run_gspan(train_file, test_file, min_sup)

    # Create empty matrices
    train_mat = [[0 for _ in range(len(freq_pattern))] for _ in range(len(train))]
    test_mat = [[0 for _ in range(len(freq_pattern))] for _ in range(len(test))]

    # Fill train matrix
    for i, graph in enumerate(train):
        for j, pattern in enumerate(freq_pattern):
            if graph_contains_pattern(graph, pattern[1]):
                train_mat[i][j] = 1

    # Fill test matrix
    for i, graph in enumerate(test):
        for j, pattern in enumerate(freq_pattern):
            if graph_contains_pattern(graph, pattern[1]):
                test_mat[i][j] = 1

    return train_mat, test_mat, len(freq_pattern)


def load_labels(filename, sep=","):
    """ Load labels for graphs """
    with open(os_join(DATA_PATH, filename)) as f:
        return [line.strip().split(sep)[-1] for line in f]


def first_set(min_sup):
    """ Database bbp2 """
    print("-- Database: bbp2 --")
    train_labels = load_labels("train_bbp2.gt")
    test_labels = load_labels("test_bbp2.gt")

    # Run graph mining to get matrices
    train_matrix, test_matrix, num_freq = graph_mining(os_join(DATA_PATH, "train_bbp2.gsp"),
                                                       os_join(DATA_PATH, "test_bbp2.gsp"), len(train_labels) * min_sup)

    # Train RandomForrestClassifier with matrices and labels
    try:
        score = run_random_forest(train_matrix, train_labels, test_matrix, test_labels)
    except Exception as e:
        print(str(e))
        return str(e)

    print("Accuracy of classifier: " + str(score))
    return score, num_freq


def second_set(min_sup):
    """ Database molecules """
    print("-- Database: molecules --")
    train_labels = load_labels("train_molecules.groundTruth", sep=" ")
    test_labels = load_labels("test_molecules.groundTruth", sep=" ")

    # Run graph mining to get matrices
    train_matrix, test_matrix, num_freq = graph_mining(os_join(DATA_PATH, "train_molecules.gsp"),
                                                       os_join(DATA_PATH, "test_molecules.gsp"),
                                                       len(train_labels) * min_sup)

    # Train RandomForrestClassifier with matrices and labels
    try:
        score = run_random_forest(train_matrix, train_labels, test_matrix, test_labels)
    except Exception as e:
        print(str(e))
        return str(e)

    print("Accuracy of classifier: " + str(score))
    return score, num_freq


def long_time_analyse():
    """ Run through all thresholds 10 times for every data set to get best result """
    t = time.time()
    t1 = t
    path = "analyse"
    for i in range(10):
        output = open(path + r"\analyse{}.txt".format(i), "w")
        output.close()
        for m in np.arange(0.3, 0.9, 0.1):
            sup = round(m, 3)
            with open(path + r"\analyse{}.txt".format(i), "a") as output:
                print("---> SUPPORT: " + str(sup))
                output.write("-> Support: {}".format(sup) + "\n")
                output.write("bbp2: {} -- {}".format(*first_set(sup)) + "\n")
                print("-" * 20)
                output.write("molecules: {} -- {}".format(*second_set(sup)) + "\n")

        with open(path + r"\analyse{}.txt".format(i), "a") as output:
            print("Time: {}s".format(time.time() - t1))
            output.write(str(time.time() - t1))
        t1 = time.time()

    print(time.time() - t)

    try:
        subprocess.call("shutdown -h", shell=True)
    except Exception as e:
        print(str(e))


def main():
    # Run on bpp2 set
    first_set(0.4)

    # Run on molecules set
    second_set(0.5)
