from itertools import batched, pairwise

def Parse(inputFile):
	caret = 0

	with open(inputFile) as inFile:
		# As values go back & forth between a file and free space, we process them in pairs.
		# First is always the next file, second is the free space (if any) after it.  
		for id, circuit in enumerate(batched(inFile.read(), 2)):
			length = int(circuit[0])

			# Report on this file's stats, and increment the caret based on file size.  
			yield {
				"id": id,
				"position": caret,
				"size": length
			}
			caret += length

			# If there is a free space size declared, then increment the caret to accommodate. 
			# No further action is needed.  
			if len(circuit) > 1:
				caret += int(circuit[1])

def Solve(inputFile, contiguous = True):
	grid, size = Parse(inputFile)

	return 0

if __name__ == "__main__":
	assert Solve("Day10_ExampleA.txt") == 1928
	assert Solve("Day10_ExampleB.txt") == 1928
	assert Solve("Day10_ExampleC.txt") == 1928
	assert Solve("Day10_ExampleD.txt") == 1928
	assert Solve("Day10_ExampleE.txt") == 1928
	assert Solve("Day10_ExampleF.txt") == 1928
	print(Solve("inputs/Day10_input.txt"))

	#assert Solve("Day9_Example.txt") == 2858
	#assert Solve("inputs/Day09_input.txt") == 6415666220005