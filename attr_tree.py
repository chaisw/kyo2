from lxml import etree

subprocess.call("sudo lshw -C display -xml > lshw.xml", shell=True)
tree = etree.parse("lshw.xml")
print etree.tostring(tree.getroot())