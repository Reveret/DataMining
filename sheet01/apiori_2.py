import numpy
import time


def read2(file, treshold):
    datei = open(file, "r")
    data = []
    count = None
    for line in datei:
        tmp = [int(x) for x in line.strip().split(",")]
        number = 0
        if count == None:
            count = [0 for i in range(len(tmp))]

        for i in range(len(tmp)):
            if tmp[i] == 1:
                count[i] += 1
                number += 2 ** i

        data.append(number)
    datei.close()
    first = []
    global freq_set
    for i in range(len(count)):
        if count[i] / len(data) >= treshold:
            first.append(2 ** i)

            freq_set.update({2**i: {i}})
            #print(freq_set)
    return first, data


def check(x):
    global data, trashold
    count = 0
    min = len(data) * trashold
    for n in data:
        if n & x == x:
            count += 1
        if count >= min:
            return True
    return count >= min


def calc(new, k, i=0, j=0, z_or=0, z_add=0, set=set()):  # i: anzahl schon dazuaddierte zahl
    global freq_set
    #print(set, len(set), k)
    if i != 0 and (len(set)>k-1+i or len(set)>k):
        #print("Muh")
        return []
    if i == k:  # Wenn man k zahlen zusammenaddiert/geort hat
        if z_or * (k - 1) == z_add and check(z_or):
            freq_set.update({z_or:set})
            return [z_or]
        else:
            return []
    else:
        result = []
        for l in range(j, len(new)-(k-i)+1):
            if j == 0 and False:
                print(k)
            if k > len(new) - j + i:
                break
          #  print(freq_set.get(new[-l - 1]), -l-1)
            global tie
            t = time.clock()
            x = set.copy()
            for s in freq_set.get(new[-l - 1]):
                x.add(s)
            tie += time.clock()-t
            result += calc(new, k, i + 1, l + 1, z_or | new[-l - 1], z_add + new[-l - 1], set | freq_set.get(new[-l - 1]))
        return result


tie = 0
freq_set = {}

def myprog():
    global data, trashold
    trashold = 0.6
    first, data = read2("dm4.csv", trashold)
    #print("First", first)

    result = [first]

    for i in range(2, len(first)):
        t1 = time.clock()
        print("i", i-1, "länge", len(result[i - 2]))
        tmp = calc(result[i - 2], i)
        print("Time:", time.clock()-t1)
        if tmp == []:
            break

        result.append(tmp)
        # print(result[i - 2])

    result1 = []
    #print("result", result)
    for x in result:
        for i in range(len(x)):
            number = set()
            a = x[i]
            j = 1
            # print("AAAAA", a%2)
            while a != 0:
                # print(a)
                # print("AAAAA", a % 2, j)
                if a % 2 == 1:
                    number |= {j}
                j += 1
                a = int(a / 2)
            sorted(number)
            result1.append(number)

    print(result1)



t = time.clock()
myprog()
print(time.clock()-t)

print("Vergleichzeit", tie)