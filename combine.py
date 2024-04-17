import os
import unicodedata
def toascii(text):
	return unicodedata.normalize('NFKD',text.replace('\u2018','\'').replace('\u2019','\'')).encode('ascii','ignore')
for i in range(1,100):
	if not os.path.exists("art{0}.script".format(i)):
		print("Couldn't find art{0}.script".format(i))
		exit(-1)
outFile = open("combined.script","wb")
for i in range(1,100):
	splitFile = open("art{0}.script".format(i),"r")
	text = splitFile.read()
	splitText = text.split("\n")
	fullText = ""
	if i != 1:
		outFile.write(toascii(".pa\n.of\n"))
		for i in range(8,len(splitText)):
			if i != len(splitText)-1:
				fullText = fullText + splitText[i] + "\n"
			else:
				fullText = fullText + splitText[i]
	else:
		fullText = text
	outFile.write(toascii(fullText))
outFile.close()

#file = open("combined.script","wb")