from itertools import pairwise

def Parse(inputFile, contiguous):
	from itertools import batched

	caret = 0
	with open(inputFile) as inFile:
		for id, circuit in enumerate(batched(inFile.read(), 2)):
			n, l = 1, int(circuit[0])
			if not contiguous:
				n, l = l, n

			for _ in range(n):
				yield {
					"id": id,
					"position": caret,
					"size": l
				}
				caret += l

			if len(circuit) > 1:
				caret += int(circuit[1])

def Defrag(disk):
	freeBlocks = []
	for a, b in pairwise(disk):
		freeStart = a["position"] + a["size"]

		freeBlocks.append({
			"position": freeStart,
			"size": b["position"] - freeStart
		})

	for target in sorted(disk, key = lambda f: f["position"], reverse = True):
		availableBlock = next(b for b in freeBlocks if b["size"] >= target["size"])
		assert availableBlock["size"] > 0

		if availableBlock["position"] > target["position"]:
			continue

		# We could keep track of the newly-freed up regions as well.
		# However, because only right-to-left moves are valid here, 
		# there's not much point - They won't be considered in the 
		# first place.
		target["position"] = availableBlock["position"]
		if target["size"] > availableBlock["size"]:
			availableBlock["position"] += target["size"]
			availableBlock["size"] -= target["size"]
		else:
			freeBlocks.remove(availableBlock)

	disk.sort(key = lambda f: f["position"])

def RepDisk(disk):
	disk.sort(key = lambda f: f["position"])

	diskMap = ["_"] * (disk[-1]["position"] + disk[-1]["size"])

	for file in disk:
		for x in range(file["position"], file["position"] + file["size"]):
			diskMap[x] = str(file["id"])

	return "".join(diskMap)

def Solve(inputFile, contiguous = True):
	disk = list(Parse(inputFile, contiguous))
	Defrag(disk)

	checksum = 0
	for file in disk:
		for x in range(file["position"], file["position"] + file["size"]):
			checksum += file["id"] * x

	return checksum

#assert Solve("Day9_Example.txt", contiguous = False) == 1928
assert Solve("inputs/Day09_input.txt", contiguous = False) == 6398252054886

#assert Solve("Day9_Example.txt") == 2858
#print("A")
#assert Solve("inputs/Day09_input.txt") == 80