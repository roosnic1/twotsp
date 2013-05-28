import csv
import numpy as np
import cProfile as profile

from traveling_santa import TSP
from traveling_santa_evo import EVO as EVO
from traveling_santa_evo_acs import EVO as ACS
from traveling_santa_me import ME as ME

import matplotlib.pyplot as plt


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

    #Plot Points
    y = int(data[0][1])
    z = int(data[0][2])
    u = [int(data[0][1])]
    v = [int(data[0][2])]
    for x in range(1,len(data)):
        u.append(int(data[x][1]))
        v.append(int(data[x][2]))
        if int(data[x][1]) > y:
            y = int(data[x][1])

        if int(data[x][2]) > z:
            z = int(data[x][2])


    #print y,z
    #print u,v

    plt.plot(u,v,'bo')
    plt.axis([0,y,0,z])
    plt.show();


    print "*** Step 2: ***"
    tsp = TSP(data)
    tsp.solve()
    #tsp.plot()

    print "*** Step 3: ***"
    route0 = tsp.h_tour
    q = []
    w = []
    for x in range(0,len(route0)):
        q.append(int(route0[x][0]))
        w.append(int(route0[x][0]))

    plt.plot(q,'g-')
    plt.show()


    #acs = ACS(data,route0)
    evo = EVO(data,route0)
    #profile.run("evo.solve()")
    evo.solve()
    #acs.solve()


    route1 = evo.tour
    #route1 = acs.tour
    #route1 = list(route0)

    route0_lenght = evo.calc_path_lenght(route0)
    route1_lenght = evo.calc_path_lenght(route1)

    print "*** Step 4: ***"
    
    me = ME(evo.weights,route0, route1)
    me.solve()
 

    print('Path0: {0}'.format(evo.calc_path_lenght(me.route0)))
    print('Path0: {0}'.format(me.route0))
    print('Path1: {0}'.format(evo.calc_path_lenght(me.route1)))
    print('Path1: {0}'.format(me.route1))

    print('*** Step 5: ***')
    print "Results:"
    print('Path0: {0} / {1}'.format(evo.calc_path_lenght(me.route0), route0_lenght))
    print('Path1: {0} / {1}'.format(evo.calc_path_lenght(me.route1), route1_lenght))
    print('shortes possible Path {0}'.format(route1_lenght/1.5))
    print('path0 {0}*'.format(evo.calc_path_lenght(me.route0)/(route0_lenght/1.5)) )
    print('path1 {0}*'.format(evo.calc_path_lenght(me.route1)/(route0_lenght/1.5)) )
    print('path0-path1 {0}*'.format(evo.calc_path_lenght(me.route1)/evo.calc_path_lenght(me.route0)) )



