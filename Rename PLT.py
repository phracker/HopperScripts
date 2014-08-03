doc = Document.getCurrentDocument()

doc.log("# PLT funtion rename v1.0")
doc.log("# Author: @pwntester")

segment = doc.getCurrentSegment()
lower = segment.getStartingAddress()
upper = segment.getStartingAddress() + segment.getLength()

plt_address = 0

doc.log("Lower: {0}".format(hex(lower)))
doc.log("Upper: {0}".format(hex(upper)))
for i in xrange(upper-lower):
	comment = segment.getCommentAtAddress(lower + i)
	if comment is not None:
		doc.log(comment)
		if "Section .plt" in comment:
			plt_address = lower + i
			doc.log("PLT at: {0}".format(hex(plt_address))) 
			break

if plt_address > 0:
	doc.log("Renaming in range %s to %s" % (hex(plt_address), hex(upper)))

	adr = plt_address
	while adr <= upper:
		name = segment.getNameAtAddress(adr)
		if name is not None:
			ins = segment.getInstructionAtAddress(adr)
			op = ins.getInstructionString()
			arg = ins.getFormattedArgument(0)
			if op == "jmp" and "sub_" in name and "@GOT" in arg:
				new_name = arg[:arg.index('@GOT')]
				if new_name != None:
					doc.log("Renaming %s to %s" % (name, new_name))
					doc.setNameAtAddress(adr, new_name)
		adr = adr + 1
		name = ''
	doc.refreshView()
