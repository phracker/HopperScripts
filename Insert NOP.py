#
# Written by Moloch
# v0.1
#
### Opcodes
nop_opcodes = {
    1: 0x90, # 1 i386
    2: 0x90, # 2 x86_64
    3: 0x0000a0e1, # 3 ARM
}

### Functions
def write_nop(adr, arch):
    doc.log("Writing NOP to 0x%08x" % adr)
    seg.writeByte(adr, nop_opcodes[arch])
    seg.markAsCode(adr)

def overwrite_instruction(adr):
    instr = seg.getInstructionAtAddress(adr)
    arch = instr.getArchitecture()
    if arch not in nop_opcodes:
        doc.log("Error: CPU Architecture not supported")
    else:
        arch_name = Instruction.stringForArchitecture(instr.getArchitecture())
        doc.log("--- Inserting %s opcodes ---" % arch_name)
        if arch != 3:  # Ignore ARM
            for index in range(instr.getInstructionLength()):
                write_nop(adr + index, arch)
### Main
doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()

resp = doc.message("What do you want to NOP?", [
    " Current Instruction (0x%08x) " % adr,
    " Alternate Address ",
    " Cancel "
])
if resp == 0:
    overwrite_instruction(adr)
elif resp == 1:
    user_adr = Document.ask("Enter alternate address:")
    if user_adr is not None:
        if user_adr.startswith("0x"):
            user_adr = user_adr[2:]
        user_adr = int(user_adr, 16)
        doc.log("New address is: 0x%08x" % user_adr)
        if user_adr is not None and user_adr != Segment.BAD_ADDRESS:
            overwrite_instruction(user_adr)
        else:
            doc.log("Error: Bad Address %s" % user_adr)