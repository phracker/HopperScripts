######### Return True #########
bytes = [0xB8,0x01,0x00,0x00,0x00,0xC3]
doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()
i = seg.getInstructionAtAddress(adr)
for x in range(0, len(bytes)): seg.writeByte(adr + x, bytes[x])
