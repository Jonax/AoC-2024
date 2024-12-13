import pytest
from math import log10
from collections import Counter

'''
APPROACH:
	This is a Game of Rice problem: While straightforward enough for low-blink scenarios, it quickly
	explodes in memory & time taken as number of blinks increase IF stones were handled individually. 
	Luckily, despite the extensive spec there's no effect in keeping the stones in order (position means
	nothing) - So we can batch them up based on a stone's value instead.  

	Parse the input into a counter/dict which holds a stone value against how many stones have that value.
	For a blink:
		Create a fresh dictionary/Counter.
		For each group of identical stones:
			* If value is 0: New value is 1.
			* Otherwise: Find how many digits the number has using the log10 trick. 
			  	* If odd digits: New value is old value multiplied by 2024.
			  	* If even digits: Determine the "split mark" with 10 to the power of half the number of digits.
			  	  The quotient & remainder from divmod() will suffice for the two bisected values.  
		  	With the new value known for the key, add the quantity of stones to the new dict.  
 	Once pass is done and all stones are processed, make the new dict the source of truth for the stones, and
 	reuse as the input for the next blink.
 	Repeat for the specified number of blinks.
 	Sum up the quantity of all stone groups to get the final number of stones present.

 	For Part 1:
 		Calculate for 25 blinks.

	For Part 2:
		Calculate for 75 blinks.
		The problem here comes from the exponential growth of stones in each blink.
		Handling each stone individually will end up taking too much time, akin to the Game of Rice.
'''

def Parse(inputFile):
	with open(inputFile) as inFile:
		return [int(n) for n in inFile.read().strip().split(" ")]

def Blink(stones):
	# A dict can work here as well, but using a Counter lets us skip certain explicit behaviour 
	# (e.g. checking if a key exists before append to it).
	updated = Counter()

	for id, count in stones.items():
		if id == 0:
			updated[1] += count
		else:
			# Number of digits used to represent x can be easily found with the equation
			# `x = floor(log10(x)) + 1`. Integer casting is used in place of math.floor() to avoid 
			# pulling in another library. 
			numDigits = int(log10(id))

			# As the equation above will normally return 0 for even-digit numbers, we can simply
			# skip the increment-by-one by inverting the two cases.  
			if numDigits % 2:
				splitMark = 10 ** int((numDigits + 1) / 2)
				a, b = divmod(id, splitMark)

				# Since we're splitting each stone into two, add the original amount to both stacks.
				updated[a] += count
				updated[b] += count
			else:
				updated[id * 2024] += count

	# We generate a fresh registry each time as in-place updating runs the risk of updates within 
	# a blink bleeding into each other (e.g. the same "stones" being processed more than once for 
	# different values).  
	return updated

def Solve(inputFile, numBlinks):
	stones = Counter(Parse(inputFile))

	for i in range(numBlinks):
		stones = Blink(stones)

	# We don't care what values each stone has, just how many there are. 
	return sum(stones.values())

testCases = [
	("examples/Day11_ExampleA.txt", 1, 7),
	("examples/Day11_ExampleB.txt", 6, 22),
	("inputs/Day11_input.txt", 25, 187738)
]
@pytest.mark.parametrize(	"inputPath, numBlinks, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_a(inputPath, numBlinks, expected):
	assert Solve(inputPath, numBlinks) == expected

testCases = [
	("inputs/Day11_input.txt", 75, 223767210249237)
]
@pytest.mark.parametrize(	"inputPath, numBlinks, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_b(inputPath, numBlinks, expected):
	assert Solve(inputPath, numBlinks) == expected

if __name__ == "__main__":
	pytest.main(["-v", __file__])
