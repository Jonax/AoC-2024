import pytest
import re
from collections import Counter
from math import prod

'''
APPROACH:
	Parse the input into a series of robots, each represented by an x-y for position and an x-y for 
	velocity. 

	Part 1:
		Simulate 100 seconds in one go by multiplying the velocity and adding to position (this is 
		possible since the robots are following a constant velocity).  
		Use modulus to wrap the positions around. 
		Once simulates, disregard any robot on a midpoint line, and split the rest into quadrants based
		on x-y position.
		Find the product of the number of robots in each quadrant to get the answer.  

	Part 2:
		This one is trickier as it's more visual than most. However, we can exploit an observation - 
		As the robots need to be synchronised for this to work, that timeframe is expected to have
		no overlapping robots. 
		So: Find the first timeframe where the number of unique robot positions matches the number of
		robots, and pray 
		(Spoiler: It worked)
'''

def Parse(inputFile):
	robotRegex = re.compile(r"p=(?P<px>\d+),(?P<py>\d+) v=(?P<vx>-*\d+),(?P<vy>-*\d+)")

	with open(inputFile) as inFile:
		for match in robotRegex.finditer(inFile.read()):
			yield {k:int(v) for k,v in match.groupdict().items()}

def SimulateMovement(gridSize, robots, seconds = 1):
	# As the robots move in constant, unchanging velocity, we can simply multiple & apply velocity.
	# Robots will likely go over the edge - As we're meant to loop them round in those cases, we can
	# use modulus to handle in one go. 
	for robot in robots:
		robot["px"] = (robot["px"] + robot["vx"] * seconds) % gridSize[0]
		robot["py"] = (robot["py"] + robot["vy"] * seconds) % gridSize[1]

def PartA(inputFile, gridSize):
	robots = list(Parse(inputFile))
	
	# Simulate for 100 turns.
	SimulateMovement(gridSize, robots, 100)

	# Safety check: Make sure the width & height are both odd-numbered.
	assert all(s % 2 for s in gridSize)

	# Get the center point in the grid.  
	center = tuple(gs // 2 for gs in gridSize)

	quadrants = Counter()
	for robot in robots:
		# If a robot is in line with the center point in either axis, disregard it.  
		if robot["px"] == center[0] or robot["py"] == center[1]:
			continue

		# Determine which quadrant a robot is present in by determining which side of
		# the center point it's on.  
		# As it's a 2x2 layout, we can get away with using booleans for keys in this case.
		# Those on the midpoint lines won't spoil the result since they were filtered out above.
		quadrants[(
			robot["px"] > center[0], 
			robot["py"] > center[1]
		)] += 1

	# Pull the number of robots in each quadrant, and return the product of them all.  
	return prod(quadrants.values())

def PartB(inputFile, gridSize):
	robots = list(Parse(inputFile))

	i = 0

	unique = False
	while not unique:
		# Simulate movement for one second.  
		SimulateMovement(gridSize, robots)
		i += 1

		# Pull each robot's positions post-move and turn them into a set. 
		# The set will automatically filter out any duplicate positions.  
		uniquePositions = set((r["px"], r["py"]) for r in robots)

		# Only if the number of unique positions matches the number of robots are all robots in a 
		# unique location. Ergo, bail out.  
		unique = len(uniquePositions) == len(robots)

	# Return whatever i ended up as for the answer.  
	return i

testCases = [
	("examples/Day14_Example.txt", (11, 7), 12),
	("inputs/Day14_input.txt", (101, 103), 216027840)
]
@pytest.mark.parametrize(	"inputPath, gridSize, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_a(inputPath, gridSize, expected):
	assert PartA(inputPath, gridSize) == expected

testCases = [
	("inputs/Day14_input.txt", (101, 103), 6876)
]
@pytest.mark.parametrize(	"inputPath, gridSize, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_b(inputPath, gridSize, expected):
	assert PartB(inputPath, gridSize) == expected

if __name__ == "__main__":
	pytest.main(["-v", __file__])
