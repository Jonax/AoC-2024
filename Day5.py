import operator
import os
import re
from io import StringIO
from math import prod
from functools import cmp_to_key

def Parse(inputFile):
	with open(inputFile) as inFile:
		dependencies, _, updates = inFile.read().partition("\n\n")

		dependencies = [d.partition("|") for d in dependencies.split("\n")]
		dependencies = set((int(a), int(b)) for a, _, b in dependencies)

		updates = [u for u in updates.split("\n")]
		updates = [[int(u2) for u2 in u.split(",")] for u in updates]

		return dependencies, updates

def EvaluateUpdate(line, groupings):
	groups = [groupings.get(p) for p in line]
	if groups != sorted(groups):
		return 0

	assert len(line) % 2 == 1

	return line[int(len(line) / 2)]

def Solve(inputFile, fixIncorrects = False):
	dependencies, updates = Parse(inputFile)

	result = 0
	for update in updates:
		corrected = sorted(update, key = cmp_to_key(lambda a, b: (a, b) in dependencies and -1 or 1))

		if (update == corrected) ^ fixIncorrects:
			result += corrected[int(len(corrected) / 2)]

	return result

assert Solve("Day5_Example.txt") == 143
assert Solve("inputs/Day05_input.txt") == 4774

assert Solve("Day5_Example.txt", fixIncorrects = True) == 123
assert Solve("inputs/Day05_input.txt", fixIncorrects = True) == 6004
