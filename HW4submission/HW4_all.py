import random

total = 0

#___________________________________________________________
# Classes

class FreqDist(object):
	global total	
	def __init__(self, filename):
		self.total = 0
		self.dict = read(filename, False)
		self.total = total
	def count(self, word):
		if word is not None:
			word = word.lower()
		return self.dict.get(word,0)
	def freq(self, word):
		if self.total <= 0:
			return 0
		else:
			return self.count(word)/float(self.total)

class BiFreqDist(object):
	global total	
	def __init__(self, filename):
		self.dict = read(filename, True)
		self.total = total
	def count(self, word1, word2):
		if word1 is not None:
			word1 = word1.lower()
		if word2 is not None:
			word2 = word2.lower()
		return  self.dict.get((word1,word2),0)
	def freq(self, word1, word2):
		if self.total <= 0:
			return 0
		else:
			return self.count(word1,word2)/float(self.total)

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

#___________________________________________________________
# CORE FUNCTIONALITY: UNIGRAMS AND BIGRAMS

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

#___________________________________________________________
# IO READ FUNCTION

def read(filename, bigram):
	#setup
	global total
	total = 0
	words = []
	wordDict = {}
	first = None
	inFile = open(filename, "r")
	data = inFile.readlines()
	#create list of words
	for line in data:
		array  = line.strip().split(" ")
		array = [a for a in array if len(a) > 0]
		words.extend(array)
	#iterate through word list
	for word in words:
		word = word.lower()
		# creating bigrams and unigram dicts
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
	if bigram:
		wordDict[(words[-1], None)] = 1
	return wordDict

#___________________________________________________________
# MAIN METHOD

if __name__ == '__main__':
	cfdist = CondFreqDist("austen.token")
	outputs = ["she","Mr","herself","sister","lady","manner","cried","feelings","pride","great","family","home","character","letter","happiness","party","means","acquaintance","woman"]
	generateUnigramSeq(cfdist.udict, 20)
	fo = open("austenCounts.txt","w")
	print "\n1b. FreqDist of Words"
	fo.write("1b. FreqDist of Words")
	for uitem in outputs:
		print uitem, "Count: ", cfdist.udict.count(uitem), "Freq: ", cfdist.udict.freq(uitem)
		fo.write('\n%s\n\t%s%d %s%f\n\n' % (uitem, "Count: ", cfdist.udict.count(uitem), "Freq: ", cfdist.udict.freq(uitem)))
	print "\n3. Bigram Probabilities"
	fo.write("3. Bigram Probabilities")
	prev = "and"
	for bitem in outputs:
		print prev+" "+bitem, "Count: ", cfdist.bdict.count(prev,bitem), "Freq: ", cfdist.bdict.freq("and", bitem)
		fo.write('\n%s\n\t%s%d %s%f\n\n' % (prev+" "+bitem, "Count: ", cfdist.bdict.count(prev, bitem), "Freq: ", cfdist.bdict.freq(prev, bitem)))
	print "\n4. Conditional Probabilities"
	fo.write("4. Conditional Probabilities")
	for cfitem in outputs:
		print prev+" "+cfitem, "Count: ", cfdist.count(prev,cfitem), "Freq: ", cfdist.freq("and", cfitem)
		fo.write('\n%s\n\t%s%d %s%f\n\n' % (prev+" "+cfitem, "Count: ", cfdist.count(prev, cfitem), "Freq: ", cfdist.freq(prev, cfitem)))
	fo.close()
	fo = open("austenNGrams.txt","w")
	print "\n2. Unigram Sequences"
	fo.write("2. Unigram Sequences")
	print "UGRAM: ", generateUnigramSeq(cfdist.udict,20)
	fo.write("\n%s\n" % generateUnigramSeq(cfdist.udict, 20))
	print "\n5. Bigram Sequences"
	fo.write("5. Bigram Sequences")
	for cfitem in outputs:
		print "BIGRAMS: ", generateBigramSeq(cfdist,10,cfitem)
		fo.write("\n%s\n" % generateBigramSeq(cfdist, 10, cfitem))
	fo.close()
