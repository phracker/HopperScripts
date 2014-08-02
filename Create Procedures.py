# This sample script will search for the standard pattern that
# identifies a function's prolog, and mark each of them as a procedure

doc = Document.getCurrentDocument()

# First, we disassemble the whole segment
seg = doc.getCurrentSegment()
seg.disassembleWholeSegment()

addr = seg.getStartingAddress()
last = addr + seg.getLength()
while addr < last:
    # Find the next unexplored area
    addr=seg.getNextAddressWithType(addr,Segment.TYPE_CODE)
    if addr == Segment.BAD_ADDRESS:
        break

    # Look for the "push ebp / mov ebp, esp" pattern
    if doc.is64Bits() and seg.readByte(addr) == 0x55 and seg.readByte(addr + 1) == 0x48 and seg.readByte(addr + 2) == 0x89 and seg.readByte(addr + 3) == 0xE5:
        seg.markAsProcedure(addr)
    if not doc.is64Bits() and seg.readByte(addr) == 0x55 and seg.readByte(addr + 1) == 0x89 and seg.readByte(addr + 2) == 0xE5:
        seg.markAsProcedure(addr)

    addr = addr + 1
