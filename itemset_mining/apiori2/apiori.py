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
        neg = []
        for i in range(len(count)):
            if count[i] / len(data) >= treshold:
                freq.append(frozenset([i]))
            else:
                neg.append(frozenset([i]))

        return freq, neg

    def findFreq(sets, threshold, data):
        freq = []
        neg = []
        for s in sets:
            count = 0
            for line in data:
                if isSub(s, line):
                    count += 1
                    if float(count) / len(data) >= threshold:
                        break
            if float(count) / len(data) >= threshold:
                freq.append(s)
            else:
                neg.append(s)
        return freq, neg

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
    freqOnes, neg = firstFreq(data, threshold)
    freq[0] = freqOnes
    candidates = genCand(freq[0], len(data))
    k = 1
    negBor = neg
    posBor = freqOnes
    while len(candidates) > 0:
        freq[k], neg = findFreq(candidates, threshold, data)
        negBor += neg
        for freq_set in freq[k]:
            for ele in freq_set:
                old_pos = set(freq_set.copy())
                old_pos.remove(ele)
                if old_pos in posBor:
                    posBor.remove(old_pos)
        posBor += freq[k]
        # print(len(freq[k]), " elements with length ", k + 1)
        # print("time elapsed: ", clock() - t)
        # print(candidates)
        candidates = genCand(freq[k], len(data))
        k += 1
    print("data: ", input, "Threshold", threshold, "neg", negBor)
    print("data: ", input, "Threshold", threshold, "pos", posBor)
    # print(freq[5])
    runtime = clock() - t

    itemset_sizes_pos = [len(posBor[i]) for i in range(len(posBor))]
    itemset_sizes_neg = [len(negBor[i]) for i in range(len(negBor))]
    # print("item", itemset_sizes)
    # plotting

    # print(itemset_sizes)

    with open("results/"+ input + "_threshold" + str(threshold) + "_negative" +".csv", 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for s in negBor:
            spamwriter.writerow(s)

    with open("results/"+ input + "_threshold" + str(threshold) + "_positive" +".csv", 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for s in posBor:
            spamwriter.writerow(s)






    if True:
        plt.hist(itemset_sizes_pos, align='left', bins=np.arange(0, len(freq) + 2, 1))
        plt.title("Frequent Itemsets")
        plt.xlabel("Size")
        plt.ylabel("Frequency")
        plt.xticks(np.arange(len(freq) + 0.5))

        plt.savefig("pictures/" + input + "_threshold" + str(threshold) + "_negative" + "_runtime" + str(runtime) + ".png")
        plt.clf()

        plt.hist(itemset_sizes_neg, align='left', bins=np.arange(0, len(freq) + 2, 1))
        plt.title("Frequent Itemsets")
        plt.xlabel("Size")
        plt.ylabel("Frequency")
        plt.xticks(np.arange(len(freq) + 0.5))

        plt.savefig("pictures/" + input + "_threshold" + str(threshold) + "_positive" + "_runtime" + str(runtime) + ".png")
        plt.clf()


# t =clock()
# apiori(0.6, "dm4.csv")
# print(clock()-t)

apiori(0.4, "dm1.csv")
exit()

data = ["dm1.csv", "dm2.csv", "dm3.csv", "dm4.csv"]
for d in data:
    for i in range(6):
        apiori((9 - i) / 10, d)
