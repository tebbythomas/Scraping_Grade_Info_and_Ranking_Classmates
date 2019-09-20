import os
from cgpa_ranks import computeCGPA

count = 1
while (os.stat("csis_Ranks_CGPA.txt").st_size == 0):
	print "Iteration Number = %d" % (count)
   	computeCGPA()
   	count = count + 1

