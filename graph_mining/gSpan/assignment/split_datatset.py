import algorithms as alg
import gspan_helper as gh
import csv


def split(filename, train_file, test_file):
    data, _ = alg.read_data(filename, has_header=False)
    lines = []
    t = 0
    for l in data:
        if l[0] == 't':
            t += 1
        lines.append(l)

    k = 0
    file_train = open(train_file, "w")
    file_test = open(test_file, "w")

    for i in range(len(lines)):

        if k < 2 * int(t / 3):
            for x in lines[i]:
                file_train.write(x + " ")
            if lines[i+1][0] == 't':
                k += 1

            if k >= 2 * int(t / 3):
                continue
            file_train.write("\n")


        else:
            for x in lines[i]:
                file_test.write(x + " ")
            file_test.write("\n")


def graph_mining(filename):
    test_file = "test.gsp"
    train_file = "train.gsp"
    split(filename, train_file, test_file)

    train, test, ins_pattern_blubb = gh.run_gspan(train_file, test_file, 150)

    D = [[0 for j in range(len(test))] for i in range(len(ins_pattern_blubb))]

    for i in range(len(test)):
        for j in range(len(ins_pattern_blubb)):
            if gh.graph_contains_pattern(train[i], ins_pattern_blubb[j][1]):
                D[j][i] = 1

    print(D)

   # gh.graph_contains_pattern()


graph_mining("data/bbp2.gsp")
