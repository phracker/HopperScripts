doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
adr = doc.getCurrentAddress()
ins = seg.getInstructionAtAddress(adr)
arch = ins.getArchitecture()

if not arch in [1, 2]:
	doc.log('Unsupported arch!')
else:
	if not ins.isAConditionalJump():
		doc.log('Not a conditional jump!')
	else:
		b = seg.readByte(adr)
		if 0x70 <= b <= 0x7F:
			# rel8
			seg.writeByte(adr, 0xEB)
			seg.markAsCode(adr)
		elif b == 0x0F:
			b = seg.readByte(adr + 1)
			if 0x80 <= b <= 0x8F:
				# rel16/32
				seg.writeByte(adr, 0x90)
				seg.writeByte(adr + 1, 0xE9)
				seg.markAsCode(adr)
			else:
				doc.log('Unknown conditional jump!')
		else:
			doc.log('Unknown conditional jump!')
