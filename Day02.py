import pytest

'''
APPROACH:
	Parse the input into lines of integer sequences.  
	Evaluate each report's safety by the number of "errors" in the sequence.
	An error is determined as when the current value and the last "good" value 
	don't follow the rules 

	For Part 1:
		Any errors at all in a report means the report can be disregarded.
		Therefore, only count those where numErrors = 0

	For Part 2:
		One error is tolerable, as long as the following value works with the 
		last good value.
		Therefore, only count those where numErrors = 0 or 1.
'''

def Parse(inputFile):
	with open(inputFile) as inFile:
		for line in inFile.readlines():
			yield [int(x) for x in line.strip().split(" ")]

# Rate a report's "safety" based on the number of errors found.
def GetReportSafety(line):
	# Identify which direction the report is expected to be going using
	# the first two values.
	# If any deltas along the same sequence go in the opposite direction, 
	# that suggests a switched direction somewhere and therefore an error.
	direction = line[1] - line[0]

	# Error counter
	numErrors = 0

	# Tracks the last value that passed, for comparing later values against.
	# Starts as the first value in the list, since there's nothing before it to
	# contradict.
	lastValidValue = line[0]

	# Start at the second value so we can start comparing against the 
	# first value. 
	for current in line[1:]:
		# Find the delta from last valid to current.
		delta = current - lastValidValue

		# If the delta's zero, the two numbers match which should not happen.
		if delta == 0:
			numErrors += 1
			continue

		# If multiplying delta by the original direction results in a 
		# negative number, the delta's going in the opposite direction
		# (similar to using dot product). Ergo, an error.  
		if direction * delta < 0:
			numErrors += 1
			continue

		# Finally, if the absolute delta is not between 1 & 3, then it's
		# out of range and therefore an error.  
		if not (1 <= abs(delta) <= 3):
			numErrors += 1
			continue

		# If reaching this point, the value was good so make it the 
		# next "good" value.  
		lastValidValue = current

	# In the end, return however many errors were encountered.  
	return numErrors

def Solve(inputFile, maxTolerance = 0):
	# Return the number of reports that had at most the number of 
	# errors deemed acceptable.  
	return sum(GetReportSafety(report) <= maxTolerance for report in Parse(inputFile))

testCases = [
	("examples/Day02_Example.txt", 2),
	("inputs/Day02_input.txt", 483)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_a(inputPath, expected):
	assert Solve(inputPath) == expected

testCases = [
	("examples/Day02_Example.txt", 4),
	("inputs/Day02_input.txt", 528)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_b(inputPath, expected):
	assert Solve(inputPath, maxTolerance = 1) == expected

if __name__ == "__main__":
	pytest.main(["-v", __file__])
