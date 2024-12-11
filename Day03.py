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

def test_part_a():
	assert Solve("examples/Day03_ExampleA.txt") == 161

	assert Solve("inputs/Day03_input.txt") == 187825547

def test_part_b():
	assert Solve("examples/Day03_ExampleB.txt", toggle = True) == 48

	assert Solve("inputs/Day03_input.txt", toggle = True) == 85508223

if __name__ == "__main__":
	pytest.main(["-v", __file__])
