#!/usr/bin/python
import sys
import json
from contextlib import closing
from random import randint

MODE_TRAIN = "train"
MODE_GENERATE = "generate"
MODE_HELP = "help"

DEFAULT_MINIMUM = 3
DEFAULT_MAXIMUM = 32
DEFAULT_COUNT = 1
DEFAULT_SEGMENT_LENGTH = 2
LINE_ENDINGS = ['\n']
NEW_WORD = 'EOW'

LOADED_TRAINING = None

def help():
	return """Usages:

python darmok.py %s <input file> <output file> [<segment length>]

	Builds up a data model using the input file and writes it as JSON to the output file.

	The segment length defines how many letters will be used to determine what letter comes next.
	Smaller numbers are better for smaller sets. Default is 2. Greater than 3 is not recommended.

	Example: darmok.py %s names.txt names.json

python darmok.py %s <input file> [<minimum length> [<maximum length> [<count>]]]

	Using the data model represented in the input file to generate one or more names.
	The names will be a minimum of %d characters long, unless another is specified.
	The names will be a maximum of %d characters long, unless another is specified.
	By default %d will be generated, unless count is specified.

	Example: darmok.py %s names.json 2 12 5

python darmok.py %s

	Shows this message.""" % (MODE_TRAIN, MODE_TRAIN, MODE_GENERATE, DEFAULT_MINIMUM, DEFAULT_MAXIMUM, DEFAULT_COUNT, MODE_GENERATE, MODE_HELP)

def train(infile, outfile, segmentLength = 2):
	matrix = {}

	for line in open(infile, 'r'):
		line = line.strip()

		previousLetters = []
		for i in range(segmentLength):
			previousLetters.append(NEW_WORD)

		aline = []
		for char in line:
			aline.append(char)
		aline.append(NEW_WORD)
		for char in aline:
			iterMatrix = matrix
			for i in range(segmentLength):
				if previousLetters[i] not in iterMatrix:
					iterMatrix[previousLetters[i]] = {}
				iterMatrix = iterMatrix[previousLetters[i]]
			if char not in iterMatrix:
				iterMatrix[char] = 1
			else:
				iterMatrix[char] += 1

			previousLetters.append(char)
			while len(previousLetters) > segmentLength:
				previousLetters = previousLetters[1:]

	out = open(outfile, 'w')
	json.dump({"segmentLength": segmentLength, "data": matrix}, out)
	out.close()

def generate(infile, maxLength):
	global LOADED_TRAINING
	if LOADED_TRAINING is None:
		LOADED_TRAINING = json.load(open(infile, 'r'))
	training = LOADED_TRAINING
	segmentLength = training["segmentLength"]
	matrix = training["data"]
	ret = ""
	previousLetters = []
	for i in range(segmentLength):
		previousLetters.append(NEW_WORD)
	for i in range(0, maxLength):
		iterMatrix = matrix
		for j in range(segmentLength):
			iterMatrix = iterMatrix[previousLetters[j]]
		csum = 0
		for char in iterMatrix:
			csum += iterMatrix[char]
		chosenSpot = randint(0, csum)
		res = None
		isum = 0
		for char in iterMatrix:
			isum += iterMatrix[char]
			if isum >= chosenSpot:
				res = char
				break
		if res == NEW_WORD:
			break
		ret += res
		previousLetters.append(char)
		while len(previousLetters) > segmentLength:
			previousLetters = previousLetters[1:]
	return ret

if __name__ == "__main__":
	mode = sys.argv[1]
	if mode == MODE_TRAIN:
		infile = sys.argv[2]
		outfile = sys.argv[3]
		segmentLength = int(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_SEGMENT_LENGTH
		train(infile, outfile, segmentLength)
	elif mode == MODE_GENERATE:
		infile = sys.argv[2]
		minLength = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_MINIMUM
		maxLength = int(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_MAXIMUM
		count = int(sys.argv[5]) if len(sys.argv) > 5 else DEFAULT_COUNT
		for c in range(count):
			w = ""
			while len(w) < minLength:
				w = generate(infile, maxLength)
			print w
	else:
		print help()
