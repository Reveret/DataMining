import time
import numpy as np
from matplotlib import pyplot as plt
import csv


def read(file, threshold, frequency):
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
    neg = []
    for i in range(len(count)):
        if count[i] / len(data) >= threshold:
            first.append(2 ** i)
            frequency[2 ** i] = count[i]
        else:
            neg.append(2 ** i)

    return first, data, neg


def check_freq(x, threshold):
    global data
    count = 0
    min = len(data) * threshold
    for n in data:
        if n & x == x:
            count += 1
    return count, count >= min


# Calculate Freq-tupel with size k
def cacl_freq(prev_freq, ones, k, threshold, frequency):
    # new = dict()    # Anzhal der Subset, die zum set werden
    pos = dict()  # subset des sets
    for prev in prev_freq:
        for o in ones:
            new_or = prev | o
            if new_or != prev:
                if new_or not in pos.keys():
                    # new[new_or] = 1
                    pos[new_or] = [prev]
                else:
                    # new[new_or] += 1
                    pos[new_or].append(prev)

    next_freq = []
    neg = []
    result_pos = set()  # Subsets vom set, welches auch freq ist
    free = []
    for n in pos.keys():
        if len(pos[n]) == k:
            number, is_freq = check_freq(n, threshold)
            frequency[n] = number
            if is_freq:
                next_freq.append(n)
                result_pos |= set(pos[n])
                for subsets in pos[n]:
                    if number >= frequency[subsets]:
                        break
                else:
                    free.append(n)
            else:
                neg.append(n)
    return next_freq, neg, result_pos, free, pos


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

    frequency = dict()
    freq_ones, data, neg = read(file, threshold, frequency)
    result = [freq_ones]
    prev_freq = freq_ones

    neg_bor = [neg.copy()]
    pos_bor = [freq_ones.copy()]

    free_set = [freq_ones.copy()]
    closed_set = freq_ones.copy()

    k = 2
    while len(prev_freq) != 0:
        prev_freq, neg, pos, free, subsets_of_prefFreq = cacl_freq(prev_freq, freq_ones, k, threshold, frequency)
        neg_bor.append(neg)
        result.append(prev_freq)
        free_set.append(free)
        # print("k=", k, "Länge", len(prev_freq))

        for p in pos:
            if p in pos_bor[k - 2]:
                pos_bor[k - 2].remove(p)

        for f in prev_freq:
            for s in subsets_of_prefFreq[f]:
                if (frequency[f] >= frequency[s]):
                    if s in closed_set:
                        closed_set.remove(s)

        closed_set += prev_freq

        k += 1

        pos_bor.append(prev_freq)
        # pos_bor.append(prev_freq)

    # print(free_set)
    # print(closed_set)
    neg_tupel = number_to_tupel(neg_bor)
    pos_tupel = number_to_tupel(pos_bor)
    # return: transform number to tupel
    result_tupel = number_to_tupel(result)

    return closed_set, free_set


def create_histogram(freq, file, threshold, neg_tupel, pos_tupel):
    with open("results2/" + file + "_threshold" + str(threshold) + "_negative" + ".csv", 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for s in neg_tupel:
            spamwriter.writerow(s)

    with open("results2/" + file + "_threshold" + str(threshold) + "_positive" + ".csv", 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for s in pos_tupel:
            spamwriter.writerow([s])

    itemset_sizes_neg = []
    for i in neg_tupel:
        for l in range(len(i)):
            itemset_sizes_neg.append(len(i[0]))

    itemset_sizes_pos = []
    for i in pos_tupel:
        for l in range(len(i)):
            itemset_sizes_pos.append(len(i[0]))

        plt.hist(itemset_sizes_pos, align='left', bins=np.arange(0, len(freq) + 2, 1))
        plt.title("Frequent Itemsets")
        plt.xlabel("Size")
        plt.ylabel("Frequency")
        plt.xticks(np.arange(len(freq) + 0.5))

        plt.savefig("pictures3/" + file + "_threshold" + str(threshold) + "_negative" + ".png")
        plt.clf()

        plt.hist(itemset_sizes_neg, align='left', bins=np.arange(0, len(freq) + 2, 1))
        plt.title("Frequent Itemsets")
        plt.xlabel("Size")
        plt.ylabel("Frequency")
        plt.xticks(np.arange(len(freq) + 0.5))

        plt.savefig("pictures3/" + file + "_threshold" + str(threshold) + "_positive" + ".png")
        plt.clf()


def write_in_cvs(closed_set, free_set, threshold, file):
    with open("results/" + file + "_threshold" + str(threshold) + "_closed_set" + ".csv", 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(closed_set)

    with open("results/" + file + "_threshold" + str(threshold) + "_free_set" + ".csv", 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(free_set)


data = []

files = ["dm1.csv", "dm2.csv", "dm3.csv", "dm4.csv"]
thresholds = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
runtimes = [[""] + thresholds]
for f in files:
    times = [f]
    for th in thresholds:
        t = time.clock()
        closed_set, free_set = get_all_freq(th, f)
        seconds = time.clock() - t
        write_in_cvs(closed_set, free_set, th, f)
        # create_histogram(freq, f, t, neg, pos)
        times.append(seconds)
        print(seconds)
        # exit()
    runtimes.append(times)


with open("runtimes.csv", 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for times in runtimes:
        spamwriter.writerow([times])

