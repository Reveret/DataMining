import math
import random
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
import matplotlib.colors as plc
import sklearn.metrics as skm
from purity import purity_score


# Calculate distance between two points in n-dimensions
def distance(a, b):
    return math.sqrt(sum([(d_a - d_b) ** 2 for d_a, d_b in zip(a, b)]))


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

    return centers, clusters


# Lese File ein
def read_dataset(path):
    file = open("datasets/" + path, "r")
    data = []
    labels = []

    for line in file:
        num_line = list(map(float, [num for num in line.strip().split() if num not in ("", "\t")]))
        point = []
        label = [0.0]
        for i, num in enumerate(num_line):
            point.append(num) if i < 2 else label.append(num)

        data.append(point)
        labels.append(label[-1])

    print("Read in: {}".format(path))
    return np.array(data), labels


# Plotting for clusters
def plot_cluster(data, clusters, centers):
    for num, cluster in enumerate(clusters):
        # Colors
        hsv = (((300 / len(clusters)) * num + 60) / 360, 0.7, 1)
        # Plot clusters
        d = np.array([data[i] for i in cluster])
        plt.plot(d[:, 0], d[:, 1], color=plc.hsv_to_rgb(hsv), marker='o', ls="")
        # Plot centers
        plt.plot(centers[num][0], centers[num][1], 'rD')

    plt.show()


def labels_for_clusters(clusters):
    labels = [None for _ in range(sum(len(l) for l in clusters))]
    for num, cluster in enumerate(clusters):
        for point in cluster:
            labels[point] = num
    return labels


def labels_to_clusters(labels):
    clusters = [[] for _ in range(max(labels) + 1)]
    for i, lab in enumerate(labels):
        clusters[lab].append(i)

    return clusters


def clustering(path=None, k=None):
    # Read in command line arguments
    path = path if path is not None else sys.argv[2]
    k = k if k is not None else int(sys.argv[1])

    # Read in data
    data, _ = read_dataset(path)

    # Calculate clusters
    centers, clusters = kmeans(k, data)

    # Plot clusters
    plot_cluster(data, clusters, centers)

    return centers, clusters, data


def analyse(method, path, borders, repeats=30, target_labels=None):
    # Read in data and labels
    if target_labels is not None:
        data, _ = read_dataset(path)
    else:
        data, target_labels = read_dataset(path)
    scores = []
    all_labels = []
    # Calculate different k's
    for k in range(borders[0], borders[1]):

        # Calculate more often to avoid local peaks
        best_score = -math.inf
        best_labels = []
        for _ in range(repeats):
            # Calculate clusters
            _, clusters = kmeans(k, data)
            # Get labels
            labels = labels_for_clusters(clusters)
            n_score = method(target_labels, labels)
            if best_score < n_score:
                best_score = n_score
                best_labels = labels

        scores.append(best_score)
        all_labels.append(best_labels)

    # Plot the scores
    plt.plot(range(1, 10), scores, marker="o", ls="")
    plt.plot(scores.index(max(scores)) + 1, max(scores), marker="*", markersize=13, color=(1, 0, 0))
    plt.ylabel("score")
    plt.xlabel("k")
    plt.ylim(ymax=max(scores) * 1.2)
    title = "{} - {}".format(path, method.__name__)
    plt.title(title)
    plb.savefig("analyse/plots/{}.png".format(title))
    plt.close()

    # Save best label
    with open("analyse/labels/{}_labels.txt".format(title), "w") as f:
        d = all_labels[scores.index(max(scores))]
        for l in d:
            f.write(str(l) + "\n")

    return scores


def analysing_datasets():
    files = []  # ["jain.txt", "Compound.txt"]
    methods = [skm.adjusted_rand_score, skm.adjusted_mutual_info_score, purity_score]

    for file in files:
        for method in methods:
            print(method.__name__ + " with " + file)
            scores = analyse(method, file, (1, 10))

    for method in methods:
        print(method.__name__ + " with " + "s2.txt")
        labels = []
        with open("s2_target_labels.txt", "r") as f:
            for line in f:
                labels.append(line)
        score = analyse(method, "s2.txt", (1, 10), target_labels=labels)


if __name__ == "__main__":
    """_, clusts, _ = clustering("s2.txt", 15)
    labels = labels_for_clusters(clusts)
    with open("datasets/s2_target_labels.txt", "w") as f:
        for l in labels:
            f.write(str(l) + "\n")
    """
    labels = []
    with open("datasets/s2_target_labels.txt", "r") as f:
        for line in f:
            labels.append(int(line))
    clust = labels_to_clusters(labels)
    cents = [[0, 0] for _ in range(max(labels) + 1)]
    calc_centers(cents, clust, 2, read_dataset("s2.txt"))

    # analysing_datasets()
