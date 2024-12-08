import os
from collections import Counter

def Parse(inputFile):
	a, b = [], []

	with open(inputFile) as inFile:
		for line in inFile.readlines():
			line = line.strip().partition("   ")
			
			a.append(int(line[0]))
			b.append(int(line[-1]))

	return a, b

def PartA(inputFile):
	left, right = Parse(inputFile)

	left.sort()
	right.sort()

	return sum(abs(l - r) for l,r in zip(left, right))

def PartB(inputFile):
	left, right = Parse(inputFile)

	right = Counter(right)

	return sum([l * right[l] for l in left])

assert PartA("Day1_Example.txt") == 11
assert PartA("Day1_Input.txt") == 1941353

assert PartB("Day1_Example.txt") == 31
print(PartB("Day1_Input.txt"))