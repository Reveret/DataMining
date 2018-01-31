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
    for i in range(len(count)):
        if count[i] / len(data) >= treshold:
            first.append(2 ** i)
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

def check_zor(k, x):
    #print(bin(x).count("1"))
    return bin(x).count("1") <= k
    i = 0
    #print(x)
    while x > 0:
        if x % 2 == 1:
            i += 1
        if i > k:
            return False
        #print(x)
        x = int(x / 2)
    return True

def calc(new, k, i=0, j=0, z_or=0, z_add=0):  # i: anzahl schon dazuaddierte zahl

    if i != 0 and not check_zor(k, z_or):
        return []
    if i == k:  # Wenn man k zahlen zusammenaddiert/geort hat
        if z_or * (k - 1) == z_add and check(z_or):
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
            result += calc(new, k, i + 1, l + 1, z_or | new[-l - 1], z_add + new[-l - 1])
        return result


tie = 0

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