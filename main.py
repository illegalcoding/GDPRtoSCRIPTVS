import requests
from bs4 import BeautifulSoup
import textwrap
import unicodedata
def toascii(text):
	return unicodedata.normalize('NFKD',text.replace('\u2018','\'').replace('\u2019','\'')).encode('ascii','ignore')
boilerplate = """.df title1 type('Helvetica' 18 bold)
.df title2 type('Helvetica' 20 bold)
.df norm type('Helvetica' 12)
.ti ^ 05
.ju off
.rf cancel
.pn off
.rh cancel
.bf title1
.ce on
"""
aftertitle1 = ".bf title2\n"
aftertitle2 = ".bf norm\n.sp 3\n.ce off\n"
beforepara = ".of\n.of 5\n"
afterpara = ".bl\n"
beforepoint = ".of\n.of 10\n.il 5\n"
afterpoint = ".bl\n"
alphabet = "abcdefghijklmnopqrstuvwxyz"
def getArticleURL(num):
	return "https://gdpr-info.eu/art-{0}-gdpr/".format(num)

def articleToScript(num):
	url = getArticleURL(num)
	httpResponse = requests.get(url)
	responseContent = httpResponse.content
	soup = BeautifulSoup(responseContent,"html.parser")
	title1 = soup.find_all("span",{"class":"dsgvo-number"})[0].text
	title1Wrapped = textwrap.wrap(title1,width=50)
	title1WrappedFull = ""
	for line in title1Wrapped:
		title1WrappedFull = title1WrappedFull + line + "\n"
	title2 = soup.find_all("span",{"class":"dsgvo-title"})[0].text
	title2Wrapped = textwrap.wrap(title2,width=50)
	title2WrappedFull = ""
	for line in title2Wrapped:
		title2WrappedFull = title2WrappedFull + line + "\n"
	entrycontent = soup.find_all("div",{"class":"entry-content"})[0]
	ol = entrycontent.find("ol")
	if(ol == None):
		p = entrycontent.find("p",recursive=False)
		sups = p.find_all("sup")
		for sup in sups:
			sup.clear()
		wrappedText = textwrap.wrap(p.text,width=50)
		fullWrappedText = ""
		for line in wrappedText:
			fullWrappedText = fullWrappedText + line + "\n"
		file = open("art{0}.script".format(num),"wb")
		file.write(toascii(boilerplate))
		file.write(toascii(title1WrappedFull))
		file.write(toascii(aftertitle1))
		file.write(toascii(title2WrappedFull))
		file.write(toascii(aftertitle2))
		file.write(toascii(fullWrappedText))
		file.close()
		print(p)
		return
	liList = ol.find_all("li",recursive=False)
	supLiList = ol.find_all("li",recursive=True)
	for li in supLiList:
		sups = li.find_all("sup")
		for sup in sups:
			sup.clear()
	print(liList[0].find('p'))
	file = open("art{0}.script".format(num),"wb")
	file.write(toascii(boilerplate))
	file.write(toascii(title1WrappedFull))
	file.write(toascii(aftertitle1))
	file.write(toascii(title2WrappedFull))
	file.write(toascii(aftertitle2))
	for i in range(len(liList)):
		hadNested = 0
		if liList[i].find("ol") != None:
			hadNested = 1
			print("Paragraph {0} has subpoints".format(i+1))
			nestedLi = liList[i].find_all('li')
			firstLine = liList[i].text.split('\n')[0]
			wrappedFirstLine = textwrap.wrap(firstLine,width=50)
			fullWrappedFirstLine = ""
			for line in wrappedFirstLine:
				fullWrappedFirstLine = fullWrappedFirstLine + line + "\n"
			file.write(toascii(beforepara))
			file.write(toascii(str(i+1)+".^"+fullWrappedFirstLine))
			for j in range(len(nestedLi)):
				if(j == 0):
					file.write(toascii(".bl\n"))
				li = nestedLi[j]
				wrappedText = textwrap.wrap(li.text,width=50)
				fullWrappedText = ""
				for line in wrappedText:
					fullWrappedText = fullWrappedText + line + "\n"
				file.write(toascii(beforepoint))
				file.write(toascii("({0})^{1}".format(alphabet[j],fullWrappedText)))
				file.write(toascii(afterpoint))
				#print(li.text)
		if liList[i].find("p") != None:
			print(liList[i].find_all("p"))
			sups = liList[i].find("p").find_all("sup")
			for sup in sups:
				sup.clear()
			print("Got extra <p> on paragraph {0}".format(i+1))
			paragraphText = liList[i].find_all("p")[0].text
			wrappedText = textwrap.wrap(paragraphText,width=50)
			fullWrappedText = ""
			for line in wrappedText:
					fullWrappedText = fullWrappedText + line + "\n"
			file.write(toascii(".bl\n.of\n.of 5\n.il 5\n"))
			file.write(toascii(fullWrappedText))
			file.write(toascii(".bl\n"))
			continue
		if hadNested == 1:
			continue
		text = liList[i].text
		wrappedText = textwrap.wrap(text,width=50)
		#print(str(i+1) + ".",end="")
		#print("\t",end="")
		#print(wrappedText)
		fullWrappedText = ""
		for line in wrappedText:
			fullWrappedText = fullWrappedText + line + "\n"
		file.write(toascii(beforepara))
		file.write(toascii(str(i+1)+".^"+fullWrappedText))
		if i != len(liList)-1:
			file.write(toascii(afterpara))
	file.close()
	#print(url)
	return

for i in range(1,100):
	print("Doing article {0}".format(i))
	articleToScript(i)