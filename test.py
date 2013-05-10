from main import read_data_file, subset_data, TSP

if __name__ == '__main__':
    print "Test"
    data = read_data_file('santa_cities.csv')

    for i in range(190, 1000):
        print '\n -- Test run', i
        sdata = subset_data(data, i)
        tsp = TSP(sdata)
        tsp.solve()