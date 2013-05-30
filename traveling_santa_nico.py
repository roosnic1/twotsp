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
## Diese Datei beinhaltet das NJM Objekt zur Findung eines NJM Pfad.                    ##
##                                                                                      ##
##                                                                                      ##
##                                                                                      ##
##                                                                                      ##
##########################################################################################
##########################################################################################

class NICO(object):

	def __init__(self,route):
		self.route0 = route
		self.route1 = []

	def solve(self):
		counter = 0
		inx = 0
		pt0 = self.route0[inx][0]

		# Einen alternativen Pfad zu route0 finden
		# Partitionierung mit genau 5 Kanten 
		while inx < len(self.route0)-3 and inx != len(self.route0)-5:
			# 3 Kanten nach vorne
			inx += 3
			pt1 = self.route0[inx][0]
			self.route1.append( (pt0,pt1) )
			pt0 = pt1

			# Neustart der Partitionierung 
			if counter < 2:
				counter += 1
				# 2 Kanten zurueck
				inx -= 2
				pt1 = self.route0[inx][0]
				self.route1.append( (pt0,pt1) )
				pt0 = pt1
			else:
				counter = 0

		# Loesen der letzen verbleibenden Punkte
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

		return self.route1
