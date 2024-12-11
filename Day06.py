import pytest

def Parse(inputFile):
	obstacles = set()
	guard = None

	with open(inputFile) as inFile:
		grid = [line.strip() for line in inFile.readlines()]
		height = len(grid)
		width = len(grid[0])

		for y, line in enumerate(grid):
			for x, c in enumerate(line):
				if c == "#":
					obstacles.add((x, y))
				elif c == "^":
					assert guard is None
					guard = (x, y)

	return guard, (width, height), obstacles

def RunSimulation(size, startingPosition, obstacles):
	guard_position = startingPosition
	guard_direction = [0, -1]
	direction_idx = 0

	isLoop = False
	visited = {}
	while (0 <= guard_position[0] < size[0]) and (0 <= guard_position[1] < size[1]):
		directionFlag = 1 << direction_idx

		previousEncounter = visited.get(guard_position, 0)
		if (previousEncounter & directionFlag) == directionFlag:
			isLoop = True
			break

		visited.setdefault(guard_position, 0)
		visited[guard_position] |= directionFlag

		nextTile = tuple(n + i for n, i in zip(guard_position, guard_direction))

		if nextTile in obstacles:
			guard_direction = [
				guard_direction[1] * -1,
				guard_direction[0] * 1
			]
			direction_idx = (direction_idx + 1) % 4
		else:
			guard_position = nextTile

	return isLoop, set(visited.keys())

def Solve(inputFile, interfere = False):
	guard_position, size, obstacles = Parse(inputFile)

	# An extra obstacle would only have an effect on spots the guard would visit naturally.
	_, visited = RunSimulation(size, guard_position, obstacles)
	
	if not interfere:
		return len(visited)	

	visited.discard(guard_position)

	numMatches = 0
	for coord in visited:
		loop, _ = RunSimulation(size, guard_position, obstacles | set([coord]))
		if loop:
			numMatches += 1

	return numMatches

testCases = [
	("examples/Day06_Example.txt", 41),
	("inputs/Day06_input.txt", 5199)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_a(inputPath, expected):
	assert Solve(inputPath) == expected

testCases = [
	("examples/Day06_Example.txt", 6),
	("inputs/Day06_input.txt", 1915)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_b(inputPath, expected):
	assert Solve(inputPath, interfere = True) == expected

if __name__ == "__main__":
	pytest.main(["-v", __file__])
