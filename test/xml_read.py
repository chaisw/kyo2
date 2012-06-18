from xml.dom.minidom import parseString
import subprocess
from XmlNode import *

subprocess.call("sudo lshw -xml > /home/chais/Projects/kyo/test/lshw.xml", shell=True)

file = open('lshw.xml','r') #open the xml file for reading
#data = file.read() #convert to string
data_list = file.readlines()
file.close()

del data_list[0:5]

fout = open("lshw.xml", "w")
fout.writelines(data_list)
fout.close()

file1 = open('lshw.xml','r')
data = file1.read()
file1.close()

dom = parseString(data) #parse the xml you got from the file
#prod = find_element(dom, "product")
vend = dom.childNodes[0].childNodes[1].childNodes[5].childNodes[0].nodeValue
prod = dom.childNodes[0].childNodes[1].childNodes[3].childNodes[0].nodeValue
print prod

#retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
xmlTag = dom.getElementsByTagName('list')[0].toxml()
#strip off the tag (<tag>data</tag>  --->   data):
xmlData=xmlTag.replace('<list>','').replace('</list>','')
#print out the xml tag and data in this format: <tag>data</tag>
#print xmlTag
#just print the data
#print "dom.childNodes[0]",dom.childNodes[0].childNodes[0]
#print xmlData