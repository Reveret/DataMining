import math
import random
import numpy as np
import sys
import time
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
import matplotlib.colors as plc
import sklearn.metrics as skm
from purity import purity_score

SHOW_STEPS = False


# Calculate distance between two points in n-dimensions
def distance(a, b):
    return math.sqrt(sum([(d_a - d_b) ** 2 for d_a, d_b in zip(a, b)]))


# Calculate new centers for the clusters
def calc_centers(centers, clusters, dimensions, data):
    for num, cluster in enumerate(clusters):
        # If cluster is empty set random center
        if len(cluster) == 0:
            centers[num] = [random.random() * (data.max() - data.min()) + data.min() for _ in range(dimensions)]
            continue

        # Calculate mean of all dimensions and create center
        for dim in range(dimensions):
            centers[num][dim] = np.array([data[p][dim] for p in cluster]).mean()


# K-Means calculation
def kmeans(k, data):
    # Get dimensions of data
    dimensions = len(data[0])

    # Create k random initialization centers
    centers = []
    for i in range(k):
        centers.append([random.random() * (data.max() - data.min()) + data.min() for _ in range(dimensions)])

    clusters = [[] for _ in range(k)]
    old_clusters = None

    # As long as the clusters change continue with creating new clusters
    while old_clusters != clusters:

        # Save old clusters
        old_clusters = clusters.copy()

        # Delete clusters to create new ones
        clusters = [[] for _ in range(k)]

        # Evaluate which point belongs to which cluster
        for index, point in enumerate(data):
            # Calculate distance between point and all center and find minimum
            dists = [distance(point, cen) for cen in centers]
            min_dist = min(dists)

            # Add index of point to cluster
            clusters[dists.index(min_dist)].append(index)

        # Calculate new centers for every cluster
        calc_centers(centers, clusters, dimensions, data)

        # Show steps
        if SHOW_STEPS:
            plot_cluster(data, clusters, centers)

    return centers, clusters


# Read in file
def read_dataset(path):
    file = open("datasets/" + path, "r")
    data = []
    labels = []

    for line in file:
        # Prepare line
        num_line = list(map(float, [num for num in line.strip().split() if num not in ("", "\t")]))

        # Split into data point and label
        point = []
        label = []
        for i, num in enumerate(num_line):
            point.append(num) if i < 2 else label.append(num)

        data.append(point)
        if len(label) > 0:
            labels.append(label[-1])

    print("Completed read in: {}".format(path))
    return np.array(data), labels if len(labels) > 0 else None


# Plotting for clusters
def plot_cluster(data, clusters, centers):
    for num, cluster in enumerate(clusters):
        # Colors
        hsv = (((300 / len(clusters)) * num + 60) / 360, 0.7, 1)
        # Plot clusters
        if len(cluster) != 0:
            d = np.array([data[i] for i in cluster])
            plt.plot(d[:, 0], d[:, 1], color=plc.hsv_to_rgb(hsv), marker='o', ls="")
        # Plot centers
        plt.plot(centers[num][0], centers[num][1], 'rD')

    plt.show()


# Create 1D list with a label for every data point with is corresponding to its cluster
def clusters_to_labels(clusters):
    labels = [None for _ in range(sum(len(l) for l in clusters))]
    for num, cluster in enumerate(clusters):
        for point in cluster:
            labels[point] = num
    return labels


# Create clusters from 1D label list - uses index of label for point in cluster
def labels_to_clusters(labels):
    clusters = [[] for _ in range(max(labels) + 1)]
    for i, lab in enumerate(labels):
        clusters[lab].append(i)

    return clusters


# Cluster a given dataset with k clusters
def clustering(path=None, k=None):
    # Read in command line arguments if there are some else use arguments
    path = path if path is not None else sys.argv[2]
    k = k if k is not None else int(sys.argv[1])

    # Read in data
    data, _ = read_dataset(path)

    # Calculate clusters
    centers, clusters = kmeans(k, data)

    # Plot clusters
    plot_cluster(data, clusters, centers)

    return centers, clusters


# Analyse a dataset with all methods given
def analyse(methods, path, borders, repeats=30, target_labels=None):
    # Read in data and labels
    # Use given labels if there are any else use from file
    if target_labels is not None:
        data, _ = read_dataset(path)
    else:
        data, target_labels = read_dataset(path)

    eval_scores = [[] for _ in methods]
    eval_labels = [[] for _ in methods]
    # For every 'k' in border
    for k in range(borders[0], borders[1]):
        print("k: " + str(k))

        # Best score and labels
        best_scores = [-math.inf for _ in methods]
        best_labels = [[] for _ in methods]

        # Calculate more often to avoid local peaks
        for rep in range(repeats):
            t = time.time()
            # Calculate clusters
            _, clusters = kmeans(k, data)
            # Get labels
            labels = clusters_to_labels(clusters)
            print("-{}: clustering complete after: {}".format(rep, time.time() - t))

            # Evaluate clustering with different methods
            for i, method in enumerate(methods):

                # Take best score and the labels for this
                n_score = method(target_labels, labels)
                if best_scores[i] < n_score:
                    best_scores[i] = n_score
                    best_labels[i] = labels

        for i in range(len(eval_scores)):
            eval_scores[i].append(best_scores[i])
            eval_labels[i].append(best_labels[i])

    for i, method in enumerate(methods):
        # Plot the scores
        color = [1 if i == j else 0 for j in range(3)]
        plt.plot(range(borders[0], borders[1]), eval_scores[i], marker="o", ls="--", color=color, label=method.__name__)
        plt.plot(eval_scores[i].index(max(eval_scores[i])) + 1, max(eval_scores[i]), marker="*", markersize=13,
                 color=color)

        # Save best labels in file
        with open("analyse/labels/{}_labels.txt".format("{} - {}".format(path, method.__name__)), "w") as f:
            d = eval_labels[eval_scores.index(max(eval_scores))]
            for l in d:
                f.write(str(l) + "\n")

    # Plot all scores in one diagram for best comparison and save to file
    plt.ylabel("score")
    plt.xlabel("k")
    plt.legend(bbox_to_anchor=(-0.15, 1.1), loc=2, ncol=3)
    plt.title("{} - all scores".format(path), y=1.08)
    plb.savefig("analyse/plots/{}.png".format("{} - all scores".format(path)))
    plt.show()


def analysing_datasets():
    files = []  # ["jain.txt", "Compound.txt"]
    methods = [skm.adjusted_rand_score, skm.adjusted_mutual_info_score, purity_score]

    for file in files:
        analyse(methods, file, (1, 10), 1)

    # analyse(methods, "s2.txt", (1, 10), target_labels=)
    with open("datasets/s2_target_labels.txt", "r") as f:
        labels = [int(line.strip()) for line in f]
    analyse(methods, "s2.txt", (1, 10), target_labels=labels)


def plot_from_label(label_file, data_file):
    labels = []
    with open(label_file, "r") as f:
        for line in f:
            labels.append(int(line))
    clust = labels_to_clusters(labels)
    cents = [[0, 0] for _ in range(max(labels) + 1)]
    data, _ = read_dataset(data_file)
    calc_centers(cents, clust, len(data[0]), data)
    plot_cluster(data, clust, cents)


if __name__ == "__main__":
    """_, clusts, _ = clustering("s2.txt", 15)
    labels = labels_for_clusters(clusts)
    with open("datasets/s2_target_labels.txt", "w") as f:
        for l in labels:
            f.write(str(l) + "\n")
    """
    # plot_from_label("analyse/labels/Compound.txt - purity_score_labels.txt", "Compound.txt")

    analysing_datasets()

    # clustering("Compound.txt", 8)
