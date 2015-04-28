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
	addr += 3

    x = seg.readByte(addr)
    y = seg.readByte(addr + 1)
    z = seg.readByte(addr + 2)
    if not doc.is64Bits() and x == 0x55 and y in (0x89, 0x8B) and z in (0xE5, 0xEC):
        seg.markAsProcedure(addr)
	addr += 2

    addr = addr + 1
