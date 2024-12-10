from itertools import batched, pairwise

class Node():
	def __init__(self, position, height):
		self.position = position
		self.height = int(height)

		self.next = set()

	def __str__(self):
		return f"{self.position[0]}, {self.position[1]} [{self.height}]"

	def __repr__(self):
		return f"{self.position[0]}, {self.position[1]} [{self.height}]"

def Parse(inputFile):
	nodes = {}

	with open(inputFile) as inFile:
		for y, line in enumerate(inFile.readlines()):
			for x, h in enumerate(line.strip()):
				if h == ".":
					continue

				node = Node(position = (x, y), height = h)
				assert node.position not in nodes

				nodes[node.position] = node

				if x > 0:
					left = nodes.get((x - 1, y))
					if left != None:
						# If either node is the next height up from the other, link them in ascending direction.
						if left.height == node.height + 1:
							node.next.add(left)
						elif node.height == left.height + 1:
							left.next.add(node)

				if y > 0:
					up = nodes.get((x, y - 1))
					if up != None:
						# If either node is the next height up from the other, link them in ascending direction.
						if up.height == node.height + 1:
							node.next.add(up)
						elif node.height == up.height + 1:
							up.next.add(node)

	return nodes

def EvaluateStartingPoint(startPoint):
	trailsConfirmed = 0

	stack = set([startPoint])
	encountered = set(stack)

	while any(stack):
		current = stack.pop()

		for nextPoint in current.next:
			if nextPoint in encountered:
				continue

			assert nextPoint not in stack

			if nextPoint.height == 9:
				trailsConfirmed += 1
			else:
				assert 0 <= nextPoint.height < 9, f"Unexpected height: {nextPoint.height}"
				stack.add(nextPoint)
			encountered.add(nextPoint)

	return trailsConfirmed

def Solve(inputFile, contiguous = True):
	pathNodes = Parse(inputFile)

	# First, use a list to build a stack - This way, we can avoid extensive recursion. 
	# We'll be going DFS over BFS so exhaust starting nodes quicker, so we'll treat it like a stack 
	# rather than a queue.
	startingPoints = [pn for pn in pathNodes.values() if pn.height == 0]

	return sum(EvaluateStartingPoint(start) for start in startingPoints)

if __name__ == "__main__":
	#assert Solve("Day10_ExampleA.txt") == 1
	#import sys
	#sys.exit()
	assert Solve("Day10_ExampleB.txt") == 2
	assert Solve("Day10_ExampleC.txt") == 4
	assert Solve("Day10_ExampleD.txt") == 3
	assert Solve("Day10_ExampleE.txt") == 36
	assert Solve("inputs/Day10_input.txt") == 611

	#assert Solve("Day9_Example.txt") == 2858
	#assert Solve("inputs/Day09_input.txt") == 6415666220005