import math
import matplotlib.pyplot as plt


def likelihood(x, u, o, p, n_clusters):
    return sum([math.log(sum([p[k] * f(x_e, u[k], o[k]) for k in range(n_clusters)])) for x_e in x])


def f(x, u, o):
    return math.exp(-math.pow(x - u, 2) / (2 * math.pow(o, 2))) / (math.sqrt(2 * math.pi) * o)


def e_step(x, u, o, p, n_clusters):
    w = [[0 for _ in range(len(x))] for _ in range(n_clusters)]
    for i in range(len(x)):
        p_x = sum([f(x[i], u[k], o[k]) * p[k] for k in range(n_clusters)])
        for k in range(n_clusters):
            w[k][i] = f(x[i], u[k], o[k]) * p[k] / p_x
    return w


def m_step(x, u, o, w, p, n_clusters):
    for k in range(n_clusters):
        try:
            u[k] = sum([w[k][i] * x[i] for i in range(len(x))]) / sum(w[k])
        except ZeroDivisionError:
            print(w[k])
        o[k] = sum([w[k][i] * (x[i] - u[k]) ** 2 for i in range(len(x))]) / sum(w[k])
        o[k] = math.sqrt(o[k])


def read_data(filename):
    fl = open(filename, "r")
    data = []
    for line in fl:
        data.append(float(line))
    return data


# This example
probs = [0.6, 0.4]  # list of probabilities for clusters
my = [1, 4]  # initial values for my
sigma = [1, 1]  # initial values for sigma
weights = None  # matrix of probabilities for every point and every cluster
lhs = []

num_clusters = 2  # Number of clusters
max_iters = 20  # Max number of iterations
iters = 0

data = read_data("EM-data.csv")  # Read in data
out_file = open("output.txt", "w", encoding="UTF-16")

# While not max iterations are reached or any changes to the likelihood occur
old_likelihood = None
while old_likelihood != likelihood(data, my, sigma, probs, num_clusters) and iters < max_iters:
    iters += 1
    old_likelihood = likelihood(data, my, sigma, probs, num_clusters)
    weights = e_step(data, my, sigma, probs, num_clusters)
    m_step(data, my, sigma, weights, probs, num_clusters)
    lhs.append(likelihood(data, my, sigma, probs, num_clusters))
    output = ("{}. Iteration" + "\n" +
              "{}: {}" + "\n" +
              "{}: {}" + "\n" +
              "likelihood: {}" + "\n").format(iters, chr(181), my, chr(963), sigma, lhs[-1])
    # To Screen
    print(output)
    print()

    # To File
    out_file.write(output)
    out_file.write("\n")

out_file.close()


def plot(x, u, o, n_clusters, it, hoods):
    x.sort()
    for k in range(n_clusters):
        line = plt.plot(x, [f(x_e, u[k], o[k]) for x_e in x],
                        label="{}={}  {}={}".format(chr(181), round(u[k], 4), chr(963), round(o[k], 4)))
        plt.plot([u[k], u[k]], [0, line[0].get_ydata().max()], ls="--", color=line[0].get_color())
    plt.legend()
    plt.xlabel("X")
    plt.ylabel("{}(X | {}, {})".format(chr(966), chr(181), chr(963)))
    plt.title("Density - {} Iterations".format(it) if it == max_iters - 1 else "Density - Completed evaluation")
    plt.show()

    plt.plot(hoods)
    plt.title("Likelihood - {} Iterations".format(it))
    plt.show()


plot(data, my, sigma, num_clusters, iters, lhs)
