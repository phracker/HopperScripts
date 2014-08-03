doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()
dstStr = Document.ask("Enter destination address:")
if dstStr != None:
	dst = int(dstStr, 16)
	offset = dst - (adr + 5)
	after = adr + 5
	while seg.getTypeAtAddress(after) == Segment.TYPE_NEXT:
		after = after + 1
	seg.writeByte(adr + 0, 0xE9)
	seg.writeByte(adr + 1, ((offset >>  0) & 255))
	seg.writeByte(adr + 2, ((offset >>  8) & 255))
	seg.writeByte(adr + 3, ((offset >> 16) & 255))
	seg.writeByte(adr + 4, ((offset >> 24) & 255))
	seg.markAsCode(adr)
	adr = adr + 5
	while adr < after:
		seg.writeByte(adr, 0x90)
		seg.markAsCode(adr)
		adr = adr + 1
