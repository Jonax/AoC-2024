import os
from collections import Counter

def Parse(inputFile):
	with open(inputFile) as inFile:
		for line in inFile.readlines():
			yield [int(x) for x in line.strip().split(" ")]

def GetReportSafety(line):
	direction = line[1] - line[0]

	numDangers = 0
	lastGoodValue = line[0]
	for current in line[1:]:
		delta = current - lastGoodValue

		if delta == 0:
			numDangers += 1
			continue

		if direction * delta < 0:
			numDangers += 1
			continue

		if not (1 <= abs(delta) <= 3):
			numDangers += 1
			continue

		lastGoodValue = current

	return numDangers

def Solve(inputFile, maxTolerance):
	return sum(GetReportSafety(report) <= maxTolerance for report in Parse(inputFile))

assert Solve("Day2_Example.txt", 0) == 2
assert Solve("Day2_Input.txt", 0) == 483

assert Solve("Day2_Example.txt", 1) == 4
assert Solve("Day2_Input.txt", 1) == 528
