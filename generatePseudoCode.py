from os.path import exists, expanduser, split
from os import makedirs

doc = Document.getCurrentDocument()
seg = doc.getCurrentSegment()

# get proc count
procCount = seg.getProcedureCount()
homeDir = expanduser("~")
head, appName = split(doc.getExecutableFilePath())
path = homeDir + '/hopperDumps/' + appName + '/'
if not exists(path):
	makedirs(path)

# iterate through procs
i = 0
while i < procCount:
	# get proc
	proc = seg.getProcedureAtIndex(i)
	# get proc's name
	name = seg.getNameAtAddress(proc.getEntryPoint())
	if name:
		# clean the name of any unsavoury chars
		items = ["[", "]", ":"]
		for item in items:
			name = name.replace(item, "")
		name = name.replace(" ", "__")
	
		# grab the decompilation
		output = proc.decompile()

		# open up a file handler for the name
		with open(path + name +'.pseu', 'w') as outFile:
			outFile.write(output + '\n')
	i += 1

print "[*] Pseudo code export complete. Export located at: %s" % (path)