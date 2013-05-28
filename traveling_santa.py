import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.delaunay as triang
import matplotlib.patches as patch
import math as m
import time
from networkx.algorithms.matching import max_weight_matching

class TSP(object):
    """Travelling Santa Problem"""

    def __init__(self, data):
        super(TSP, self).__init__()
        self.data = data
        self.city_ids = data[0::, 0]
        self.x = data[0::, 1].astype(np.float)
        self.y = data[0::, 2].astype(np.float)
        self.build_mesh()
        self.build_distance_graph()

    def solve(self):
        """ Solve the TSP with Christofides-Heuristic"""
        self.compute_MST()
        self.find_odd_degree_nodes()
        self.find_minimum_weight_matching()
        self.find_euler_tour()
        self.find_hamilton_tour()

    def build_mesh(self):
        print 'triangulating ...'
        circumcenters, edges, tri_points, tri_neighbors = triang.delaunay(self.x, self.y)
        self.tri_points = tri_points
        self.edges = edges

    def build_distance_graph(self):
        print "build graph"
        self.xy = np.array((self.x, self.y))
        g = nx.Graph()
        g.dist_func = self.euclidean_dist
        for i, j in self.edges:
            g.add_edge(i, j, weight=g.dist_func(i, j))
        self.g = g
        print '#edges:', len(self.edges), '#nodes:', len(self.x)

    def euclidean_dist(self, i, j):
        d = self.xy[:,i] - self.xy[:,j]
        return np.sqrt(np.dot(d, d))

    def calc_path_length(self, path):
        plen = 0
        for i, j in path:
            plen += self.g.dist_func(i, j)
        return plen

    def compute_MST(self):
        print "computing MST"
        t1 = time.time()
        self.mst = nx.minimum_spanning_tree(self.g)
        t2 = time.time()
        print "took %s" % (t2-t1)

    def find_odd_degree_nodes(self):
        odd_nodes = []
        for n in self.mst.nodes_iter():
            if nx.degree(self.mst, n) & 1:
                odd_nodes.append(n)
        #print odd_nodes
        self.odd_deg_nodes = odd_nodes

    def find_minimum_weight_matching(self):
        """ finds a minimum weight perfect matching"""
        print "computing delaunay of odd_deg_nodes"
        circumcenters, edges, tri_points, tri_neighbors = triang.delaunay(self.x[self.odd_deg_nodes], self.y[self.odd_deg_nodes])
        o = nx.Graph()
        o.dist_func = lambda i,j: -self.euclidean_dist(i,j)
        for i, j in edges:
            mi = self.odd_deg_nodes[i]
            mj = self.odd_deg_nodes[j]
            o.add_edge(mi, mj, weight=o.dist_func(mi, mj))
        self.o = o
        print '#edges:', len(edges), '#odd_deg_nodes:', len(o.nodes()), len(self.odd_deg_nodes)
        print "computing minimum matching"
        t1 = time.time()
        mates = max_weight_matching(o, maxcardinality=True)
        t2 = time.time()
        print "took %s" % (t2-t1)        
        m = nx.Graph()
        for i in mates.keys():
            m.add_edge(i,mates[i], weight=self.g.dist_func(i,mates[i]))
        print '#edges:', len(m.edges()), '#nodes:', len(m.nodes())
        self.min_matching = m

    def find_euler_tour(self, nx_euler=False):
        h = nx.MultiGraph()
        h.add_edges_from(self.mst.edges())
        h.add_edges_from(self.min_matching.edges())
        if not nx.is_eulerian(h):
            raise ValueError('h must be eulerian')
        print "find euler tour"
        t1 = time.time()
        if nx_euler:
            euler_edges = nx.eulerian_circuit(h)
            self.euler_path = [e for e in euler_edges]
        else:
            self.euler_path = self.build_euler_tour(h)
        t2 = time.time()
        print "took %s" % (t2-t1) 
        print "euler path: ", self.euler_path
        print '#edges:', len(self.euler_path), '#nodes:', len(h.nodes())
        #self.plot_edges(self.euler_path,'c--',2)
        self.h = h


    def build_euler_tour(self, h, start=0):
        """ build euler tour, using Hierholzer algorithm """
        n = start
        path = [n]
        unvis_edge_nodes = [n]
        while len(unvis_edge_nodes) > 0:
            #form subpath cycle, insert
            subpath = []
            #start at node n
            n = unvis_edge_nodes[-1]
            cn = n  # set current node
            uedges = self.unvisited_edges(h, cn)
            if len(uedges) == 0:
                unvis_edge_nodes.pop()
                continue
            e = uedges[0]
            next = e[1]
            h[cn][next][e[2]]["v"] = True
            while next != n:  #travel until n reached again
                cn = next
                edges = self.unvisited_edges(h, cn)
                if len(edges) > 1:
                    #add nodes with unvisited edges to list
                    unvis_edge_nodes.append(cn)
                    #print "node with unvisited edges:", cn, len(edges)
                e = edges[0]  # there has to be at least one
                next = e[1]
                h[cn][next][e[2]]["v"] = True  # mark edge as visited
                subpath.append(cn)
                #print edges
            # insert subpath at index i
            i = path.index(n)
            #print "  -- Insert circle at ", i, subpath
            path[i:i] = subpath
        tour = []
        for n in path:
            tour.append((start, n))
            start = n
        return tour

    def unvisited_edges(self,h,node):
        unvisited = []
        neighbors = h.neighbors(node)
        for n in neighbors:
            for edge, data in h[node][n].items():
                #print edge, data
                if not "v" in data:
                    unvisited.append((node, n, edge))
        return unvisited

    def find_hamilton_tour(self):
        """ Make the euler path Hamiltonian by skipping visited nodes (shortcutting)"""
        h = self.h
        self.g.add_weighted_edges_from(self.min_matching.edges(data=True))
        crossings = [1]
        visit = 1
        tour = self.euler_path
        print "start shortcutting"
        t1 = time.time()
        while visit <= 6:
            tour, crossings = self.shortcut_path(h, tour, visit)
            tour = self.unfuddle_crossings(crossings, tour, visit)
            visit = visit + 1
        #print tour
        t2 = time.time()
        print "took %s" % (t2-t1) 
        self.best_tour_len = self.calc_path_length(tour)
        print '#edges:', len(tour), "path len:", self.best_tour_len
        self.h_tour = tour
        #self.plot_edges(tour,'m-',5)


    def shortcut_path(self, h, path, visit):
        print "  --  start shortcutting visit ", visit
        h_tour = []
        self.h_tour = h_tour
        crossings = []
        i=0
        while i < len(path):
            e = path[i]
            next = e[1]
            n = self.g.node[next] # next node
            if n.has_key("v") and n['v'] == visit:
                this = e[0]
                print next, 'visited!', this#, self.g[next]
                # if node has deg>=4: its a crossing -> unfuddle it
                if h.degree(n) >= 4 and not self.has_sting(h,next) and visit<3:
                    v1, v2 = self.con_vis_neighbours(h_tour, next,this,visit)
                    print "its a crossing\n", "connected_visited_neighbors:", v1, v2
                    if v1 and v2:
                        if (next, v1) in h_tour:
                            e1 = (next, v1)
                            e1i = h_tour.index(e1)
                            e2 = (v2, next)
                            e2i = e1i - 1
                            h_tour.remove(e1)
                            h_tour.remove(e2)
                            h_tour.insert(e2i, (v2, v1) )
                        elif (v1, next) in h_tour:
                            e1 = (v1, next)
                            e1i = h_tour.index(e1)
                            e2 = (next, v2)
                            e2i = e1i + 1
                            h_tour.remove(e1)
                            h_tour.remove(e2)
                            h_tour.insert(e1i, (v1, v2) )
                        else:
                            print "------------ error: edge not in h_tour -------------"
                        h_tour.append(e)
                    else: #its a real crossing!
                        print "#its a real crossing!"
                        crossings.append(e)
                        h_tour.append(e)
                    i=i+1
                # else start shortcutting
                # look forward
                elif path[i+1][1] in self.g[this]:
                    jump = path[i+1][1]
                    h_tour.append((this, jump))
                    self.g.node[jump]["v"] = visit
                    i=i+2
                    print " looking forwards: ", this, jump, " cutting ", next
                # look backwards
                elif h_tour[len(h_tour)-1-1][0] in self.g[this] and visit<3:
                    start = h_tour[len(h_tour)-1-1][0]
                    h_tour.pop()
                    jump = h_tour.pop()[1]
                    h_tour.append((start, this))
                    h_tour.append(e)
                    i=i+1
                    print " looking backwards: ", start, this, " cutting ", jump

                else:
                    i=i+1
                    uber_next = path[i][1]
                    self.g.add_edge(this, uber_next)
                    h_tour.append(e)
                    print '----------- unhandled situation -----------'
            else:
                n["v"] = visit
                h_tour.append(e)
                #print self.g.node[e[1]]
                i=i+1
        #print h_tour, "crossings"
        print crossings
        print '#edges:', len(h_tour), "#crossings:", len(crossings)
        #self.plot_edges(h_tour,'m-',5)
        return h_tour, crossings

    def con_vis_neighbours(self, tour, n, exclude, visit):
        """ return two connected and visited neighbours """
        l = self.visited_neighbours(n, exclude, visit)
        #l = self.visited_neighbours(n, exclude)
        for i in range(0, len(l)-1):
            cn1 = l[i]
            for cn2 in l[i+1:]:
                if cn1 != cn2:
                    if cn1 in self.g[cn2]:
                        if (cn1,n) in tour or (n,cn1) in tour:
                            if (cn2,n) in tour or (n,cn2) in tour:
                                return cn1,cn2
        return None, None

    def visited_neighbours(self, n, exclude=None, visit=1):
        nl = self.g.neighbors(n)
        return [n for n in nl if self.g.node[n].has_key("v") and self.g.node[n]["v"] == visit and n != exclude]

    def unfuddle_crossings(self, crossings, tour, visit):
        for e in crossings:
            print "unfuddle", e
            cn = e[1] # center node
            start_n = e[0]
            #center = self.g[cn]
            neig = self.visited_neighbours(cn, visit=visit)
            try:
                ei = tour.index(e)  # if it's still present
            except Exception, e:
                continue
            prev = tour[ei-1][0]
            cand = [n for n in neig if n in self.g[start_n] and n != prev]
            print cn, start_n, prev, neig, cand
            if len(cand) < 1:
                print "EE - not enough candidates!"
            for ca in cand:
                if (ca, cn) in tour:
                    i = tour.index((ca, cn))
                    new = tour[:i]
                    new.append((ca,start_n))
                    new.extend(self.reverse_path(tour[i+1:ei]))
                    new.extend(tour[ei+1:])
                else:
                    print "EE - no cross resolving"
            tour = new if 'new' in locals() else tour

        return tour

    def reverse_path(self, path):
        new = []
        for e in reversed(path):
            new.append((e[1], e[0]))
        return new

    def has_sting(self, g, n):
        """ checks if node has a sting, eg. true for node 2 in 1,2,3,2,4  """
        node = g[n]
        for nn, edge in node.items():
            if len(edge) == 2:  # its a parallel edge
                if g.degree(nn) == 2:  # is leading nowehre else
                    return True
        return False

    def plot(self, labelNodes=False, showMST=False):
        for t in self.tri_points:
            # t[0], t[1], t[2] are the points indexes of the triangle
            t_i = [t[0], t[1], t[2], t[0]]
            plt.plot(self.x[t_i], self.y[t_i], 'b-',lw=0.5)
        if labelNodes:
            for city, city_id, cx, cy in zip(range(0,len(self.x)), self.city_ids, self.x, self.y):
                plt.annotate("%s"%(city), (cx, cy), xytext=(8,8), textcoords='offset points')
        if showMST:
            self.plot_edges(self.mst.edges(), 'g-', 2, 2)
        self.highlight_nodes(self.odd_deg_nodes)
        self.plot_edges(self.min_matching.edges(),'r-',2)  # min-weight-matching
        self.plot_edges(self.euler_path,'c--',2)

        if hasattr(self, "h_tour"):
            self.plot_path(self.h_tour)
        plt.plot(self.x, self.y, '.', ms=3)
        plt.axis('equal')
        #plt.show()

    def plot_edges(self, edges, fmt='r--', width=3, zorder=5):
        for e in edges:
            tup = [e[0], e[1]]
            plt.plot(self.x[tup],self.y[tup], fmt, lw=width, zorder=zorder)

    def plot_path(self, path, color="m"):
        for e in path:
            x0 = self.x[e[0]]
            x1 = self.x[e[1]]
            dx = x1 - x0
            y0 = self.y[e[0]]
            y1 = self.y[e[1]]
            dy = y1 - y0
            arr = plt.arrow(x0,y0,dx,dy, shape='full', lw=4, color=color,length_includes_head=True, head_width=140, head_length=160, overhang=0, zorder=10, alpha=0.8)

    def highlight_nodes(self, nodes, fmt='ro', ms=8):
        plt.plot(self.x[nodes], self.y[nodes], fmt, ms=ms)

        # for n in nodes:
        #     plt.plot(self.x[n], self.y[n], 'yo',ms=12)

