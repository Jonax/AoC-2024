import operator
import pytest
from io import StringIO
from math import prod

def Parse(inputFile):
	with open(inputFile) as inFile:
		return [line.strip() for line in inFile.readlines()]

def FindPossibleDirections(x, y, w, h, strLength):
	left = x - strLength >= -1
	right = x + strLength <= w

	up = y - strLength >= -1
	down = y + strLength <= h

	if up:
		if left:
			yield (-1, -1)

		yield (0, -1)

		if right:
			yield (1, -1)

	if left:
		yield (-1, 0)

	if right:
		yield (1, 0)

	if down:
		if left:
			yield (-1, 1)

		yield (0, 1)

		if right:
			yield (1, 1)

def GetPhrase(grid, start, direction, numLetters):
	caret = start

	# Normalise direction to unit vector
	direction = tuple(d != 0 and int(d / abs(d)) or 0 for d in direction)

	with StringIO() as phrase:
		for _ in range(numLetters):
			phrase.write(grid[caret[1]][caret[0]])

			caret = tuple(map(operator.add, caret, direction))

		return phrase.getvalue()

def FindOccurances(grid, phrase):
	numSteps = len(phrase) - 1

	for y, line in enumerate(grid):
		for x, c in enumerate(line):
			if c != phrase[0]:
				continue

			for direction in FindPossibleDirections(x, y, len(grid[0]), len(grid), len(phrase)):
				if GetPhrase(grid, (x, y), direction, len(phrase)) == phrase:
					yield (x, y), (x + direction[0] * numSteps, y + direction[1] * numSteps)

def PartA(inputFile):
	# This way is used over len() to avoid having to resolve the entire iterator in one go.
	return sum(1 for _ in FindOccurances(Parse(inputFile), "XMAS"))

def PartB(inputFile):
	grid = Parse(inputFile)

	# Forwards & backwards
	phrases = ["MAS", "MAS"[::-1]]

	numMatches = 0
	for start, end in FindOccurances(grid, "MAS"):
		direction = tuple(map(operator.sub, end, start))
		if prod(direction) <= 0:
			continue

		xStart = (start[0], end[1])
		xDirection = (direction[0], -direction[1])

		result = GetPhrase(grid, xStart, xDirection, len(phrases[0])) 
		numMatches += result in phrases

	return numMatches

def test_part_a():
	assert PartA("Day4_ExampleA.txt") == 4
	assert PartA("Day4_ExampleB.txt") == 18

	assert PartA("inputs/Day04_input.txt") == 2571

def test_part_b():
	assert PartB("Day4_ExampleB.txt") == 9

	assert PartB("inputs/Day04_input.txt") == 1992

if __name__ == "__main__":
	pytest.main(["-v", __file__])
