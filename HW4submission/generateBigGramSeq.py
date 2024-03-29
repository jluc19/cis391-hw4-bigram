from CondFreqDist import *
import random

def generateBigramSeq(cfdist, length, first):
	bigram = []
	keys = cfdist.bdict.dict.keys()
	bigram.append(first.lower())
	for a in xrange(1,length):
		r = random.random()
		while(len(bigram) == a):
			i = 0
			for (word1,word2) in keys:
				if word1 == bigram[a-1]:
					#print word1, bigram[a-1], bigram
					i = i + cfdist.freq(word1,word2)
					if i > r:
						bigram.append(word2)
						#keys.remove((word1,word2))
		 				break
	return bigram

if __name__ == '__main__':
	cfdist = CondFreqDist("austen.token")
	outputs = ["she","Mr","herself","sister","lady","manner","cried","feelings","pride","great","family","home","character","letter","happiness","party","means","acquaintance","woman"]
	
	#printing
	print "\n5. Bigram Sequences"
	for cfitem in outputs:
		print generateBigramSeq(cfdist, 10, cfitem)

	#write to file
	fo = open("hw4p5.txt","w")
	fo.write("5. Bigram Sequences")
	for cfitem in outputs:
		fo.write("\n%s\n" % generateBigramSeq(cfdist, 10, cfitem))
	fo.close()
