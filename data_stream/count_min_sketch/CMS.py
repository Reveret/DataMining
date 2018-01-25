import mmh3
import math


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

    def hash(self, input, i):
        return mmh3.hash128(input, self.hash_table[i]) % self.w

    def add(self, input):
        self.N += 1
        for i in range(self.d):
            hashValue = self.hash(input, i)
            self.tables[i][hashValue] += 1

    def estimate(self, input):
        e = float("inf")
        for i in range(self.d):
            hashValue = self.hash(input, i)
            e = min(e, self.tables[i][hashValue])
        return e


def stram_mining(file):
    cms = CMS(0.4, 0.02)

    f = open(file, 'r')
    line = f.readline().strip().split(",")
    n = 0
    while line != "":
        for i in range(3, len(line)):
            for words in line[i].split(" "):
                cms.add(words)

        line = f.readline().strip().split(",")
        print("Line", n)
        n += 1




stram_mining("tweets.csv")
