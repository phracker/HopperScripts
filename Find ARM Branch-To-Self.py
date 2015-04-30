# This script marks branch-to-self (0xe7fe) instructions. These are often
# used to wait for an event such as an interrupt.
# Based off of the "Create Procedures ARM" script by bradenthomas@me.com

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
        if halfword_value & 0xffff == 0xe7fe: # Branch to self
            seg.setNameAtAddress(addr, "loc_%x_bts" % addr)
    except:
        continue

    addr += 2
