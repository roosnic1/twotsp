import csv
import numpy as np
import cProfile as profile

from traveling_santa import TSP
from traveling_santa_evo import EVO as EVO
from traveling_santa_evo_acs import EVO as ACS
from traveling_santa_me import ME as ME
from traveling_santa_nico import NICO as NICO

import matplotlib.pyplot as plt
import cPickle as pickle
import time


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


def doSolve(filename):
    print "*** Step 1: *** \t\t\t ***"

    if filename:
        readdump = True
    else:
        readdump = False
    # read dump
    if readdump:
        print '--- Read stored dump --- \t\t\t ---'
        dump = pickle.load(open(str(filename),'rb'))
        route0 = dump[0]
        route1 = dump[1]
        data = dump[2]
        route0_lenght = dump[3]
        route1_lenght = dump[4]
        exectime = dump[5]

    if not readdump:
        t1 = time.time()
    if not readdump:
        print "--- Reading Data --- \t\t\t ---"
        data = read_data_file('santa_cities.csv')  # id, x, y
        print "--- Sample Data --- \t\t\t ---"
        data = subset_data(data, anzpoints)


    if not readdump:
        print "*** Step 2: *** \t\t\t ***"
        print "--- Initialize Cristophiedes Heuristik --- \t\t\t ---"
        tsp = TSP(data)
        print "--- Solving Cristophiedes Heuristik --- \t\t\t ---"
        tsp.solve()
        route0 = tsp.h_tour

    print "*** Step 3: *** \t\t\t ***"
    if not readdump:
        # -- Ant Colony Optimation
        #acs = ACS(data,route0)
        #acs.solve()
        #route1 = acs.tour

        # -- Random Evo Path Generation
        # !!! evo must be initialized - not solved
        evo = EVO(data,route0)
        #evo.solve()
        #route1 = evo.tour

        # -- Using same paths  
        #route1 = list(route0)

        # -- Testing Paths
        #route0 = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,0)]
        #route0 = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,0)]

        # -- NJM Algo
        print "--- Initialize NJM-Algo --- \t\t\t ---"
        nico = NICO(route0)
        print "--- Solving NJM-Alog --- \t\t\t ---"
        route1 = nico.solve()

        # Resolving duplicates
        me = ME(evo.weights,route0, route1)
        me.solve()
        route0 = me.route0
        route1 = me.route1
    

    print "*** Step 4: *** \t\t\t ***"
   
    if not readdump:
        print "--- Calc path length --- \t\t\t ---"
        route0_lenght = evo.calc_path_lenght(route0)
        route1_lenght = evo.calc_path_lenght(route1)
    
    if not readdump:
        # calculate exectime
        t2 = time.time()
        exectime = (t2-t1)

        print "--- Saving dump --- \t\t\t ---"
        dump = (route0,route1,data,route0_lenght,route1_lenght,exectime)
        pickle.dump(dump,open(str("results/route"+str(len(route0))+".dump"),'wb'))
    
    mins = int( exectime/60 )
    secs = int( exectime - (mins * 60) )

    print "--- Print Stats ------------------------------------------"
    print ""
    print('{0} Points in {1}min {2}s'.format(len(route0), mins, secs ) )
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('Path \t Length \t longer then - \t factor ')
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('- \t {0}'.format( route0_lenght/1.5  ))
    print('0 \t {0} \t {1}'.format( route0_lenght,  route0_lenght/(route0_lenght/1.5) ))
    print('1 \t {0} \t {1} \t {2}'.format( route1_lenght,  route1_lenght/(route0_lenght/1.5), route1_lenght/route0_lenght ))
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print ""

    print "--- Print Gui --- \t\t\t ---"
    #Plot Points
    print "--- Initialize Plot --- \t\t\t ---"
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

    plt.plot(u,v,'.',color='gray')
    plt.axis([0,y,0,z])



    q = []
    w = []
    for x in range(0,len(route0)):
        data[int(route0[x][0])][1]
        q.append(data[int(route0[x][0])][1])
        w.append(data[int(route0[x][0])][2])
        q.append(data[int(route0[x][1])][1])
        w.append(data[int(route0[x][1])][2])

    a = []
    s = []
    for x in range(0,len(route1)):
        data[int(route0[x][0])][1]
        a.append(data[int(route1[x][0])][1])
        s.append(data[int(route1[x][0])][2])
        a.append(data[int(route1[x][1])][1])
        s.append(data[int(route1[x][1])][2])


    t = np.array(q)
    z = np.array(w)
    i = np.array(a)
    k = np.array(s)
    #print 'Data:'
    #print data

    #print 'Route0:'
    #print route0
    #print q
    #print t
    #t = np.arange(0., 5., 0.2)
    #print t
    plt.plot(t[0],z[0],'rs')
    plt.plot(t,z,'--', color='#1ADD1A')
    plt.plot(a[0],s[0],'ys')
    plt.plot(a,s,'--', color='#DD2121')
    plt.show()

if __name__ == '__main__':
    doSolve("results/route80me.dump")

   





