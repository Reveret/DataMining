import matplotlib.pyplot as plt

x = []
score1 = []
score2 = []
numPat1 = []
numPat2 = []

inp = open("analyse.txt")
for line in inp:
    if line.startswith("->"):
        x.append(float(line.split(":")[1].strip()))
    elif line.startswith("bbp2"):
        try:
            d = [float(e) for e in line.split(":")[1].split("--")]#
            score1.append(d[0])
            numPat1.append(d[1])
        except ValueError:
            numPat1.append(0)
    elif line.startswith("molecules"):
        try:
            d = [float(e) for e in line.split(":")[1].split("--")]
            score2.append(d[0])
            numPat2.append(d[1])
        except ValueError:
            numPat2.append(0)
    else:
        print("ERROR!")

inp.close()

fig, ax = plt.subplots(nrows=2)

ax[0].plot(x[:min(len(score1), len(x))], score1, ls="--", marker="o", label="bbp2")
ax[0].plot(x[:min(len(score2), len(x))], score2, ls="--", marker="o", label="molecules")
ax[0].set_title("RF scores")
ax[0].legend()

ax[1].plot(x, [e / max(numPat1) for e in numPat1], label="bbp2")
ax[1].plot(x, [e / max(numPat2) for e in numPat2], label="molecules")
ax[1].set_title("Freq patterns relative")
ax[1].legend()

fig.subplots_adjust(hspace=0.3)


plt.show()
