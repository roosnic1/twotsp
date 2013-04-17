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
    route0 = tsp.h_tour

    evo = EVO(data,route0)
    evo.solve()

    route1 = evo.tour

    route0_lenght = evo.calc_path_lenght(route0)
    route1_lenght = evo.calc_path_lenght(route1)

    print "*** Step 4: ***"
    print "# Duplicates: #"
    douplicates = 0
    for inx0, edge0 in enumerate(route0):
        for inx1, edge1 in enumerate(route1):
            if( (edge1[0] == edge0[0] and edge1[1] == edge0[1]) or (edge1[1] == edge0[0] and edge1[0] == edge0[1]) ):
                print('duplicate ({0}) {1} and ({2}) {3}'.format(inx0, edge0, inx1, edge1))
                douplicates += 1
    print('dupicates: {0}'.format(douplicates) )
    print('Path0: {0}'.format(evo.calc_path_lenght(route0)))
    print('Path1: {0}'.format(evo.calc_path_lenght(route1)))

    print('*** Step 4.1: ***')

    while(evo.calc_path_duplicates(route0,route1)):
        for inx0, edge0 in enumerate(route0):
            for inx1, edge1 in enumerate(route1):
                if( (edge1[0] == edge0[0] and edge1[1] == edge0[1]) or (edge1[1] == edge0[0] and edge1[0] == edge0[1]) ):
                    print('solving duplicate ({0}) {1} and ({2}) {3}'.format(inx0, edge0, inx1, edge1))
                    if(evo.calc_path_lenght(route0)<evo.calc_path_lenght(route1)):
                        print('manipulate route0 on {0}'.format(inx0) )
                        route0.append( (route0[-1][1],route0[inx1][0]) )
                        route0[inx0-1] = (route0[inx0-1][0],route0[inx0][1])
                        route0.remove(route0[inx0])   
                    else:
                        print('manipulate route1 on {0}'.format(inx1) )
                        route1.append( (route1[-1][1],route1[inx1][0]) )
                        route1[inx1-1] = (route1[inx1-1][0],route1[inx1][1])
                        route1.remove(route1[inx1]) 

    print('Path0: {0}'.format(evo.calc_path_lenght(route0)))
    print('Path0: {0}'.format(route0))
    print('Path1: {0}'.format(evo.calc_path_lenght(route1)))
    print('Path1: {0}'.format(route1))

    print('*** Step 5: ***')
    print "Results:"
    print('Path0: {0} / {1}'.format(evo.calc_path_lenght(route0), route0_lenght))
    print('Path1: {0} / {1}'.format(evo.calc_path_lenght(route1), route1_lenght))
