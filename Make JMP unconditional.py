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
			seg.writeByte(adr, 0x90)
			seg.writeByte(adr + 1, 0xE9)
			seg.markAsCode(adr)
	else:
		print "Not a conditional jump"
else:
	seg.writeByte(adr, 0xEB)
	seg.markAsCode(adr)
