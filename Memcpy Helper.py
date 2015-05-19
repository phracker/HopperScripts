# vim: tabstop=4:softtabstop=4:shiftwidth=4:noexpandtab:

# Copyright: (c)2015 Chris Kuethe <chris.kuethe+github@gmail.com>
# License: Perl Artistic <http://dev.perl.org/licenses/artistic.html>
# Description: copy regions of memory, adding analyst comments

doc = Document.getCurrentDocument()

def input_to_num(inputstr):
	'''converts input to number, possibly resolving from hex or named address'''
	addr = doc.getAddressForName(inputstr)
	if addr is not None: # user input a named address?
		out = doc.readUInt32LE(addr) # XXX assume it's little endian
	else: # nope, that didn't work. let's pretend it's a number.
		i = inputstr.lower()
		if '0x' in i:
			out = int(i, 16)
		else:
			out = int(i)
	#doc.log("converted '%s' to %d" % (inputstr, out))
	return out

reloc_src = doc.ask("relocation source?")
reloc_dst = doc.ask("relocation target?")
reloc_len = doc.ask("relocation length?")

reloc_src = input_to_num(reloc_src)
reloc_dst = input_to_num(reloc_dst)
reloc_len = input_to_num(reloc_len)

seg = doc.getSegmentAtAddress(reloc_dst)
for i in range(reloc_len):
	b = doc.readByte(reloc_src + i)
	if doc.writeByte(reloc_dst + i, b) is not None:
		n = doc.getNameAtAddress(reloc_src + i)
		if n is not None:
			seg.setInlineCommentAtAddress(reloc_dst + i, n)
doc.log("copied %d bytes from 0x%x to 0x%x" % (reloc_len, reloc_src, reloc_dst))
