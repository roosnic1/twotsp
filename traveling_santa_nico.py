class NICO(object):

	def __init__(self,route):
		self.route0 = route
		self.route1 = []

	def solve(self):
		counter = 0
		inx = 0
		pt0 = self.route0[inx][0]

		while inx < len(self.route0)-3 and inx != len(self.route0)-5:

			inx += 3
			pt1 = self.route0[inx][0]
			self.route1.append( (pt0,pt1) )

			pt0 = pt1

			if counter < 2:
				print counter
				counter += 1
				inx -= 2
				pt1 = self.route0[inx][0]
				self.route1.append( (pt0,pt1) )
				pt0 = pt1
			else:
				counter = 0

			#print('-----------')
			#print self.route1

		#print inx
		#print len(self.route0)
		if inx == len(self.route0)-5:
			inx += 4
			pt1 = self.route0[inx][0]
			self.route1.append( (pt0,pt1) )
			pt0 = pt1

			inx -= 3
			pt1 = self.route0[inx][0]
			self.route1.append( (pt0,pt1) )
			pt0 = pt1

			inx += 2
			pt1 = self.route0[inx][0]
			self.route1.append( (pt0,pt1) )
			pt0 = pt1

			inx = 0
			pt1 = self.route0[inx][0]
			self.route1.append( (pt0,pt1) )
			pt0 = pt1

		elif len(self.route0) % 2 == 1 and inx != len(self.route0)-1:
			inx += 1
			pt1 = self.route0[inx][0]
			self.route1.append( (pt0,pt1) )
			pt0 = pt1

			inx += 1
			pt1 = self.route0[inx][1]
			self.route1.append( (pt0,pt1) )
		else:
			inx = -1
			pt1 = self.route0[inx][1]
			self.route1.append( (pt0,pt1) )


		print self.route1
		return self.route1
