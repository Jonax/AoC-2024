import pytest
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
	disk = list(Parse(inputFile))
	disk.sort(key = lambda f: f["position"])

	# Because of the scale of the input data, a registry of free blocks is required. 
	# This is calculated as the spaces between elements once the data is sorted.  
	freeBlocks = []
	for a, b in pairwise(disk):
		freeStart = a["position"] + a["size"]

		freeBlocks.append({
			"position": freeStart,
			"size": b["position"] - freeStart
		})

	# sorted() is used here over reversed() etc so that it intentionally makes a copy of the initial
	# file list. This means the original list can be modified without causing enumeration issues.  
	for target in sorted(disk, key = lambda f: f["position"], reverse = True):
		desiredSize = contiguous and target["size"] or 1

		# While we still need to find space for the target (mainly for non-contiguous mode)...
		while target["size"] > 0:
			# Find the next available block that's big enough for the target to move into.  
			availableBlock = next((b for b in freeBlocks if b["size"] >= desiredSize), None)

			# If no block could be found, or the block is after the target, then there's no 
			# valid block to move into. Go to the next target.  
			if availableBlock is None or availableBlock["position"] >= target["position"]:
				break

			# Figure out how much data can be transferred in one go.  
			# For contiguous mode, it's the size of the target.
			# For non-contiguous mode, it's however much we can get away with.  
			availableSize = target["size"]
			if not contiguous:
				# Fit into whatever memory is available
				availableSize = min(availableBlock["size"], availableSize)

			# Add a new entry to the disk for the block being written to.  
			# It's done like this to allow splitting up of files (for non-contiguous).
			disk.append({
				"id": target["id"],
				"position": availableBlock["position"],
				"size": availableSize
			})

			# Decrement the target size by the amount that was transferred.  
			# If the resulting size is zero, then just remove the file from the disk.  
			target["size"] -= availableSize
			if target["size"] == 0:
				disk.remove(target)

			# Shrink the block used by the transferred amount.  
			# If the amount filled up the whole block, then remove it from the list of free blocks.
			if availableBlock["size"] > availableSize:
				availableBlock["position"] += availableSize
				availableBlock["size"] -= availableSize
			else:
				freeBlocks.remove(availableBlock)

	# Process the checksum.
	checksum = 0
	for file in disk:
		for x in range(file["position"], file["position"] + file["size"]):
			checksum += file["id"] * x

	return checksum

def test_part_a():
	assert Solve("Day9_Example.txt", contiguous = False) == 1928

	assert Solve("inputs/Day09_input.txt", contiguous = False) == 6398252054886

def test_part_b():
	assert Solve("Day9_Example.txt") == 2858

	assert Solve("inputs/Day09_input.txt") == 6415666220005

if __name__ == "__main__":
	pytest.main(["-v", __file__])
