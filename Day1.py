import re
from collections import Counter

'''
APPROACH:
	Parse the input into two columns of files.

	For Part 1:
		Sort both lines in ascending order. 
		Find the absolute distance between each sorted row. 
		Sum up all the differences.

	For Part 2:
		Count number of instances of each unique number on right.
		For each number on left, multipy value by number of its occurance on right.
		Sum up all the results.
'''

def Parse(inputFile):
	inputRegex = re.compile(r"(\d+)\s+(\d+)")

	with open(inputFile) as inFile:
		for line in inputRegex.findall(inFile.read()):
			assert len(line) == 2
			yield tuple(int(x) for x in line)

def Solve(inputFile, combine = False):
	lines = list(Parse(inputFile))

	left = [x[0] for x in lines]
	if not combine:
		# Part 1
		left.sort()
		right = sorted(x[1] for x in lines)

		return sum(abs(a - b) for a,b in zip(left, right))

	# Part 2
	right = Counter(x[1] for x in lines)

	return sum([a * right[a] for a in left])

assert Solve("Day1_Example.txt") == 11
assert Solve("Day1_Input.txt") == 1941353

assert Solve("Day1_Example.txt", combine = True) == 31
assert Solve("Day1_Input.txt", combine = True) == 22539317
