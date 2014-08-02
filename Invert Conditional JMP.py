def writeByteAndPreserveProc(seg,instr_adr,adr,b):
	proc = seg.getProcedureAtAddress(instr_adr)
	entry = proc.getEntryPoint() if proc != None else Segment.BAD_ADDRESS
	seg.writeByte(adr, b)
	seg.markAsCode(instr_adr)
	if entry != Segment.BAD_ADDRESS:
		seg.markAsProcedure(entry)
	
doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()
b = seg.readByte(adr)
if b < 0x70 or b > 0x7F:
	if b == 0x0F:
		b = seg.readByte(adr + 1)
		if b < 0x80 or b > 0x8F:
			print "Not a conditional jump"
		else:
			writeByteAndPreserveProc(seg, adr, adr + 1, b ^ 0x01)
	else:
		print "Not a conditional jump"
else:
	writeByteAndPreserveProc(seg, adr, adr, b ^ 0x01)
