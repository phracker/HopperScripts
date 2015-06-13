# vim: tabstop=4:softtabstop=4:shiftwidth=4:noexpandtab:

# Copyright: (c)2015 Chris Kuethe <chris.kuethe+github@gmail.com>
# License: Perl Artistic <http://dev.perl.org/licenses/artistic.html>
# Description: label the ARM exception vectors and their targets

import struct

vectors = {	0x00: 'RESET',
		0x04: 'UNDEF_INSN',
		0x08: 'SUPERVISOR_CALL',
		0x0c: 'PREFETCH_ABORT',
		0x10: 'DATA_ABORT',
		0x14: 'HYPERVISOR_CALL',
		0x18: 'IRQ',
		0x1c: 'FIQ',
		0x20: 'SECURE_MONITOR_CALL',
	 }

doc = Document.getCurrentDocument()
# r = doc.getSelectionAddressRange()
# doc.log("Selection Range: %s" % r )

seg = doc.getSegment(0)
firstAddress = seg.getStartingAddress()

insn = seg.getInstructionAtAddress(firstAddress)
arch = insn.getArchitecture()
arch = insn.stringForArchitecture(arch)

if arch is 'ARM':
	last_vect = 0x24
	for addr in range(0, last_vect, 4):
		word, = struct.unpack("<I", seg.readBytes(addr, 4))
		if ((word & 0xffffff00 != 0xe59ff000) and (word & 0xffffff00 != 0xea000000)):
			continue

		# coerce the vector to be code
		seg.markRangeAsUndefined(addr, 4)
		seg.setARMModeAtAddress(addr)
		seg.markAsCode(addr)
		last_vect = addr

		# analyze the instruction
		insn = seg.getInstructionAtAddress(addr)
		istr = insn.getInstructionString()
		argA = insn.getRawArgument(0)
		argB = insn.getRawArgument(1)

		if istr == 'ldr' and argA == 'pc':
			offset = (word & 0xff) + addr + 8
			target, = struct.unpack("<I", seg.readBytes(offset, 4))
			print "offset 0x%02x, naming 0x%x as xhdlr_%s" % (offset, target, vectors[addr])
			doc.setNameAtAddress(target, "xhdlr_%s" % vectors[addr])
		elif istr == 'b':
			argA = int(argA, 16)
			doc.setNameAtAddress(argA, "xhdlr_%s" % vectors[addr])


	for addr in reversed(sorted(vectors.keys())):
		if addr > last_vect:
			continue
		print "vector 0x%02x - setNameAtAddress(0x%x, xp_%s)" % (addr, last_vect + addr + 4, vectors[addr])
		doc.setNameAtAddress(last_vect + addr + 4 , "xp_%s" % vectors[addr])
		doc.setNameAtAddress(addr, "xv_%s" % vectors[addr])
	
	doc.refreshView()
else:
	doc.log("Not an ARM binary")
