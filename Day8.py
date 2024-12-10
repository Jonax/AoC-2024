from itertools import combinations

def Parse(inputFile):
	frequencies = {}
	guard = None

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

assert Solve("Day8_ExampleA.txt", limited = True) == 14
assert Solve("inputs/Day08_input.txt", limited = True) == 214

assert Solve("Day8_ExampleB.txt") == 9
assert Solve("Day8_ExampleA.txt") == 34
assert Solve("inputs/Day08_input.txt") == 80
