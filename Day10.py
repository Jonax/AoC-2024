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
				assert 0 <= nextPoint["height"] < 9, f"Unexpected height: {nextPoint["height"]}"
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

if __name__ == "__main__":
	assert Solve("Day10_ExampleA.txt") == 1
	assert Solve("Day10_ExampleB.txt") == 2
	assert Solve("Day10_ExampleC.txt") == 4
	assert Solve("Day10_ExampleD.txt") == 3
	assert Solve("Day10_ExampleE.txt") == 36
	assert Solve("inputs/Day10_input.txt") == 611

	assert Solve("Day10_ExampleF.txt", countDistinctRoutes = True) == 3
	assert Solve("Day10_ExampleG.txt", countDistinctRoutes = True) == 13
	assert Solve("Day10_ExampleH.txt", countDistinctRoutes = True) == 227
	assert Solve("Day10_ExampleE.txt", countDistinctRoutes = True) == 81
	assert Solve("inputs/Day10_input.txt", countDistinctRoutes = True) == 1380