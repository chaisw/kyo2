# Node Transversal
from xml.dom.minidom import parse, parseString
import subprocess
import sys
sys.path.append("/home/chais/Projects/kyo")
from XmlNode import *

#subprocess.call("sudo lshw -C display -xml > /home/chais/Projects/kyo/test/lshw.xml", shell=True)
root = XmlNode.makeRoot(open('lshw.xml','rw'))

n = root.getChild('node')
prod = n.getChild('product').getData()
vend = n.getChild('vendor').getData()
print vend, prod