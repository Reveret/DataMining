import numpy as np
from time import clock
from matplotlib import pyplot as plt
import csv


def apiori(threshold, input):
    def read(file):
        datei = open(file, "r")
        data = []
        for line in datei:
            data.append([int(x) for x in line.strip().split(",")])
        datei.close()
        return data

    def firstFreq(data, treshold):
        count = [0.0 for i in range(len(data[0]))]

        for i in range(len(data)):
            for j in range(len(data[0])):
                count[j] += data[i][j]
        freq = []
        for i in range(len(count)):
            if count[i] / len(data) >= treshold:
                freq.append({i})

        return freq

    def findFreq(sets, threshold, data):
        freq = []
        for s in sets:
            count = 0
            for line in data:
                if isSub(s, line):
                    count += 1
                    if float(count) / len(data) >= threshold:
                        break
            if float(count) / len(data) >= threshold:
                freq.append(s)
        return freq

    def genCand(prevSets, length):
        candidates = set()
        for ps in prevSets:
            for element in range(length):
                if not element in ps:
                    newSet = set(ps.copy())
                    newSet.add(element)
                    if newSet in candidates:  # the new set is already a candidate
                        continue
                    if allSubsAvailable(newSet, prevSets):
                        candidates.add(frozenset(newSet))
        return candidates

    def allSubsAvailable(superSet, sets):
        for element in superSet:
            subSet = superSet.copy()
            subSet.remove(element)
            if not subSet in sets:
                return False
        return True

    def isSub(subSet, superSet):
        isSubSet = True
        for element in subSet:
            if superSet[element] == 0:
                isSubSet = False
                break
        return isSubSet

    t = clock()
    data = read(input)
    freq = {}
    freqOnes = firstFreq(data, threshold)
    freq[0] = freqOnes
    candidates = genCand(freq[0], len(data))
    k = 1
    while len(candidates) > 0:
        freq[k] = findFreq(candidates, threshold, data)
        print(len(freq[k]), " elements with length ", k + 1)
        print("time elapsed: ", clock() - t)
        # print(candidates)
        candidates = genCand(freq[k], len(data))
        k += 1
    # print(freq)
    # print(freq[5])
    runtime = clock() - t


    print("Hallo",freq)

    # plotting

    #print(itemset_sizes)
    if True:
        itemset_sizes = []
        for i in range(len(freq)):
            for s in freq[i]:
                # print(s,len(s))
                itemset_sizes.append(len(s))

        plt.hist(itemset_sizes, align='left', bins=np.arange(0, len(freq) + 2, 1))
        plt.title("Frequent Itemsets")
        plt.xlabel("Size")
        plt.ylabel("Frequency")
        plt.xticks(np.arange(len(freq) + 0.5))

        plt.savefig("pictures/" + input + "_threshold" + str(threshold) + "_runtime" + str(runtime) + ".png")
        plt.clf()



apiori(0.4, "dm1.csv")

exit()
data = ["dm1.csv","dm2.csv","dm3.csv","dm4.csv"]
for d in data:
    for i in range(6):
        apiori((9-i)/10, d)