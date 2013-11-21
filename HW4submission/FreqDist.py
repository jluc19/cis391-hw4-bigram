total = 0

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
	fd = FreqDist("austen.token")
	outputs = ["she","Mr","herself","sister","lady","manner","cried","feelings","pride","great","family","home","character","letter","happiness","party","means","acquaintance","woman"]
	
	#write to file
	fo = open("hw4p1.txt","w")
	fo.write("1b. FreqDist of Words")
	for uitem in outputs:
		fo.write('\n%s\n\t%s%d %s%f\n\n' % (uitem, "Count: ", fd.count(uitem), "Freq: ", fd.freq(uitem)))
	fo.close()

	#printing
	print "\n1b. FreqDist of Words"
	for uitem in outputs:
		print uitem, "Count: ", fd.count(uitem), "Freq: ", fd.freq(uitem)
