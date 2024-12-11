import pytest
import re
from math import prod

'''
APPROACH:
	Parse the input as a raw set of text-based data.  
	Search for all instances of `mul(a, b)`, `do()` and `don't()`.
	As a precaution, only count `mul`s featuring 1-3 digit numbers.
	Multiple the numbers in each `mul` call and sum up the multiplcations.  

	For Part 1:
		`do` and `don't` have no effect here.
		Just count all the `mul`s and process.  

	For Part 2:
		`do` and `don't` will switch on/off whether to include subsequent
		`mul`s. The flag starts at enabled. 
		Only count the `mul`s when the flag is enabled. 
'''

def Parse(inputFile):
	# Send the input back raw: It's needed in this case.
	with open(inputFile) as inFile:
		return inFile.read().strip()

def Solve(inputFile, toggle = False):
	# Regex to capture relevant operators from raw data.
	opRegex = re.compile(r"(mul|do|don't)\((?:(\d{1,3}),(\d{1,3})){0,1}\)")

	result = 0		# Running total for final result.

	active = True	# Flag to determine whether to cuunt a `mul`.
	for match in opRegex.finditer(Parse(inputFile)):
		# `mul`s will have two values, `do` and `don't` none.
		op, *values = match.groups()

		if op == "don't":
			# Stop counting `mul`s, but ONLY is in Part 2.
			if toggle:
				active = False
		elif op == "do":
			# Count `do`s regardless: This will have zero effect in Part 1.
			active = True
		else:
			# Sanity check: Make sure the operation is a `mul`, in case it's
			# no longer the only remaining operator.  
			assert op == "mul"

			# If not currently ignoring, add the product to the running total.  
			if active:
				result += prod(int(x) for x in values)

	# Return running total
	return result

testCases = [
	("examples/Day03_ExampleA.txt", 161),
	("inputs/Day03_input.txt", 187825547)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_a(inputPath, expected):
	assert Solve(inputPath) == expected

testCases = [
	("examples/Day03_ExampleB.txt", 48),
	("inputs/Day03_input.txt", 85508223)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_b(inputPath, expected):
	assert Solve(inputPath, toggle = True) == expected

if __name__ == "__main__":
	pytest.main(["-v", __file__])
