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


    def calc_path_lenght(self,path):
        total  = 0
        for c in path:
            total += self.weights[c[0]][c[1]]
        return total

    def build_hasmap(self):
        self.hashmap = dict()
        for inx,edge in enumerate(self.route0):
            if edge[0] > edge[1]:
                edgehash = str(edge[0])+str(edge[1])
            else:
                edgehash = str(edge[1])+str(edge[0])

            self.hashmap.update({edgehash:(inx,False)})

        for inx,edge in enumerate(self.route1):
            if edge[0] > edge[1]:
                edgehash = str(edge[0])+str(edge[1])
            else:
                edgehash = str(edge[1])+str(edge[0])

            if edgehash in self.hashmap:
                oldinx = self.hashmap.get(edgehash)[0]
                self.hashmap.update({edgehash:(oldinx,inx)})

        for inx,edge in enumerate(self.route0):
            if edge[0] > edge[1]:
                edgehash = str(edge[0])+str(edge[1])
            else:
                edgehash = str(edge[1])+str(edge[0])

            if self.hashmap.get(edgehash)[1] == False:
                del self.hashmap[edgehash]
    def solve_duplicate(self,route,inx):

        


        return route

    def solve(self):
        self.hashmap = dict()

        while(len(self.hashmap)>0):
            self.build_hasmap()

            for mapentry in self.hashmap:
                if self.calc_path_lenght(self.route0) > elf.calc_path_lenght(self.route1):
                    self.route1 = self.solve_duplicate(self.route1,self.hashmap.get(mapentry)[1])
                else:
                    self.route0 = self.solve_duplicate(self.route0,self.hashmap.get(mapentry)[0])
        
        


                            
