##########################################################################################
##########################################################################################
##                                                                                      ## 
## Dieser Code ist im Rahmen der Projektarbeit des Moduls Softwareprojekt 2             ##
## im Zeitraum vom 20.02.2013 bis 30.05.2013 entstanden.                                ##
##                                                                                      ##
## Authoren: Jeremie Blaser, Nicolas Roos, Martin Eigenmann                             ##
## Version: 1.0                                                                         ##
##                                                                                      ##
## - Alle Rechte Vorbehalten -                                                          ##
##                                                                                      ##
## ------------------------------------------------------------------------------------ ##
## Diese Datei gibt bei der Ausfuehrung alle Relevanten Daten aus den Dumps aus.        ##
## Diese Datei dient zur Vereinfachung der Handhabung waehrend der Dokumentationsphase. ##
##                                                                                      ##
## Aufruf: python results.py                                                            ##
##                                                                                      ##
##########################################################################################
##########################################################################################

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



def doSolve(filename):



    print '--- Read stored dump --- \t\t\t ---'
    dump = pickle.load(open(str(filename),'rb'))
    route0 = dump[0]
    route1 = dump[1]
    data = dump[2]
    route0_lenght = dump[3]
    route1_lenght = dump[4]
    exectime = dump[5]


    
    mins = int( exectime/60 )
    secs = int( exectime - (mins * 60) )

    print "--- Print Stats ------------------------------------------"
    print ""
    print filename
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
    #return False
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
    print "*************************** 25 ****************************************"
    doSolve("results/route25me.dump")
    doSolve("results/route25evo.dump")
    doSolve("results/route25aco.dump")
    doSolve("results/route25.dump")

    print "*************************** 80 ****************************************"
    doSolve("results/route80me.dump")
    doSolve("results/route80evo.dump")
    doSolve("results/route80aco.dump")
    doSolve("results/route80.dump")

    print "*************************** 200 ****************************************"
    doSolve("results/route200evo.dump")
    doSolve("results/route200.dump")

    print "*************************** 400 ****************************************"
    doSolve("results/route400evo.dump")
    doSolve("results/route400.dump")

    print "*************************** 1000 ****************************************"
    doSolve("results/route1000.dump")
   
    print "*************************** 5000 ****************************************"
    doSolve("results/route5000.dump")

    print "*************************** 15000 ****************************************"
    doSolve("results/route15000.dump")





