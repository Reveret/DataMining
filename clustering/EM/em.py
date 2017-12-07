# -*- coding: cp1252 -*-
import math


def likelihood(x, u, o, p, num_clusters):
    return sum([math.log(sum([p[k] * f(x[i], u[k], o[k]) for k in range(num_clusters)])) for i in range(len(x))])


def f(x, u, o):
    return (1 / math.sqrt(2 * math.pi * o)) * math.e ** (-(x - u) ** 2 / (2 * o ** 2))


def m_step(x, u, o, p, num_clusters):
    for k in range(num_clusters):
        try:
            u[k] = sum([w[k][i] * x[i] for i in range(len(x))]) / sum(w[k])
        except ZeroDivisionError:
            print(w[k])
        o[k] = sum([w[k][i] * (x[i] - u[k]) ** 2 for i in range(len(x))]) / sum(w[k])
        o[k] = math.sqrt(o[k])


def e_step(x, u, o, p, num_clusters):
    w = [[0 for _ in range(len(x))] for _ in range(num_clusters)]
    for i in range(len(x)):
        p_x = sum([f(x[i], u[k], o[k]) * p[k] for k in range(num_clusters)])
        for k in range(num_clusters):
            w[k][i] = f(x[i], u[k], o[k]) * p[k] / p_x
    return w


def read_data(filename):
    f = open(filename, "r")
    x = []
    for line in f:
        x.append(float(line))
    return x


p = []  # liste der verteilung
w = []  # liste der wahrscheinlichkeiten
u = []  # mü fürs cluster
o = []  # roh für cluster

## This example
p = [0.5, 0.5]
u = [1, 4]
o = [1, 1]
x = read_data("EM-data.csv")
num_clusters = 2
max_iters = 20

old_likeli = None
while old_likeli != likelihood(x, u, o, p, num_clusters) and max_iters >= 0:
    max_iters -= 1
    print(likelihood(x, u, o, p, num_clusters))
    w = e_step(x, u, o, p, num_clusters)
    m_step(x, u, o, p, num_clusters)

print("u:", u)
print("o:", o)
