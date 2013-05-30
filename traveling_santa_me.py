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

            try:
                if self.hashmap.get(edgehash)[1] == False:
                    del self.hashmap[edgehash]
            except Exception:
                pass


    def solve_duplicate(self,route,inx):
        newpt = self.getNearesPoint(route[inx],self.nearespoints)

        self.nearespoints.update({newpt:True})
        self.nearespoints.update({route[inx][0]:True})
        self.nearespoints.update({route[inx][1]:True})
        if not newpt:
            return route

        
        route.insert(inx+1,(newpt,route[inx][1]))
        route[inx] = (route[inx][0],newpt)

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
        self.nearespointsOld = dict({'00':False})
        self.hashmapOld = dict({'old':(False,False)})
        self.hashmapOldOld = dict({'old':(False,False)})

        # Alle Duplikate finden und loesen
        # self.hashmap beinhaltet referenzen zu allen Duplikate => Zugriff und Erkennund der Duplikate in O(n)
        while(len(self.hashmap)> 0 and self.hashmapOld != self.hashmap and self.hashmapOldOld != self.hashmapOld):
            # self.nearestpoints beinhaltet eine Liste der geometrisch nahesten Punkte
            self.nearespoints = dict()
            # Falls route0 kuerzer als route1 ist, werden alle Duplikate in route0 geloest
            if self.calc_path_lenght(self.route0) < self.calc_path_lenght(self.route1):      
                for mapentry in self.hashmap:    
                    print('solving {0}'.format(mapentry))
                    self.route0 = self.solve_duplicate(self.route0,self.hashmap.get(mapentry)[0])
            else:           
                for mapentry in self.hashmap:    
                    print('solving {0}'.format(mapentry))
                    self.route1 = self.solve_duplicate(self.route1,self.hashmap.get(mapentry)[1])
            # Erkennung von Endlos-Schleifen
            self.hashmapOldOld = self.hashmapOld
            self.hashmapOld = self.hashmap
            # ev. neu entstandene Duplikate finden
            self.build_hasmap()

        print('{0} remaining unsolved duplicates'.format(len(self.hashmap)))
        
        inxold = False
        while(len(self.hashmap)> 0):
            
            if(self.calc_path_lenght(self.route0)<self.calc_path_lenght(self.route1)):
                for mapentry in self.hashmap:                     
                    inx = self.hashmap.get(mapentry)[0]
                    print('manipulate route0 on {0}'.format(inx) )
                    print self.route0
                    self.route0.append( (self.route0[-1][1],self.route0[inx][0]) )
                    self.route0[inx-1] = (self.route0[inx-1][0],self.route0[inx][1])
                    self.route0.remove(self.route0[inx])   
            else:
                for mapentry in self.hashmap:
                    inx = self.hashmap.get(mapentry)[1] 
                    print('manipulate route1 on {0}'.format(inx) )
                    print self.route1
                    self.route1.append( (self.route1[-1][1],self.route1[inx][0]) )
                    self.route1[inx-1] = (self.route1[inx-1][0],self.route1[inx][1])
                    self.route1.remove(self.route1[inx]) 

            if inx == inxold and (inx == len(self.route0) or inx == len(self.route0)-1 or inx == len(self.route0)-2):
                self.hashmap=dict()
            else:
                self.build_hasmap()

            inxold = inx
            self.build_hasmap()
            print "-----------------------------------------------------"
            print('{0} remaining unsolved duplicates'.format(len(self.hashmap)))



        


                            
