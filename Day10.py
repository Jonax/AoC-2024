import pytest

def Parse(inputFile):
	nodes = {}

	with open(inputFile) as inFile:
		for y, line in enumerate(inFile.readlines()):
			for x, h in enumerate(line.strip()):
				if h == ".":
					continue

				node = {
					"position": (x, y),
					"height": int(h),
					"next": []
				}

				assert node["position"] not in nodes
				nodes[node["position"]] = node

				if x > 0:
					left = nodes.get((x - 1, y))
					if left is not None:
						# If either node is the next height up from the other, link them in ascending direction.
						if left["height"] == node["height"] + 1:
							node["next"].append(left)
						elif node["height"] == left["height"] + 1:
							left["next"].append(node)

				if y > 0:
					up = nodes.get((x, y - 1))
					if up is not None:
						# If either node is the next height up from the other, link them in ascending direction.
						if up["height"] == node["height"] + 1:
							node["next"].append(up)
						elif node["height"] == up["height"] + 1:
							up["next"].append(node)

	return nodes

def ExploreTrailhead(startPoint, distinct):
	# We go with BFS since we don't need to return the paths we find, just the number that *have*
	# been found.
	completed = []
	
	stack = [ startPoint ]
	while any(stack):
		node = stack.pop()

		for nextPoint in node["next"]:
			if nextPoint["height"] == 9:
				completed.append(nextPoint["position"])
			else:
				assert 0 <= nextPoint["height"] < 9
				stack.append(nextPoint)

	# We could've potentially do the distinct check during the trail following...but as the graph is 
	# fairly shallow and we don't need to store the full routes, it doesn't really save much in the 
	# grand scale of things. 
	return len(distinct and completed or set(completed))

def Solve(inputFile, countDistinctRoutes = False):
	pathNodes = Parse(inputFile)

	# First, use a list to build a stack - This way, we can avoid extensive recursion. 
	# We'll be going DFS over BFS so exhaust starting nodes quicker, so we'll treat it like a stack 
	# rather than a queue.
	startingPoints = [pn for pn in pathNodes.values() if pn["height"] == 0]

	return sum(ExploreTrailhead(start, countDistinctRoutes) for start in startingPoints)

testCases = [
	("examples/Day10_ExampleA.txt", 1),
	("examples/Day10_ExampleB.txt", 2),
	("examples/Day10_ExampleC.txt", 4),
	("examples/Day10_ExampleD.txt", 3),
	("examples/Day10_ExampleE.txt", 36),
	("inputs/Day10_input.txt", 611)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_a(inputPath, expected):
	assert Solve(inputPath) == expected

testCases = [
	("examples/Day10_ExampleF.txt", 3),
	("examples/Day10_ExampleG.txt", 13),
	("examples/Day10_ExampleH.txt", 227),
	("examples/Day10_ExampleE.txt", 81),
	("inputs/Day10_input.txt", 1380)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_b(inputPath, expected):
	assert Solve(inputPath, countDistinctRoutes = True) == expected

if __name__ == "__main__":
	pytest.main(["-v", __file__])
