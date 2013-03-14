import csv
import numpy as np
#import cProfile as profile

from traveling_santa import TSP


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


if __name__ == '__main__':
    data = read_data_file('santa_cities.csv')  # id, x, y
    data = subsample_data(data, 50)
    tsp = TSP(data)
    tsp.solve()

    tsp.plot(showMST=True, labelNodes=True)
    #profile.run('tsp.plot(showMST=True)')




