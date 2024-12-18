import pytest
import re
from itertools import batched

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
	if registers == None:
		registers = payload["registers"]

	output = []

	caret = 0
	jump = None
	while caret < len(payload["program"]):
		jump = 2

		opcode, operand = payload["program"][caret:caret + 2]

		#print(f"OPERATION: {opcode} ({operand}) {registers}")

		if opcode == 0:	# adv (combo)
			#print(f"\t{opcode} (ADV): {registers[0]} // 2 ** {GetComboOperand(registers, operand)}")
			registers[0] = registers[0] >> GetComboOperand(registers, operand)
		elif opcode == 1: # bxl (literal)
			#print(f"\t{opcode} (BXL): {registers[1]} ^ {operand}")
			registers[1] = registers[1] ^ operand
		elif opcode == 2: # bst (combo)
			#print(f"\t{opcode} (BST): {GetComboOperand(registers, operand)} % 8")
			registers[1] = GetComboOperand(registers, operand) % 8
		elif opcode == 3: # jnz (literal)
			if registers[0] != 0:
				old, caret = caret, operand
				#print(f"\t{opcode} (JNZ): {registers[0]} {old}-->{caret}")
				if caret != old:
					jump = 0
			else:
				pass #print(f"\t{opcode} (JNZ): {registers[0]}")
		elif opcode == 4: # bxc (unused)
			#print(f"\t{opcode} (BXR): {registers[1]} ^ {registers[2]}")
			registers[1] = registers[1] ^ registers[2]
		elif opcode == 5: # out (combo)
			#print(f"\t{opcode} (OUT): Output: {GetComboOperand(registers, operand) % 8}")
			output.append(GetComboOperand(registers, operand) % 8)
		elif opcode == 6: # bdv (combo)
			#print(f"\t{opcode} (BDV): {registers[0]} // 2 ** {GetComboOperand(registers, operand)}")
			registers[1] = registers[0] >> GetComboOperand(registers, operand)
		elif opcode == 7: # cdv (combo)
			#print(f"\t{opcode} (CDV): {registers[0]} // 2 ** {GetComboOperand(registers, operand)}")
			registers[2] = registers[0] >> GetComboOperand(registers, operand)

		caret += jump

	return output

def PartA(inputFile):
	payload = Parse(inputFile)

	return ",".join([str(n) for n in GenerateProgram(payload)]) 

def PartB(inputFile):
	payload = Parse(inputFile)

	n = 0
	for i in range(len(payload["program"]), 0, -1):
		n = n << 3

		reference = payload["program"][i - 1:]

		while True:
			result = GenerateProgram(payload, [n, payload["registers"][1], payload["registers"][2]])

			if result == reference:
				break

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
