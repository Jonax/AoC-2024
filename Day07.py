import pytest
from itertools import product

def Parse(inputFile):
	with open(inputFile) as inFile:
		for line in inFile.readlines():
			key, _, values = line.strip().partition(": ")

			yield int(key), [int(v) for v in values.split(" ")]

def Evaluate(values, targetValue, concatenate):
	operators = "+*"
	if concatenate:
		operators += "|"

	for equation in product(operators, repeat = len(values) - 1):
		result = values[0]

		for operation, nextValue in zip(equation, values[1:]):
			if operation == "+":
				result += nextValue
			elif operation == "*":
				result *= nextValue
			elif operation == "|":
				result = int(f"{result}{nextValue}")
			else:
				raise Exception("Unexpected")
		
		if result == targetValue:
			return True

	return False

def Solve(inputFile, concatenate = False):
	return sum(key for key, values in Parse(inputFile) if Evaluate(values, key, concatenate))

testCases = [
	("examples/Day07_ExampleA.txt", 3749),
	("inputs/Day07_input.txt", 2501605301465)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_a(inputPath, expected):
	assert Solve(inputPath) == expected

testCases = [
	("examples/Day07_ExampleB.txt", 11387),
	("inputs/Day07_input.txt", 44841372855953)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_b(inputPath, expected):
	assert Solve(inputPath, concatenate = True) == expected

if __name__ == "__main__":
	pytest.main(["-v", __file__])
