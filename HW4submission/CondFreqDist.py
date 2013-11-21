from FreqDist import *
from BiFreqDist import *

class CondFreqDist(object):
	global total
	def __init__(self, filename):
		self.bdict = BiFreqDist("austen.token")
		self.udict = FreqDist("austen.token")
	def count(self, word1, word2):
		if word1 is not None:
			word1 = word1.lower()
		if word2 is not None:
			word2 = word2.lower()
		return self.bdict.dict.get((word1,word2),0)
	def freq(self, word1, word2):
		if word1 is not None:
			word1 = word1.lower()
		if word2 is not None:
			word2 = word2.lower()
		if(self.bdict.total == 0 or self.udict.dict.get(word1,0) == 0 or self.udict.total == 0):
			return 0
		else:
			bifreq = self.count(word1,word2)/float(self.bdict.total)
			ufreq = self.udict.dict.get(word1,0)/float(self.udict.total)
			return bifreq/ufreq

if __name__ == '__main__':
	cfdist = CondFreqDist("austen.token")
	outputs = ["she","Mr","herself","sister","lady","manner","cried","feelings","pride","great","family","home","character","letter","happiness","party","means","acquaintance","woman"]
	
	#write to file
	fo = open("hw4p4.txt","w")
	fo.write("4. Conditional Probabilities")
	for cfitem in outputs:
		fo.write('\n%s\n\t%s%d %s%f\n\n' % ("and "+cfitem, "Count: ", cfdist.count("and", cfitem), "Freq: ", cfdist.freq("and", cfitem)))
	fo.write("\nb) While the counts in problem 4 are identical to the counts in problem 1, the probability freq is clearly different. We are looking at am implementation of Kolmogorov's formula, namely P(a,b) = P(a|b)*P(b). CF.freq is P(a|b) while FD.freq is P(b) and BiFd.freq = P(a,b). To find the conditional probability, we divide BiFd/Fd, following the formula. Clearly, 1 and 4 will have different freqs because the words, especially in the English language, are not independent.\n")
	fo.close()

	#printing
	print "\n4. Conditional Probabilities"
	for cfitem in outputs:
		print "and "+cfitem, "Count: ", cfdist.count("and",cfitem), "Freq: ", cfdist.freq("and", cfitem)