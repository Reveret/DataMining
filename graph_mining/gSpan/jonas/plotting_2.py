import matplotlib.pyplot as plt
import numpy as np

data_score_1 = [[] for _ in range(7)]
data_num_1 = [[] for _ in range(7)]
data_score_2 = [[] for _ in range(7)]
data_num_2 = [[] for _ in range(7)]
x = np.arange(0.3, 0.9, 0.1)

for m in range(10):
    with open(r"analyse\analyse{}.txt".format(m)) as f:
        for j, line in enumerate(f):
            i = j // 3
            if line.startswith("->"):
                pass
            elif line.startswith("bbp2"):
                try:
                    d = [float(e) for e in line.split(":")[1].split("--")]  #
                    data_score_1[i].append(d[0])
                    data_num_1[i].append(d[1])
                except ValueError:
                    data_num_1[i].append(0)
            elif line.startswith("molecules"):
                try:
                    d = [float(e) for e in line.split(":")[1].split("--")]
                    data_score_2[i].append(d[0])
                    data_num_2[i].append(d[1])
                except ValueError:
                    data_num_2[i].append(0)


for i in range(7):
    data_num_1[i] = list(set(data_num_1[i]))
    data_num_2[i] = list(set(data_num_2[i]))
    data_score_1[i] = list(set(data_score_1[i]))
    data_score_2[i] = list(set(data_score_2[i]))

new = []
for i in range(7):
    s = np.array(data_score_1[i])
    if not len(s) == 0:
        new.append(s.mean())

plt.plot(x[:min(len(new), len(x))], new, ls="--", marker="o", label="bbp2")

new = []
for i in range(7):
    s = np.array(data_score_2[i])
    if not len(s) == 0:
        new.append(s.mean())

plt.plot(x[:min(len(new), len(x))], new, ls="--", marker="o", label="molecules")
plt.title("RF scores")
plt.legend()
plt.show()
