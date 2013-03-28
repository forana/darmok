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
LINE_ENDINGS = ['\n']
NEW_WORD = 'EOW'

def help():
	return """Usages:

darmok.py %s <input file> <output file>

	Builds up a data model using the input file and writes it as JSON to the output file.

	Example: darmok.py %s names.txt names.json

darmok.py %s <input file> [<minimum length> [<maximum length> [<count>]]]

	Using the data model represented in the input file to generate one or more names.
	The names will be a minimum of %d characters long, unless another is specified.
	The names will be a maximum of %d characters long, unless another is specified.
	By default %d will be generated, unless count is specified.

	Example: darmok.py %s names.json 2 12 5

darmok.py %s

	Shows this message.""" % (MODE_TRAIN, MODE_TRAIN, MODE_GENERATE, DEFAULT_MINIMUM, DEFAULT_MAXIMUM, DEFAULT_COUNT, MODE_GENERATE, MODE_HELP)

def train(infile, outfile):
	matrix = {}

	def addCount(cur, next):
		if cur not in matrix:
			matrix[cur] = {}
		if next not in matrix[cur]:
			matrix[cur][next] = 0
		else:
			matrix[cur][next] += 1

	curLetter = NEW_WORD
	for char in open(infile, 'r').read():
		if char in LINE_ENDINGS:
			char = NEW_WORD
		addCount(curLetter, char)
		curLetter = char

	out = open(outfile, 'w')
	json.dump(matrix, out)
	out.close()

def generate(infile, maxLength):
	matrix = json.load(open(infile, 'r'))
	ret = ""
	curLetter = NEW_WORD
	for i in range(0, maxLength):
		curDict = matrix[curLetter]
		csum = 0
		for char in curDict:
			csum += curDict[char]
		chosenSpot = randint(0, csum)
		res = None
		isum = 0
		for char in curDict:
			isum += curDict[char]
			if isum >= chosenSpot:
				res = char
				break
		if res == NEW_WORD:
			break
		ret += res
		curLetter = res
	return ret

if __name__ == "__main__":
	mode = sys.argv[1]
	if mode == MODE_TRAIN:
		infile = sys.argv[2]
		outfile = sys.argv[3]
		train(infile, outfile)
	elif mode == MODE_GENERATE:
		infile = sys.argv[2]
		minLength = int(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_MINIUM
		maxLength = int(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_MAXIMUM
		count = int(sys.argv[5]) if len(sys.argv) > 5 else DEFAULT_COUNT
		for c in range(count):
			w = ""
			while len(w) < minLength:
				w = generate(infile, maxLength)
			print w
	else:
		print help()
