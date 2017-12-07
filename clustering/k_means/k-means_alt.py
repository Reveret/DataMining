import math
import random
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as pltc
import scipy.special as ss


def kmeans(k, data):
    dim = len(data[0])
    min = math.inf
    max = -math.inf

    for x in data:
        for y in x:
            if y > max:
                max = y
            if y < min:
                min = y

    center = []
    cluster = [[] for i in range(k)]
    old_cluster = None

    for i in range(k):  # Erzeuge k zufällige "Mittelpunkte"
        point = []
        for j in range(dim):  # Für alle Dimensionen erzeuge eine Zufallszahl zwischen min und max
            point.append(random.random() * (max - min) + min)
        center.append(point)  # Füge den random Punkt als Startpunkt eines Clsuters hinzu

    while old_cluster != cluster:  # Solange sich die Cluster noch verändern

        old_cluster = cluster.copy()

        cluster = [[] for i in range(k)]  # Leere alte Indizes von dem vorherigen Schritt

        for d in range(len(data)):  # Für jeden Punkt
            min_dist = math.inf
            cluster_number = -1
            for c in range(len(center)):  # Bestimme den nähesten ClustermengeMittelpunkt vom Punkt data[d]

                # Bestimme Entfernung
                sum = 0
                for i in range(dim):
                    sum += (center[c][i] - data[d][i]) ** 2
                sum = math.sqrt(sum)

                # Überprüfe ob ein näherer Mittelpunkt gefunden wurde
                if sum < min_dist:
                    min_dist = sum
                    cluster_number = c

            cluster[cluster_number].append(d)  # Füge Punkt zur nähesten Cluster hinzu

        for c in range(len(cluster)):  # Update den Mittelpunkt jedes Clusters
            for d in range(dim):

                # Addiere alle Punkte aufeinander und dividiere durch die Anzahl
                sum = 0
                for p in cluster[c]:
                    sum += (data[p])[d]

                if sum != 0:
                    sum /= len(cluster[c])
                else:  # Wenn Cluster keine Punkte hat, erzeuge einen neuen zufälligen Mittelpunkt
                    sum = random.random() * (max - min) + min

                center[c][d] = sum

    return center, cluster


# Lese File ein
def read_dataset(path):
    file = open(path, "r")
    data = []

    for line in file:
        numbers = line.strip().split(" ")
        point = []
        for n in numbers:
            if n != "":
                point.append(float(n))
            if len(point) == 2:  # Datensätze haben nur 2 dimensionen
                break
        data.append(point)

    print("Ready read input")
    return data


def rand_index(size, c1, c2):
    a = 0
    b = 0

    for i in range(size):
        for j in range(i, size):
            a_same = False
            b_same = False
            for x in c1:
                if i in x and j in x:
                    a_same = True
                    break
                if (i in x and j not in x) or (j in x and i not in x):
                    break
            for x in c2:
                if i in x and j in x:
                    b_same = True
                    break
                if (i in x and j not in x) or (j in x and i not in x):
                    break
            if a_same and b_same:
                a += 1
            if not (a_same or b_same):
                b += 1
            #ss.binom(size, 2)
    return a + b / ss.binom(size, 2)


arg = sys.argv

path = "s2.txt"  # arg[2]
k = 20  # int(arg[1])
data = read_dataset(path)
centers1, clusters1 = kmeans(1, data)

for i in range(2, k):
    centers2, clusters2 = kmeans(i, data)

    score =rand_index(len(data), centers1, centers2)
    print(score)


for c in range(len(clusters1)):
    # colors = ['bo', 'go', 'co', 'mo', 'yo', 'ko', 'wo']
    r = random.random()
    g = random.random()
    b = random.random()
    color = pltc.to_rgb((r, g, b))
    d = np.array([data[i] for i in clusters1[c]])
    plt.plot(d[:, 0], d[:, 1], color=color, marker='o', ls="")
    cen = np.array(centers1[c])
    plt.plot(cen[0], cen[1], 'ro')

plt.show()
