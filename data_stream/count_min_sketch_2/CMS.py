import mmh3
import math
import matplotlib.pyplot as plt
import time


# -*- coding: utf-8 -*-

class CMS(object):
    def __init__(self, eps, delt):
        """
        w size of hash tables
        d number of hash functions
        """
        self.w = math.ceil(math.e / eps)    # HAshtabbelengröße
        self.d = math.ceil(math.log(1 / delt, math.e))  # Anzahl der Hashfunktionen
        self.N = 0

        self.hash_table = [x for x in range(self.d)]
        self.tables = [[0 for j in range(self.w)] for i in range(self.d)]

    def hash(self, inp, i):
        return mmh3.hash128(inp, self.hash_table[i]) % self.w

<<<<<<< HEAD
    def add(self, inp):
=======
    # Füge das Wort in die Tabellen ein
    def add(self, input):
>>>>>>> 6526b5433a70813d561a4fe982ddbcccd6c45343
        self.N += 1
        for i in range(self.d):
            hashValue = self.hash(inp, i)
            self.tables[i][hashValue] += 1

<<<<<<< HEAD
    def estimate(self, inp):
=======
    # Prüfe wie oft das wort input in der Tabelle "gezählt" wurde, lese die Obergrenze
    def estimate(self, input):
>>>>>>> 6526b5433a70813d561a4fe982ddbcccd6c45343
        e = float("inf")
        for i in range(self.d):
            hashValue = self.hash(inp, i)
            e = min(e, self.tables[i][hashValue])
        return e


def stream_mining(file):
    delt = [0.02, 0.0000001]
    eps = [0.04, 0.042, 0.00001]
    find = ["Caffeine", "Acetaminophen", "Trimethadione", "Diltiazem"]

    # save the results to plot at the end
    results = [[[] for j in range(len(eps))] for i in range(len(delt))]

    runtimes = [[0 for j in range(len(eps))] for i in range(len(delt))]

    z = 0
    for k in delt:
        y = 0
        for l in eps:
            t0 = time.time()
            print("eps, delt", l, k)
            cms = CMS(l, k)


            plot_table = [[] for i in range(len(find))]

            n = 0
            for line in open(file):
                row = line.strip().split(",")
                for i in range(3, len(row)):
                    for word in row[i].split(" "):
                        cms.add(word)


                for i in range(len(find)):
                    plot_table[i].append(cms.estimate(find[i]))
                #print("Line", n)
                cms.estimate("Caffeine")
                n += 1

            t1 = time.time()

            runtimes[z][y] = t1-t0
            results[z][y] = plot_table

            y += 1
        z += 1


    # Create plot
    for a in range(len(find)):
        plt.close()
        for b in range(len(eps)):
            for c in range(len(delt)):
                plt.plot(results[c][b][a], label="eps="+str(eps[b])+" delt="+str(delt[c]))

        plt.legend()
        plt.title(str(find[a]))
        plt.xlabel("Number of tweets")
        plt.ylabel("Number of found "+find[a])
        plt.savefig("results2/" + find[a] + ".jpg")


    print("", end="\t")
    for c in range(len(delt)):
        print(delt[c], end="\t")
    print()
    for b in range(len(eps)):
        print(eps[b], end="\t")
        for c in range(len(delt)):
            print(runtimes[c][b], end="\t")
        print()


    plt.savefig("results2/"+find[i]+".jpg")     # +"_eps="+str(l)+"delt="+str(k)+


stream_mining("tweets.csv")


