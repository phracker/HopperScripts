doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()

s = doc.ask("String:")
s += '\0'

for i, c in enumerate(s):
	seg.writeByte(adr + i, ord(c))

seg.setTypeAtAddress(adr, len(s), seg.TYPE_ASCII)
