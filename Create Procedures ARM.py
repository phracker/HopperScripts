# Based off of the Create Procedures sample script, but for ARM
# bradenthomas@me.com

import struct,sys

# configuration parameters, adjust as needed:
ENDIANNESS = "<" # Little endian = <, Big endian = >

# helper methods
def read_data(segment, addr, dlen):
    return "".join([chr(segment.readByte(addr+x)) for x in range(0,dlen)])

# First, we disassemble the whole segment
doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
if not seg:
    raise Exception("No segment selected")
seg.disassembleWholeSegment()

# Get segment starting address
addr = seg.getStartingAddress()
last = addr + seg.getLength()
while addr < last:
    # Find the next unexplored area
    addr=seg.getNextAddressWithType(addr,Segment.TYPE_CODE)
    if addr == Segment.BAD_ADDRESS:
        break

    # Copy a 16-bit value to see if it is in thumb mode
    try:
        halfword_value, = struct.unpack(ENDIANNESS+"H", read_data(seg, addr, 2))
    except:
        continue

    # Look for the push in thumb mode
    if halfword_value & 0xff00 == 0xb500: # PUSH (A7.1.50) with link register in the list.  Will not find every procedure, but low on false positives
        seg.markAsProcedure(addr)
    else:
        # Look for push in ARM mode
        try:
            word_value, = struct.unpack(ENDIANNESS+"I", read_data(seg, addr, 4))
        except:
            continue
        if word_value & 0xffffff00 == 0xe92d4000: # PUSH with link register in list, as above
            seg.markAsProcedure(addr)

    addr += 2