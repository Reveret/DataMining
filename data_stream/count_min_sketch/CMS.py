import mmh3
import math
import matplotlib.pyplot as plt


# -*- coding: utf-8 -*-

class CMS(object):
    def __init__(self, eps, delt):
        """
        w size of hash tables
        d number of hash functions
        """
        self.w = math.ceil(math.e / eps)
        self.d = math.ceil(math.log(1 / delt, math.e))
        self.N = 0

        self.hash_table = [x for x in range(self.d)]
        self.tables = [[0 for j in range(self.w)] for i in range(self.d)]

    def hash(self, inp, i):
        return mmh3.hash128(inp, self.hash_table[i]) % self.w

    def add(self, inp):
        self.N += 1
        for i in range(self.d):
            hashValue = self.hash(inp, i)
            self.tables[i][hashValue] += 1

    def estimate(self, inp):
        e = float("inf")
        for i in range(self.d):
            hashValue = self.hash(inp, i)
            e = min(e, self.tables[i][hashValue])
        return e


def stram_mining(file):
    delt = [0.02, 0.01, 0.002, 0.0001, 0.00001]
    eps = [0.4, 0.04, 0.002]

    for k in delt:
        for l in eps:
            print("eps, delt", l, k)
            cms = CMS(l, k)
            find = ["Caffeine", "Acetaminophen", "Trimethadione", "Diltiazem"]

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

            for i in range(len(find)):
                plt.close()
                plt.plot(plot_table[i])
                plt.savefig("results/"+find[i]+"_eps="+str(l)+"delt="+str(k)+".jpg")


stram_mining("tweets.csv")


