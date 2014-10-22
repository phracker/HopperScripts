doc = Document.getCurrentDocument()

seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()

instr = seg.getInstructionAtAddress(adr)
rip = adr + instr.getInstructionLength()

dst = int(doc.ask("Address destination:"), 0)

rel = dst - rip

print hex(rel).replace("L", "")