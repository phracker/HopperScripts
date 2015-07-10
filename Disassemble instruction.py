doc = Document.getCurrentDocument()

seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()

doc.log("-----------")
doc.log("Disassemble instruction at " + hex(adr))

instr = seg.getInstructionAtAddress(adr)

doc.log("Architecture: %s" % Instruction.stringForArchitecture(instr.getArchitecture()))
doc.log("instruction: " + instr.getInstructionString())
doc.log("instruction length: %d" % instr.getInstructionLength())

argCount = instr.getArgumentCount()
if argCount > 0:
	plural = "s"
	if argCount == 1:
		plural = ""
	doc.log("%d argument%s" % (argCount, plural))
	doc.log("Raw arguments")
	for idx in range(instr.getArgumentCount()):
		doc.log(("	  %d: " % idx) + " " + instr.getRawArgument(idx))
	doc.log("Formatted arguments")
	for idx in range(instr.getArgumentCount()):
		doc.log(("	  %d: " % idx) + " " + instr.getFormattedArgument(idx))

if instr.isAConditionalJump():
	doc.log("conditional jump")
if instr.isAnInconditionalJump():
	doc.log("inconditional jump")
