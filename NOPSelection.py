######### NOP Selection #########
doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()
start, end = doc.getSelectionAddressRange()
for x in range(start,end):
  seg.writeByte(x,0x90)
  seg.markAsCode(x)
