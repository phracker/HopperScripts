# vim: tabstop=4:softtabstop=4:shiftwidth=4:noexpandtab:

# Copyright: (c)2015 Chris Kuethe <chris.kuethe+github@gmail.com>
# License: Perl Artistic <http://dev.perl.org/licenses/artistic.html>
# Description: imports address labels and comments from a JSON file

import json

doc = Document.getCurrentDocument()
infile = doc.askFile('Select annotation file', None, None)
if infile is not None:
	f = open(infile, "r")
	symtab = json.loads(f.read())
	f.close()

	tseg = -1
	seg = None
	for addr in symtab.keys():
		try:
			a = symtab[addr]
			addr = int(addr, 16)
			if ((a['seg'] != tseg) or (seg is None)):
				tseg = a['seg']
				seg = doc.getSegment(a['seg'])
			if a['name'] is not None:
				seg.setNameAtAddress(addr, a['name'])
			if a['comm'] is not None:
				seg.setCommentAtAddress(addr, a['comm'])
			if a['icom'] is not None:
				seg.setInlineCommentameAtAddress(addr, a['icom'])
		except Exception:
			pass
	doc.log("loaded annotations from %s" % infile)
doc.refreshView()
