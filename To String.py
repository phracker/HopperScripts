#
# Turn the current selection into an ASCII string.
#
# Samuel Groß <dev@samuel-gross.de> - github.com/saelo
#

doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()
start, end = doc.getSelectionAddressRange()
bytes = [seg.readByte(addr) for addr in range(start, end)]

# check if selection is a valid ASCII string
if not bytes[-1] == 0:
    doc.log("Selection must include terminating null character")
    raise Exception("Invalid selection")
# maybe not the best way but the following should work with python 2.x and 3.x
if not all(0x20 <= byte <= 0x7e or byte == 0x0a or byte == 0x0d for byte in bytes[:-1]):
    doc.log("Selection is not a valid ASCII string")
    raise Exception("Invalid selection")
string = "".join([chr(b) for b in bytes[:-1]])

# mark bytes as string
seg.setTypeAtAddress(start, end - start, Segment.TYPE_ASCII)

# add comments to the addresses where the string is referenced
xrefs = seg.getReferencesOfAddress(start)
if xrefs:
    for xref in xrefs:
        xrefSegment = doc.getSegmentAtAddress(xref)
        comment = xrefSegment.getInlineCommentAtAddress(xref)
        if comment is None or comment.startswith('0x'):
            xrefSegment.setInlineCommentAtAddress(xref,
                    '"%s"%s' % (string[:100], '..' if len(string) > 100 else ''))
