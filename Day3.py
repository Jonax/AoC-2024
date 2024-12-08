import os
import re
from collections import Counter

def Parse(inputFile):
	with open(inputFile) as inFile:
		return inFile.read().strip()

def Solve(inputFile, toggle = False):
	op_regex = re.compile(r"mul\((?P<a>\d{1,3}),(?P<b>\d{1,3})\)|don't\(\)|do\(\)")

	active = True
	result = 0
	for match in op_regex.finditer(Parse(inputFile)):
		# Strangely easier to determine which operation by partitioning the match, than to handle in 
		# the regex level (especially as brackets can be different).
		op = match.group(0).rpartition("(")[0]
		if op == "don't":
			if toggle == True:
				active = False
		elif op == "do":
			active = True
		else:
			assert op == "mul"
			if not active:
				continue

			result += int(match.group("a")) * int(match.group("b"))

	return result

assert Solve("Day3_ExampleA.txt") == 161
assert Solve("Day3_Input.txt") == 187825547

assert Solve("Day3_ExampleB.txt", toggle = True) == 48
print(Solve("Day3_Input.txt", toggle = True))
