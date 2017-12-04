
import os

pf = 'real/'
i = 0
for filename in os.listdir(pf):
	      target = pf + str(i) + '_rd' + '.jpg'
	      source = pf +filename
	      os.rename(source, target)

	      i = i + 1
