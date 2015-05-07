'''
Find UTF-8 strings in binaries

Author: Chris Kuethe (github.com/ckuethe)
Props-to: 090h (github.com/0x90)
'''
import time

doc = Document.getCurrentDocument()

start_time = time.clock()

def is_valid_ascii(byte):
	return (byte >= 0x20 and byte <= 0x7e) or (chr(byte) in "\r\n\t")

def is_null(byte):
	return byte == 0x00

MIN_LEN = 6

num_strings = 0
start_string = 0
string_len = 0

for seg_id in range(0, doc.getSegmentCount()):
	seg = doc.getSegment(seg_id)

	seg_start = seg.getStartingAddress()
	seg_stop = seg_start + seg.getLength()
	seg_len = seg.getLength()

	doc.log("searching segment %d, length %d" % (seg_id, seg_len))
	i = 0
	for adr in range(seg_start, seg_stop-1):
		cur_byte = seg.readByte(adr)
		nxt_byte = seg.readByte(adr+1)

		i += 1
		if (i % 4096 == 0):
			doc.log("%.1f%% " % (i * 100.0 / seg_len) )

		if is_valid_ascii(cur_byte) and is_null(nxt_byte):
			string_len += 1
			if start_string == 0:
				start_string = adr

		elif is_null(cur_byte) and is_valid_ascii(nxt_byte):
			string_len += 1

		elif is_null(cur_byte) and is_null(nxt_byte):
			if string_len >= MIN_LEN:
				seg.setTypeAtAddress(start_string, string_len + 2, Segment.TYPE_UNICODE)
				num_strings += 1
				string_len = 0
				start_string = 0
			else:
				start_string = 0
				string_len = 0
		else:
			start_string = 0
			string_len = 0
	if is_null(nxt_byte) and (string_len >= MIN_LEN):
		seg.setTypeAtAddress(start_string, string_len + 2, Segment.TYPE_UNICODE)
		num_strings += 1

elapsed = (time.clock() - start_time)
doc.log("Found and marked " + str(num_strings) + " strings in " + str(elapsed) + " seconds.")
doc.refreshView()
