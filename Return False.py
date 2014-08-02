######### Return False #########
bytes = [0x31,0xC0,0xC3]
doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()
i = seg.getInstructionAtAddress(adr)
for x in range(0, len(bytes)):
  seg.writeByte(adr + x, bytes[x])
