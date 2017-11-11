import time
import numpy as np
from matplotlib import pyplot as plt
import csv

def read(file, threshold):
    file = open(file, "r")
    data = []
    count = None
    for line in file:
        tmp = [int(x) for x in line.strip().split(",")]
        number = 0
        if not count:
            count = [0 for i in range(len(tmp))]

        for i in range(len(tmp)):
            if tmp[i] == 1:
                count[i] += 1
                number += 2 ** i

        data.append(number)
    file.close()
    first = []
    for i in range(len(count)):
        if count[i] / len(data) >= threshold:
            first.append(2 ** i)
    return first, data


def check_freq(x, threshold):
    global data
    count = 0
    min = len(data) * threshold
    for n in data:
        if n & x == x:
            count += 1
        if count >= min:
            return True
    return count >= min


# Calculate Freq-tupel with size k
def cacl_freq(prev_freq, ones, k, threshold):
    new = dict()
    for prev in prev_freq:
        for o in ones:
            new_or = prev | o
            if new_or != prev:
                if new_or not in new.keys():
                    new[new_or] = 1
                else:
                    new[new_or] += 1

    next_freq = []
    for n in new.keys():
        if new[n] == k:
            if check_freq(n, threshold):
                next_freq.append(n)
    return next_freq


def number_to_tupel(result):
    freq_tupel = []
    for x in result:
        freq_k = []
        for i in range(len(x)):
            tupel = set()
            a = x[i]
            j = 1
            while a != 0:
                if a % 2 == 1:
                    tupel |= {j}
                j += 1
                a = int(a / 2)
            sorted(tupel)
            freq_k.append(tupel)
        freq_tupel.append(freq_k)
    return freq_tupel


# calculate all freq-tupel with threshold and from file
def get_all_freq(threshold, file):
    global data
    first, data = read(file, threshold)
    result = [first]
    prev_freq = first
    k = 2

    while len(prev_freq) != 0:
        prev_freq = cacl_freq(prev_freq, first, k, threshold)
        result.append(prev_freq)
        # print("k=", k, "Länge", len(prev_freq))
        k += 1

    # return: transform number to tupel
    result_tupel = number_to_tupel(result)
    return result_tupel


def create_histogram(freq, file, threshold):
    itemset_sizes = []
    for i in range(len(freq)):
        for s in freq[i]:
            # print(s)
            itemset_sizes.append(len(s))

    plt.hist(itemset_sizes, align='left', bins=np.arange(0, len(freq) + 2, 1))
    plt.title("Frequent Itemsets")
    plt.xlabel("Size")
    plt.ylabel("Frequency")
    plt.xticks(np.arange(len(freq) + 0.5))

    plt.savefig("histogramm/" + file + "_threshold" + str(threshold) + ".png")
    plt.clf()


data = []

files = ["dm1.csv", "dm2.csv", "dm3.csv", "dm4.csv"]
thresholds = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
runtimes = [[""] + thresholds]
for f in files:
    times = [f]
    for th in thresholds:
        t = time.clock()
        freq = get_all_freq(th, f)
        seconds = time.clock() - t
        create_histogram(freq, f, th)
        times.append(seconds)
        print(f,"   ", th, "    ", seconds)
    runtimes.append(times)


with open("runtimes.csv", 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for times in runtimes:
        spamwriter.writerow([times])