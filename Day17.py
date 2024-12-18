import pytest
import re

'''
	APPROACH:
		The problem describes a LOLCODE machine in sufficient detail, mentioning what each opcode 
		should do when encountered.

		Parse the input into a program consisting of initial values for three registers (A, B, C) and
		a series of 3-bit "instructions" (0-7).
		Place a caret at the start of the instructions.
		For each step, parse the number the caret is pointing to as its opcode, and the following 
		number as its literal operand.  
			- Actions to take wholly depend on the opcode value, and are too complex to detail here. 
			- Depending on the opcode, the literal operand may be used directly, or may need to be used
			  to derive the combo operand for use instead.  
			- The caret will normally increment by two after each step, but if a JNZ operation then 
			  special logic will override this.  
			- Reduced to their simplest, almost all of the operations are bitwise operations. 
		Repeat until the program reaches the end of its instructions. 
		In the process, a series of 3-bit values should be built up as output.  

		For Part 1:
			The program is run once. 
			Parse the program, run it and collect its output.
			Return output as a comma-delimited string.  

		For Part 2:
			Parse the program and store as a template. 
			Set n = 0.
			Start from the end of the instructions. 
			For each instruction (in reverse):
				- Derive a reference list from the instruction to the end.
				- Bit-shift n three bits to the left.
				- While incrementing n:
					- Calculate the resulting program for n.
					- Once the program matches the reference, stop and continue for the next instruction.
				- Don't reset n between instructions.
			Once all instructions have been processed, n should be the lowest n required for recreating 
			the original program string.
'''

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
	# Uses the literal operand to determine the value of the combo operand, as required by some
	# operations.  

	# [0-3] Use operand as the literal value.  
	if 0 <= operand <= 3:
		return operand

	# [7] Unused, so this should never trigger.
	assert operand <= 6

	# [4-6] Use the value of the respective register.
	# 4 = A, 5 = B, 6 = C
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
			# Yielding rather than adding to a local list gives us more power on how to use the result
			# (namely, short-circuiting a program we know won't be what we want. 
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
		# Observed when running the test & input cases manually is that the length of the resulting 
		# program increases in length for every base-8 OOM. We can use this quirk to skip up huge 
		# swathes of values of n by bit-shifting n three bits to the left each time the result matches
		# the end of the reference program.  
		# We do it at the start of the loop because doing it at the end would cause one more bit-shift 
		# than needed and provide a wrong answer. Instead, 0 will be bit-shifted to 0 at the start, 
		# having no adverse effect.  
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
