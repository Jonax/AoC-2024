import pytest
import re

def Parse(inputFile):
	programRegex = re.compile(r"Register A: (?P<a>\d+)\nRegister B: (?P<b>\d+)\nRegister C: (?P<c>\d+)\n\nProgram: (?P<prog>[\d,]+)")

	with open(inputFile) as inFile:
		match = programRegex.search(inFile.read())

		return {
			"registers": [
				int(match.group("a")), 
				int(match.group("b")), 
				int(match.group("c"))
			],

			"program": [int(x) for x in match.group("prog").split(",")]
		}

def GetComboOperand(registers, operand):
	if 0 <= operand <= 3:
		return operand

	assert operand <= 6
	return registers[operand - 4]

def GenerateProgram(payload, registers = None):
	# Optional override for the benefit of Part 2. By default (for Part 1), the program will use the 
	# registered as parsed in the payload. If specified (for Part 2), the list being provided is used
	# separately. This means that a payload can be reused repeatedly without a prior program run
	# bleeding its state into later runs.  
	if registers == None:
		registers = payload["registers"]

	caret = 0
	while caret < len(payload["program"]):
		jump = 2

		opcode, operand = payload["program"][caret:caret + 2]

		# Consult the problem specification for a detailed description of what to do for each opcode.
		# Instead, we've condensed them down to their simplest forms.  
		if opcode == 0:	# adv (combo)
			registers[0] >>= GetComboOperand(registers, operand)
		elif opcode == 1: # bxl (literal)
			registers[1] ^= operand
		elif opcode == 2: # bst (combo)
			registers[1] = GetComboOperand(registers, operand) % 8
		elif opcode == 3: # jnz (literal)
			if registers[0] != 0:
				# Taking advantage of Python's ability to swap variables in one go. 
				# This may not necessarily work in other languages.  
				old, caret = caret, operand
				if caret != old:
					jump = 0
		elif opcode == 4: # bxc (unused)
			registers[1] ^= registers[2]
		elif opcode == 5: # out (combo)
			yield GetComboOperand(registers, operand) % 8
		elif opcode == 6: # bdv (combo)
			registers[1] = registers[0] >> GetComboOperand(registers, operand)
		elif opcode == 7: # cdv (combo)
			registers[2] = registers[0] >> GetComboOperand(registers, operand)

		caret += jump

def PartA(inputFile):
	return ",".join([str(n) for n in GenerateProgram(Parse(inputFile))]) 

def PartB(inputFile):
	payload = Parse(inputFile)

	n = 0
	for i in range(len(payload["program"]), 0, -1):
		n <<= 3

		reference = payload["program"][i - 1:]
		# We could return the calculated program as a full list and compare, but this is a much nicer
		# trick to make it faster.  
		# GenerateProgram() acts as a generator and spouts out each value as it's calculated. 
		# Consequently, as soon as it hits a value that doesn't match the reference, it can bail out 
		# much earlier and move to the next attempt instead of calculating the rest. 
		while any(a != b for a, b in zip(
			GenerateProgram(payload, [n, *payload["registers"][1:]]), 
			reference
		)):
			n += 1

	return n

testCases = [
	("examples/Day17_ExampleA.txt", "4,6,3,5,6,3,5,2,1,0"),
	("inputs/Day17_input.txt", "6,0,6,3,0,2,3,1,6")
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_a(inputPath, expected):
	assert PartA(inputPath) == expected

testCases = [
	("examples/Day17_ExampleB.txt", 117440),
	("inputs/Day17_input.txt", 236539226447469)
]
@pytest.mark.parametrize(	"inputPath, expected", testCases, 
							ids = [t[0].split("_")[-1].split(".")[0] for t in testCases])
def test_part_b(inputPath, expected):
	assert PartB(inputPath) == expected

if __name__ == "__main__":
	pytest.main(["-v", __file__])
