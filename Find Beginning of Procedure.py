def looksLikeBeginning(doc,seg,adr):
	if doc.is64Bits() and seg.readByte(adr) == 0x55 and seg.readByte(adr + 1) == 0x48 and seg.readByte(adr + 2) == 0x89 and seg.readByte(adr + 3) == 0xE5:
		return True
	if not doc.is64Bits() and seg.readByte(adr) == 0x55 and seg.readByte(adr + 1) == 0x89 and seg.readByte(adr + 2) == 0xE5:
		return True
	return False

doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()
str = seg.getStartingAddress()

while adr > str:
	if looksLikeBeginning(doc,seg,adr):
		doc.moveCursorAtAddress(adr)
		break
	adr = adr - 1
