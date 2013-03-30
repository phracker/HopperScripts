######### Copy Highlighted Hexadecimal to Clipboard #########
import os
doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()
instr = seg.getInstructionAtAddress(adr)
len = instr.getInstructionLength()
hex = ""
for j in range(0, len):
   hex += str("%02X" % seg.readByte(adr + j))
os.system("echo '%s' | tr -d '\n' | pbcopy" % hex)
