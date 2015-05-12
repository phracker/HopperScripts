# vim: tabstop=4:softtabstop=4:shiftwidth=4:noexpandtab:

# Copyright: (c)2015 Chris Kuethe <chris.kuethe+github@gmail.com>
# License: Perl Artistic <http://dev.perl.org/licenses/artistic.html>
# Description: save document labels and comments to a file

import json
from datetime import datetime

doc = Document.getCurrentDocument()
symtab = dict()

nsegs = doc.getSegmentCount()
for segnum in range(nsegs):
	doc.log('processing segment %d/%d' % (segnum+1,nsegs))
	seg = doc.getSegment(segnum)
	for label in seg.getLabelsList():
		addr = doc.getAddressForName(label)
		addr_comm = seg.getCommentAtAddress(addr)
		addr_icom = seg.getInlineCommentAtAddress(addr)
		generic_name = "sub_%x" % addr
		if (label != generic_name) or (addr_comm is not None) or (addr_comm is not None):
			doc.log(label)
			symtab[addr] = {'seg': segnum, 'comm': addr_comm, 'icom': addr_icom, 'name': label}


t = datetime.strftime(datetime.now(), 'annotation-%Y%m%d%H%M%S.json')
outfile = doc.askFile('file to save?', t, t)
if outfile is not None:
	try:
		f = open(outfile, "a+")
		f.write(json.dumps(symtab, sort_keys=True, indent=4))
		f.close()
		doc.log("saved to %s" % outfile)
	except Exception as e:
		doc.log("failed to save %s" % outfile)
		doc.log(e)
