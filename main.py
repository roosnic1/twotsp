import csv
import numpy as np
#import cProfile as profile

from traveling_santa import TSP
from traveling_santa_evo import EVO


def read_data_file(file):
    basedir = 'data/'
    filename = basedir + file
    csv_file_object = csv.reader(open(filename, 'r'))
    #skip header
    csv_file_object.next()
    data = []
    for row in csv_file_object:
        data.append(row)
    #Convert from a list to an array (to make it easier to do math with numpy). Each item is currently a string in this format
    data = np.array(data)
    return data


def subsample_data(data, size):
    samples = []
    for i in range(0, len(data), len(data) / size):
        samples.append(data[i])
    return np.array(samples)


def subset_data(data, size):
    samples = []
    for i in range(0, size):
        samples.append(data[i])
    return np.array(samples)


if __name__ == '__main__':
    print "*** Step 1: ***"
    data = read_data_file('santa_cities.csv')  # id, x, y
    data = subset_data(data, 15)

    print "*** Step 2: ***"
    tsp = TSP(data)
    tsp.solve()

    print "*** Step 3: ***"
    evo = EVO(data)
    evo.solve()

    print "*** Step 4: ***"
    print "Results:"
    print "[Name]Algo: ", tsp.best_tour_len
    print "evolutionary algo: ", evo.best_tour_len
    tsp.plot(showMST=False, labelNodes=True)
    evo.plot(showMST=False, labelNodes=False)
    #profile.run('tsp.plot(showMST=True)')
