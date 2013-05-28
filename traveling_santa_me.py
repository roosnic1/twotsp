class ME(object):


    def __init__(self, weights, route0, route1):
        self.route0 = route0
        self.route1 = route1
        self.weights = weights
    
    def getNearesPoint(self,points,nearespoints):
            point = points[0]
            upper = max(self.weights[point])
            lower = upper

            if(point>1):
                lower = min( self.weights[ point ] [ 0 : point-1 ] )

            if(point<len(self.weights)-2):
                upper = min( self.weights[ point ] [ point+1 : -1 ] )

            tmp=(False,max(self.weights[point]))
            for p in enumerate(self.weights[point]):
                if p[1] <= tmp[1] and p[0] not in nearespoints and p[0] != point and p[0] != points[1]:
                    tmp = p
                    
            print('nearest point {0} is not {1}'.format(tmp[0],nearespoints))
            return tmp[0]

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
        newpt = self.getNearesPoint(route[inx],self.nearespoints)

        self.nearespoints.update({newpt:True})
        self.nearespoints.update({route[inx][0]:True})
        self.nearespoints.update({route[inx][1]:True})
        if not newpt:
            return route
        oldpt = route[inx][1]

        route[inx] = (route[inx][0],route[inx][1])
        route.insert(inx+1,(newpt,oldpt))

        manipulated1 = False
        for inx1, edge in enumerate(route):
            if manipulated1 == False and edge[0] == newpt and  inx1 != inx+1:
                route[inx1-1] = (route[inx1-1][0],route[inx1][1])
                route.remove(route[inx1])
                manipulated1 = True
        


        return route



    def solve(self):
        self.hashmap = dict()
        self.build_hasmap()
        self.nearespoints = dict()
        
        while(len(self.hashmap)>len(self.route0)*0.1):

            self.build_hasmap()        
            self.nearespoints = dict()

            if self.calc_path_lenght(self.route0) < self.calc_path_lenght(self.route1):
                
                for mapentry in self.hashmap:    
                    print('solving {0}'.format(mapentry))
                    self.route0 = self.solve_duplicate(self.route0,self.hashmap.get(mapentry)[0])
            else:
                
                for mapentry in self.hashmap:    
                    print('solving {0}'.format(mapentry))
                    self.route1 = self.solve_duplicate(self.route1,self.hashmap.get(mapentry)[0])
        
        


                            
