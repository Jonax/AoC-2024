import pytest
from math import log10
from collections import Counter

def Parse(inputFile):
	with open(inputFile) as inFile:
		return [int(n) for n in inFile.read().strip().split(" ")]

def Blink(stones):
	updated = Counter()

	for id, count in stones.items():
		if id == 0:
			updated[1] += count
		else:
			numDigits = int(log10(id))

			if numDigits % 2:
				splitMark = 10 ** int((numDigits + 1) / 2)
				a, b = divmod(id, splitMark)

				updated[a] += count
				updated[b] += count
			else:
				updated[id * 2024] += count

	return updated

def Solve(inputFile, numBlinks):
	stones = Counter(Parse(inputFile))

	for i in range(numBlinks):
		stones = Blink(stones)

	return sum(stones.values())

testCases = [
	("examples/Day11_ExampleA.txt", 1, 7),
	("examples/Day11_ExampleB.txt", 6, 22),
	("inputs/Day11_input.txt", 25, 187738)
]
@pytest.mark.parametrize(	"inputPath, numBlinks, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_a(inputPath, numBlinks, expected):
	assert Solve(inputPath, numBlinks) == expected

testCases = [
	("inputs/Day11_input.txt", 75, 223767210249237)
]
@pytest.mark.parametrize(	"inputPath, numBlinks, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_b(inputPath, numBlinks, expected):
	assert Solve(inputPath, numBlinks) == expected

if __name__ == "__main__":
	pytest.main(["-v", __file__])
