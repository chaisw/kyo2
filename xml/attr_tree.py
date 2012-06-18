from lxml import etree
import subprocess

#subprocess.call("sudo lshw -C display -xml > lshw.xml", shell=True)
tree = etree.parse("lshw.xml")
root = tree.getroot()
print etree.tostring(root[0][0])
print root[0].get("description")