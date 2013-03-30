######### Copy Highlighted Address to Clipboard #########
import os
doc = Document.getCurrentDocument()
adr = doc.getCurrentAddress()
os.system("echo '%X' | tr -d '\n' | pbcopy" % adr)
