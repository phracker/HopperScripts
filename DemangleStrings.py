doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
adr = seg.getStartingAddress()
last = adr + seg.getLength()

PIC = 0

#Loop through the whole code segment
#if you want to do a single proceedure
#it should be trivial to add in
while adr < last:
  instr = seg.getInstructionAtAddress(adr)
  #If the instruction sets the PIC Register value in a register
  if instr.getInstructionString() == "mov":
    register = instr.getFormattedArgument(0)
    value = instr.getFormattedArgument(1)
    if value.endswith("+_PIC_register_"):
      adr += instr.getInstructionLength()
      instr = seg.getInstructionAtAddress(adr)
      value = instr.getFormattedArgument(1)
      #And if it uses the newly set register in the next insturction
      if register in value:
        register += "+"
        value = value.replace(register,"")
        if value.startswith("0x"):
          offset = int(value, 0)
          offset = offset+PIC
          #Extract the comment
          segment = doc.getSegmentAtAddress(offset)
          comment = "\""
          while segment.readByte(offset) != 0:
            comment += chr(segment.readByte(offset))
            offset += 1
          comment += "\" at " + hex(offset)
          #Set it
          seg.setInlineCommentAtAddress(adr, comment)
          doc.log("[0x%X] Found calculated address of string %s" % (adr, comment))
  #if we call the address of the next instruction
  else:
    if instr.getInstructionString() == "call":
      value = instr.getFormattedArgument(0)
      if value.startswith("0x"):
        callTo = int(value, 0)
        adr += instr.getInstructionLength()
        #And if te call was to the next address, which was a pop
        if callTo == adr:
          instr = seg.getInstructionAtAddress(adr)
          if instr.getInstructionString() == "pop":
            #Reset our PIC
            PIC = callTo
  adr += instr.getInstructionLength()
