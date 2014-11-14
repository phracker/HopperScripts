import time

doc = Document.getCurrentDocument()

start_time = time.clock()

def is_valid_ascii(byte):
  return byte >= 0x20 and byte <= 0x7e

def is_null(byte):
  return byte == 0x00

MIN_LEN = 4

num_strings = 0
start_string = 0
string_len = 0

for seg_id in range(0, doc.getSegmentCount()):
  seg = doc.getSegment(seg_id)

  seg_start = seg.getStartingAddress()
  seg_stop = seg_start + seg.getLength()

  for adr in range(seg_start, seg_stop):
    val = seg.readByte(adr)

    if is_valid_ascii(val):
      string_len += 1
      if start_string == 0:
        start_string = adr
    elif is_null(val):
      if string_len >= MIN_LEN:
        seg.setTypeAtAddress(start_string, string_len + 1, Segment.TYPE_ASCII)
        num_strings += 1
        string_len = 0
        start_string = 0
      else:
        start_string = 0
        string_len = 0
    else:
      start_string = 0
      string_len = 0

elapsed = (time.clock() - start_time)
doc.log("Found and marked " + str(num_strings) + " strings in " + str(elapsed) + " seconds.")
