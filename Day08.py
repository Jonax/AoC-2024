import pytest
from itertools import combinations

def Parse(inputFile):
	frequencies = {}

	with open(inputFile) as inFile:
		grid = [line.strip() for line in inFile.readlines()]
		height = len(grid)
		width = len(grid[0])

		for y, line in enumerate(grid):
			for x, c in enumerate(line):
				if c == ".":
					continue

				frequencies.setdefault(c, set())
				frequencies[c].add((x, y))

	return (width, height), frequencies

def IsPointWithinGrid(point, gridSize):
	return all(0 <= pi < si for pi, si in zip(point, gridSize))

def FindPointsOnLine(start, end, gridSize, n = None):
	delta = tuple(e - s for s, e in zip(start, end))

	if any(n or []):
		# If we know the specific points to return via n, just return 
		# them after checking they fit in the grid. 
		for i in n:
			point = tuple(s + (d * i) for s, d in zip(start, delta))
			if IsPointWithinGrid(point, gridSize):
				yield point
	else:
		# Otherwise - Start from the first point and move backwards
		# until it goes off the grid...
		i = 0
		while True:
			point = tuple(s + (d * i) for s, d in zip(start, delta))
			if not IsPointWithinGrid(point, gridSize):
				break

			yield point
			i -= 1

		# Then start at the other point and repeat for the opposite
		# direction.
		i = 1
		while True:
			point = tuple(s + (d * i) for s, d in zip(start, delta))
			if not IsPointWithinGrid(point, gridSize):
				break

			yield point
			i += 1

def Solve(inputFile, limited = False):
	size, frequencies = Parse(inputFile)

	allAntinodes = set()
	for freqID, antennae in frequencies.items():
		for combo in combinations(antennae, 2):
			allAntinodes.update(FindPointsOnLine(*combo, size, n = limited and [-1, 2] or None))

	return len(allAntinodes)

testCases = [
	("examples/Day08_ExampleA.txt", 14),
	("inputs/Day08_input.txt", 214)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_a(inputPath, expected):
	assert Solve(inputPath, limited = True) == expected

testCases = [
	("examples/Day08_ExampleB.txt", 9),
	("examples/Day08_ExampleA.txt", 34),
	("inputs/Day08_input.txt", 809)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_b(inputPath, expected):
	assert Solve(inputPath) == expected

if __name__ == "__main__":
	pytest.main(["-v", __file__])
