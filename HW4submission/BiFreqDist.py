total = 0

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

if __name__ == '__main__':
	bfd = BiFreqDist("austen.token")
	outputs = ["she","Mr","herself","sister","lady","manner","cried","feelings","pride","great","family","home","character","letter","happiness","party","means","acquaintance","woman"]
	#write to file
	fo = open("hw4p3.txt","w")
	fo.write("Counts include bigrams that wrap between lines of text")
	fo.write("3. Bigram Probabilities")
	for bitem in outputs:
		fo.write('\n%s\n\t%s%d %s%f\n\n' % ("and "+bitem, "Count: ", bfd.count("and", bitem), "Freq: ", bfd.freq("and", bitem)))
	fo.close()

	#printing
	print "\n3. Bigram Probabilities"
	for bitem in outputs:
		print "and "+bitem, "Count: ", bfd.count("and",bitem), "Freq: ", bfd.freq("and", bitem)