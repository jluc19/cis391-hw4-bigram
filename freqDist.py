import sys, copy, random

total = 0

def read(filename, bigram):
	global total
	total = 0
	inFile = open(filename, "r")
	data = inFile.readlines()
	wordDict = {}
	for line in data:
		line = line.strip()
		words = line.split(" ")
		first = None
		for word in words:
			word = word.lower()
			if bigram:
				if (first,word) in wordDict:
					val = wordDict[(first, word)]
					wordDict[(first,word)] = val+1
				else:
					wordDict[(first,word)] = 1
				first = word
			else:
				if word in wordDict:
					val = wordDict[word]
					wordDict[word] = val+1
				else:
					wordDict[word] = 1
			total = total + 1
			#print "Total: ", total
	#print wordDict
	return wordDict

class FreqDist(object):
	global total	
	def __init__(self, filename):
		self.total = 0
		self.wordDict = read(filename, False)
		self.total = total
	def count(self, word):
		word = word.lower()
		count = self.wordDict[word]
		return count
	def freq(self, word):
		#print(self.count(word)/float(self.total))
		if self.total <= 0:
			return 0
		else:
			return self.count(word)/float(self.total)

def generateUnigramSeq(fdist, length):
	ugram = []
	dict = fdist.wordDict
	keys = dict.keys()
	max = 0
	for key in keys:
		freq = fdist.freq(key)
		if freq > max:
			max = freq 
	print "Max: ", max
	while len(ugram) < length:
	#for x in range(0,length):
		i = random.uniform(0,max)
		for key in keys:
			#print "{0:.6f}".format(fdist.freq(key)), i
			if fdist.freq(key) > i:
				ugram.append(key)
				#print key
				keys.remove(key)
				break
		#print i
	print ugram

class BiFreqDist(object):
	global total	
	def __init__(self, filename):
		self.freqdist = FreqDist(filename)
		self.unigram = generateUnigramSeq(self.freqdist, 1)
		print "OLD: ", total
		self.dict = read(filename, True)
		print "INIT1: ", total
		self.total = total
		print "INIT: ",total, self.total
	def count(self, word1, word2):
		return  self.dict.get((word1,word2),0)
	def freq(self, word1, word2):
		if self.total <= 0:
			return 0
		else:
			#print "COUNT: ", self.dict.get((word1,word2),0)
			#print "TOTAL: ", float(self.total)
			return self.dict.get((word1,word2),0)/float(self.total)

class CondFreqDist(object):
	global total
	def __init__(self, filename):
		self.bdict = BiFreqDist("austen.token")
		self.udict = FreqDist("austen.token")
	def count(self, word1, word2):
		return bdict.dict.get((word1,word2),0)
	def freq(self, word1, word2):
		print (bdict.dict.get((word1,word2),0)/float(bdict.total))/(udict.wordDict.get(word1,0)/float(udict.total))
		return (bdict.dict.get((word1,word2),0)/float(bdict.total))/(udict.wordDict.get(word1,0)/float(udict.total))

def generateBigramSeq(cfdist, length, word):
	bigram = []
	return 0

if __name__ == '__main__':
	udict = FreqDist("austen.token")
	bdict = BiFreqDist("austen.token")
	cfdict = CondFreqDist("austen.token")
	outputs = ["she","Mr","herself","sister","lady","manner","cried","feelings","pride","great","family","home","character","letter","happiness","party","means","acquaintance","woman"]
	fo = open("austenCounts.txt","w")
	fo.write("Unigram")
	for uitem in outputs:
		fo.write('\n%s\n\t%s%d %s%f\n\n' % (uitem, "Count: ", udict.count(uitem), "Freq: ", udict.freq(uitem)))
	fo.write("Bigram")
	prev = "and"
	for bitem in outputs:
		fo.write('\n%s\n\t%s%d %s%f\n\n' % (prev+" "+bitem, "Count: ", bdict.count(prev, bitem), "Freq: ", bdict.freq(prev, bitem)))
	fo.close()
	generateUnigramSeq(udict, 20)
	generateBigramSeq(cfdict, 20,"and")
	fo = open("austenNGrams.txt","w")
	fo.write("Unigram")
	for cfitem in outputs:
		cfdict.freq("and", cfitem)
		fo.write('\n%s\n\t%s%d %s%f\n\n' % (prev+" "+cfitem, "Count: ", cfdict.count(prev, cfitem), "Freq: ", cfdict.freq(prev, cfitem)))
	fo.close()
