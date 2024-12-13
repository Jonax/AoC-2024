import pytest
import re

'''
APPROACH:
	This can be solved with brute force, but would likely take way too long. Instead,
	this problem is essentially solving simultaneous equations. 

	Parse the input into individual games.  
	For each game:
		Solve as a system of linear equations (via Cramer's rule) to get a & b (the 
		number of times each button has to be pressed).
		Filter out those with non-integer a or b (these have no solution).
		Calculate the score for the game based on the spec.
	Sum up all valid games' scores to get the resulting answer. 

	For Part 1:
		Straight up as above.  

	For Part 2:
		A "handicap" of 1e13 is applied to each axis of each game's target coordinates.
		Increment c & d each by it and proceed as normal.
'''

def Parse(inputFile):
	# This is a longer regex, but it does mean that the code has everything it 
	# needs in one go. 
	# The only touchup required is casting number strings to integers.
	gameRegex = re.compile(r"Button A: X(?P<ax>[-+]\d+), Y(?P<ay>[-+]\d+)\nButton B: X(?P<bx>[-+]\d+), Y(?P<by>[-+]\d+)\nPrize: X=(?P<c>\d+), Y=(?P<d>\d+)")

	with open(inputFile) as inFile:
		for match in gameRegex.finditer(inFile.read()):
			yield {k:int(v) for k,v in match.groupdict().items()}

def SolveGame(game, handicap):
	c = game["c"] + handicap
	d = game["d"] + handicap

	# First, find the system's determinant.  
	determinant = (game["ax"] * game["by"] - game["ay"] * game["bx"])

	# Then use it to solve for a & b.
	a = (game["by"] * c - game["bx"] * d) / determinant
	b = (game["ax"] * d - game["ay"] * c) / determinant

	# If a solution doesn't have both a & b as integers, then it isn't a clean 
	# solution. Consequently, the game has *no* clean solutions. 
	# Instead, we return zero to remain inert in the later sum.
	if a % 1 != 0 or b % 1 != 0:
		return 0

	# Spec details that it wants 3a + b for each game.  
	return (3 * int(a)) + int(b)

def Solve(inputFile, handicap = 0):
	return sum(SolveGame(game, handicap) for game in Parse(inputFile))

testCases = [
	("examples/Day13_Example.txt", 480),
	("inputs/Day13_input.txt", 35255)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_a(inputPath, expected):
	assert Solve(inputPath) == expected

testCases = [
	("examples/Day13_Example.txt", 875318608908),
	("inputs/Day13_input.txt", 87582154060429)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_b(inputPath, expected):
	assert Solve(inputPath, handicap = 10000000000000) == expected

if __name__ == "__main__":
	pytest.main(["-v", __file__])
