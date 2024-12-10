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

def ExploreTrailhead(startPoint):
	# We go with DFS over BFS to exhaust whole areas earlier rather than keep them around. 
	# Ergo, a stack rather than a queue.  
	stack = [ [startPoint] ]

	while any(stack):
		route = stack.pop()
		currentPosition = route[-1]

		for nextPoint in currentPosition["next"]:
			nextRoute = route + [nextPoint]

			if nextPoint["height"] == 9:
				# Once a complete route has been found, yield it back to caller.  
				yield nextRoute
			else:
				assert 0 <= nextPoint["height"] < 9, f"Unexpected height: {nextPoint["height"]}"
				stack.append(nextRoute)

def Solve(inputFile, countDistinctRoutes = False):
	pathNodes = Parse(inputFile)

	# First, use a list to build a stack - This way, we can avoid extensive recursion. 
	# We'll be going DFS over BFS so exhaust starting nodes quicker, so we'll treat it like a stack 
	# rather than a queue.
	startingPoints = [pn for pn in pathNodes.values() if pn["height"] == 0]

	# Determine how trailheads are scored based on the mode used.
	scoringFunc = countDistinctRoutes \
					and len \
					or (lambda routes: len(set(r[-1]["position"] for r in routes)))

	return sum(scoringFunc(list(ExploreTrailhead(start))) for start in startingPoints)

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