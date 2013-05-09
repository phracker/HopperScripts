#!/usr/bin/python
import pefile
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >>sys.stderr, "Usage: %s DLL" % sys.argv[0]
        sys.exit(1)

    filename = sys.argv[1]
    if not os.path.exists(filename):
        print >>sys.stderr, "'%s' does not exist" % filename
        sys.exit(1)

    d = [pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_EXPORT"]]
    pe = pefile.PE(filename, fast_load=True)
    pe.parse_data_directories(directories=d)

    print "# %s exports for 'Ordinals to Names' Hopper Script" % os.path.basename(filename)
    print "# Ordinal        Name"

    exports = [(e.ordinal, e.name) for e in pe.DIRECTORY_ENTRY_EXPORT.symbols]
    for export in sorted(exports):
        print "imp_ordinal_%-4d imp_%s" % export
