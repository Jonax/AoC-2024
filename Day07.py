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

def test_part_a():
	assert Solve("examples/Day07_ExampleA.txt") == 3749

	assert Solve("inputs/Day07_input.txt") == 2501605301465

def test_part_b():
	assert Solve("examples/Day07_ExampleB.txt", concatenate = True) == 11387

	assert Solve("inputs/Day07_input.txt", concatenate = True) == 44841372855953

if __name__ == "__main__":
	pytest.main(["-v", __file__])
