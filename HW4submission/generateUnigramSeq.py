import random
from FreqDist import *

def generateUnigramSeq(fdist, length):
	ugram = []
	keys = fdist.dict.keys()
	max = 0
	while len(ugram) < length:
		r = random.random()
		i = 0
		for key in keys:
			i = i + fdist.freq(key)
			if i > r:
				ugram.append(key)
				#keys.remove(key)
				break
	return ugram

if __name__ == '__main__':
	fd = FreqDist("austen.token")
	outputs = ["she","Mr","herself","sister","lady","manner","cried","feelings","pride","great","family","home","character","letter","happiness","party","means","acquaintance","woman"]
	
	#write to file
	fo = open("hw4p2.txt","w")
	fo.write("2. Unigram Sequences")
	fo.write("\n%s\n" % generateUnigramSeq(fd, 20))
	fo.close()

	#printing
	print "\n2. Unigram Sequences"
	print "UGRAM: ", generateUnigramSeq(fd,20)
