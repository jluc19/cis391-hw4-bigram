total = 0

class BiFreqDist(object):
	global total	
	def __init__(self, filename):
		self.dict = read(filename, True)
		self.total = total
	def count(self, word1, word2):
		word1 = word1.lower()
		word2 = word2.lower()
		return  self.dict.get((word1,word2),0)
	def freq(self, word1, word2):
		word1 = word1.lower()
		word2 = word2.lower()
		if self.total <= 0:
			return 0
		else:
			return self.dict.get((word1,word2),0)/float(self.total)

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
	return wordDict

if __name__ == '__main__':
	bfd = BiFreqDist("austen.token")
	outputs = ["she","Mr","herself","sister","lady","manner","cried","feelings","pride","great","family","home","character","letter","happiness","party","means","acquaintance","woman"]
	#write to file
	fo = open("hw4p3.txt","w")
	fo.write("3. Bigram Probabilities")
	for bitem in outputs:
		fo.write('\n%s\n\t%s%d %s%f\n\n' % ("and "+bitem, "Count: ", bfd.count("and", bitem), "Freq: ", bfd.freq("and", bitem)))
	fo.close()

	#printing
	print "\n3. Bigram Probabilities"
	for bitem in outputs:
		print "and "+bitem, "Count: ", bfd.count("and",bitem), "Freq: ", bfd.freq("and", bitem)