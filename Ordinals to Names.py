import os
import re
import traceback

def get_hopper_script_dir():
    """Detect the Hopper script directory and return it if found"""

    dirs = [os.path.expanduser("~/.local/share/data/Hopper/scripts"),
            os.path.expandvars("%LOCALAPPDATA%/Hopper/scripts"),
            os.path.expanduser("~/Library/Application Support/Hopper/Scripts/HopperScripts")]
    for directory in dirs:
        if os.path.exists(directory):
            return directory
    return None

def find_import_before(doc, start_address, max_bytes=200):
    """Find the last import comment before an address, return the library name if found."""
    for adr in range(start_address, start_address - max_bytes, -1):
        lib = get_import_at(doc, adr)
        if lib:
            return lib
    return None

def get_import_at(doc, address):
    """Check the comment at address for a import library name and return it if found."""
    segment = doc.getSegmentAtAddress(address)
    if segment is not None:
        comment = segment.getCommentAtAddress(address)
        if comment.startswith("Imports from"):
            return comment[13:]
    return None

# Regular expression to match lines in our symbol files.
symbol_line = re.compile(r"^\s*(?:(\w+)\s+(\w+))?\s*([;#].*)?$")

def get_symbols(doc, lib):
    """Load symbols from library.txt and return them as a dictionary."""

    basename = lib.replace(".dll", "").lower()
    filename = os.path.join(get_hopper_script_dir(), basename + ".txt")
    if not os.path.exists(filename):
        doc.log("Symbol file not found: %s" % filename)
        return None

    symbols = {}
    with open(filename, "r") as fp:
        for i, line in enumerate(fp, 1):
            match = symbol_line.match(line)
            if not match:
                doc.log("Skipping line %d: Malformed" % i)
                continue

            ordinal, name = match.group(1), match.group(2)
            if ordinal and name:
                symbols[ordinal] = name

    return symbols

def main(doc):
    lower, upper = doc.getSelectionAddressRange()
    doc.log("Selection: %x - %x" % (lower, upper))

    # Hopper renames duplicate imports with their address, this regex matches those.
    imp_address = re.compile(r"(imp_ordinal_\d+)_[0-9a-f]+")

    # Find the last library name before the selection and load it's symbols.
    current_lib = find_import_before(doc, lower)
    if current_lib:
        doc.log("Loading symbols for %s" % current_lib)
        symbols = get_symbols(doc, current_lib)
    else:
        symbols = None

    for adr in range(lower, upper, 4):
        # See if this address has a comment indicating a library name.
        lib = get_import_at(doc, adr)
        if lib is not None and lib != current_lib:
            current_lib = lib
            doc.log("Loading symbols for %s" % current_lib)
            symbols = get_symbols(doc, current_lib)

        # If the current address indicates a name, and we have symbols,
        # see if we can replace it with a name from the symbol file.
        name = doc.getNameAtAddress(adr)
        if symbols and name is not None:
            # If the name ends with an address, strip that off.
            match = imp_address.match(name)
            if match: name = match.group(1)

            if name in symbols:
                doc.log("Renaming %s to %s" % (name, symbols[name]))
                doc.setNameAtAddress(adr, symbols[name])

    doc.log("Done")
    doc.refreshView()

doc = Document.getCurrentDocument()
try:
    main(doc)
except:
    # Exceptions seem to get lost in Hopper somewhere, so make sure we log a
    # traceback if anything goes wrong.
    doc.log("Unhandled Exception in Ordinals to Names")
    doc.log(traceback.format_exc())
