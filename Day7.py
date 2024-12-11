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

if __name__ == "__main__":
	assert Solve("Day7_ExampleA.txt") == 3749
	assert Solve("inputs/Day07_input.txt") == 2501605301465

	assert Solve("Day7_ExampleB.txt", concatenate = True) == 11387
	assert Solve("inputs/Day07_input.txt", concatenate = True) == 44841372855953
