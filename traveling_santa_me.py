class ME(object):


    def __init__(self, weights, route0, route1):
        self.route0 = route0
        self.route1 = route1
        self.weights = weights
    
    def getNearesPoint(self,point):
            upper = max(self.weights[point])
            lower = upper

            if(point>1):
                lower = min( self.weights[ point ] [ 0 : point-1 ] )

            if(point<len(self.weights)-2):
                upper = min( self.weights[ point ] [ point+1 : -1 ] )

            for p in enumerate(self.weights[point]):
                if p[1] == min(lower,upper):
                    return p[0]

    def findDuplicates(self):
        print "# Duplicates: #"
        douplicates = 0
        for inx0, edge0 in enumerate(self.route0):
            for inx1, edge1 in enumerate(self.route1):
                if( (edge1[0] == edge0[0] and edge1[1] == edge0[1]) or (edge1[1] == edge0[0] and edge1[0] == edge0[1]) ):
                    print('duplicate ({0}) {1} and ({2}) {3}'.format(inx0, edge0, inx1, edge1))
                    douplicates += 1
        print('dupicates: {0}'.format(douplicates) )
        print('Path0: {0}'.format(self.calc_path_lenght(self.route0)))
        print('Path1: {0}'.format(self.calc_path_lenght(self.route1)))


    def calc_path_duplicates(self,route0, route1):
        duplicates = 0
        for inx0, edge0 in enumerate(route0):
            for inx1, edge1 in enumerate(route1):
                if( (edge1[0] == edge0[0] and edge1[1] == edge0[1]) or (edge1[1] == edge0[0] and edge1[0] == edge0[1]) ):
                    duplicates += 1
        return duplicates


    def calc_path_lenght(self,path):
        total  = 0
        for c in path:
            total += self.weights[c[0]][c[1]]
        return total


    def solve(self):
        while(self.calc_path_duplicates(self.route0,self.route1)):
            for inx0, edge0 in enumerate(self.route0):
                for inx1, edge1 in enumerate(self.route1):
                    if( (edge1[0] == edge0[0] and edge1[1] == edge0[1]) or (edge1[1] == edge0[0] and edge1[0] == edge0[1]) ):
                        print('solving duplicate ({0}) {1} and ({2}) {3}'.format(inx0, edge0, inx1, edge1))
                        if(self.calc_path_lenght(self.route0)<self.calc_path_lenght(self.route1)):
                            print('manipulate route0 on {0}'.format(inx0) )
                            print self.getNearesPoint(inx0)
                            self.route0.append( (self.route0[-1][1],self.route0[inx1][0]) )
                            self.route0[inx0-1] = (self.route0[inx0-1][0],self.route0[inx0][1])
                            self.route0.remove(self.route0[inx0])   
                        else:
                            print('manipulate route1 on {0}'.format(inx1) )
                            self.route1.append( (self.route1[-1][1],self.route1[inx1][0]) )
                            self.route1[inx1-1] = (self.route1[inx1-1][0],self.route1[inx1][1])
                            self.route1.remove(self.route1[inx1]) 
