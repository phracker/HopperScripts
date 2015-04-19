#
# Add a comment at every XREF to a string (from the __cstring segment).
# This only seems to be necessary on ARM.
#
# Samuel Gross <dev@samuel-gross.de> - github.com/saelo
#

def readString(addr):
    """Read and return a string at the given address"""
    seg = Document.getCurrentDocument().getSegmentAtAddress(addr)
    string = ""
    while not seg.readByte(addr) == 0:
        string += chr(seg.readByte(addr))
        addr += 1
    return string


doc = Document.getCurrentDocument()

# find __cstring segment
stringSegment = None
for i in range(doc.getSegmentCount()):
    cur = doc.getSegment(i)
    if cur.getName() == '__cstring':
        stringSegment = cur
        break
if not stringSegment:
    doc.log("No cstring section found!")
    raise Exception("No cstring segment found!")

# find all strings
for addr in range(stringSegment.getStartingAddress(), stringSegment.getStartingAddress() + stringSegment.getLength()):
    if stringSegment.getTypeAtAddress(addr) == Segment.TYPE_ASCII:
        string = readString(addr)

        xrefs = stringSegment.getReferencesOfAddress(addr)
        # if there are no XREFs the above method apparently
        # returns "None" instead of an empty list...
        if xrefs:
            for xref in xrefs:
                xrefSegment = doc.getSegmentAtAddress(xref)
                comment = xrefSegment.getInlineCommentAtAddress(xref)
                if comment is None or comment.startswith('0x'):
                    xrefSegment.setInlineCommentAtAddress(xref,
                            '"%s"%s @0x%x' % (string[:100], '..' if len(string) > 100 else '', addr))

        addr += len(string)
