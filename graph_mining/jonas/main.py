from graph_mining.gspan_helper import run_gspan
from graph_mining.random_forest import run_random_forest
import random
import os


def split_data(graph_file, label_file):
    """ Shuffle input and split data in train data (2/3) and test data(1/3)"""
    path = "data"
    with open(os.path.join(path, label_file)) as f:
        labels_origin = [line.split()[-1] for line in f]

    graphs = []
    labels = []
    index = -1
    with open(os.path.join(path, graph_file)) as f:
        for line in f:
            if line[0] == "t":
                index += 1
                labels.append(labels_origin[index])
                graphs.append("")
            graphs[index] += line

    indices = list(range(len(graphs)))
    random.shuffle(indices)
    s_point = int(len(indices) / 3 * 2)
    with open(os.path.join(path, "train_{}".format(graph_file)), "w") as graph_out:
        with open(r"data\train_{}".format(label_file), "w") as label_out:
            for index in indices[:s_point]:
                graph_out.writelines(graphs[index])
                label_out.write(labels[index])
    with open(os.path.join(path, "test_{}".format(graph_file)), "w") as graph_out:
        with open(r"data\test_{}".format(label_file), "w") as label_out:
            for index in indices[s_point:]:
                graph_out.writelines(graphs[index])
                label_out.write(labels[index])


train_db, test_db, patterns = run_gspan(r"data\train_bbp2.gsp", r"data\test_bbp2.gsp", 100)

matrix =