#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gtk
import MySQLdb
import csv
from xml.dom.minidom import parseString

attributes = ["manufac", "prod_name",\
				  "socket", "family", "cpu_manufac", "voltage", "speed",\
				  "bluetooth", "ieee1394",\
				  "ram_type", "ram_slots", "ram_sizes",\
				  "serial", "screen_res", "hd_capacity",\
				  "in-house_number", "prod_desc"]

attrs = dict.fromkeys(attributes, "")
perfecto = {}
attrs.update({"ram_slots":0, "ram_sizes":[], "ieee1394":0, "in-house_number":1, "bluetooth":False})

MANUFACTURER = ""
MODEL = ""
MODEL_DES = ""
PROD_DES = ""
SERIAL = ""
info = {}
has_submit = False
db = MySQLdb.connect(host="localhost", user="root", passwd="lined1", db="inventory")

class item(object):
	has_submit = False
	db = MySQLdb.connect(host="localhost", user="root", passwd="lined1", db="inventory")
	def __init__(self):
		builder = gtk.Builder()
		good = False
		while good == False:
			try:
				builder.add_from_file("main_win.glade")
				good = True
			except:
				print "Try again."
				good = False
			
		#builder.add_from_file("main_win_libglade.glade")
		self.window = builder.get_object("window")
		self.login_window = builder.get_object("login_window")
		self.un_empty = builder.get_object("un_empty")
		self.pw_empty = builder.get_object("pw_empty")
		self.about_win = builder.get_object("aboutdialog")
		self.combo = builder.get_object("combobox")
		self.manu = builder.get_object("manufac")
		self.mod = builder.get_object("model")
		self.moddes = builder.get_object("modeldes")
		self.des_win = builder.get_object("des_window")
		self.des = builder.get_object("prod_des_textbuffer")
		self.un = builder.get_object("username")
		self.pw = builder.get_object("password")
		self.dup_window = builder.get_object("dup_window")
		self.done = builder.get_object("exit_window")
		
		builder.connect_signals({ "on_window_destroy" : self.quit, "gtk_main_quit" : self.quit,\
		"on_submit_clicked" : self.nextWin, "on_clear_clicked" : self.clearBoxes, "on_des_submit_clicked" : self.submit,\
		"on_about_activate" : self.about, "on_login_submit_button_press_event" : self.login,\
		"on_button1_clicked" : self.hide_win, "on_button2_clicked" : self.hide_win, "on_close_dup_clicked" : self.hide_win})
		
		f = open('last_login', 'r+')
		last_un = f.readline().rstrip(" \n")
		last_pw = f.readline().rstrip(" \n")
		if last_un != "":
			self.un.set_text(last_un)
		if last_pw != "":
			self.pw.set_text(last_pw)
		self.manu.set_text(MANUFACTURER)
		self.mod.set_text(MODEL)
		self.moddes.set_text(MODEL_DES)
		self.login_window.show()
	
	def submit(self, widget):
		print "YO SUBMIT"
		self.addToDB()
		self.des_win.hide()
		self.done.show()
		#self.clearBoxes(widget)
		return True
		
	def addToDB(self):
		MANUFACTURER = self.manu.get_text()
		MODEL = self.mod.get_text()
		SERIAL = attrs["serial"]
		print self.des.get_text(self.des.get_start_iter(), self.des.get_end_iter(), True)
		attrs["prod_desc"] = self.des.get_text(self.des.get_start_iter(), self.des.get_end_iter(), True)
		perfecto["prod_desc"] = attrs["prod_desc"]
		return True
		"""print self.manu.get_text()
		print self.mod.get_text()
		print self.moddes.get_text()
		#add item to local database via SQL
		c = self.db.cursor()
		sqlq = "INSERT INTO desktops (model, cpu, manufacturer, ram) VALUES (\'"\
		+ MODEL + "\', \'" + attrs["cpu_manufac"] + " " + attrs["family"] + " " + attrs["socket"] + " " + attrs["speed"] + " " + attrs["voltage"] + "\', \'" + attrs["manufac"] + " " + attrs["prod_name"] + "\', \'" + attrs["ram_slots"] + " " + attrs["ram_type"] + " " + attrs["ram_sizes"] + "\');"
		sqlq2 = ""
		dup = True
		while dup == True:
			try:
				sqlq2 = str("INSERT INTO desktops (model) VALUE (\'" + MODEL + "\');")
				c.execute(sqlq2)
				self.db.query(sqlq2)
				dup = False
			except:
				dup = True
				self.dup_window.show()
		print "Query: " + sqlq2
		#print self.db.query("SELECT * FROM desktops");print c.execute("SELECT * FROM desktops")
		#c.execute("SELECT spam, eggs, sausage FROM breakfast WHERE price < %s", (max_price,))"""
		
	def quit(self, widget):
		db.close()
		gtk.main_quit()
		
	def clearBoxes(self, widget):
		has_submit = False
		self.manu.set_text("")
		self.mod.set_text("")
		self.moddes.set_text("")
		return True
	
	def nextWin(self, widget):
		"""manuPrint = False
		for key in attrs:
			s = attrs[key]
			print key, s
			s = s + "\n"
			if key == "manufac" or key == "prod_name":
				manuPrint = True
				self.des.insert(self.des.get_start_iter(), s)
			else: self.des.insert(self.des.get_end_iter(), s)"""
		if self.has_submit == False:
			self.des.insert(self.des.get_end_iter(), perfecto["manufac"] + " " + perfecto["prod_name"] + "\n\n")
			self.des.insert(self.des.get_end_iter(), perfecto["cpu_manufac"] + " " + perfecto["family"] + "\n  ")
			self.des.insert(self.des.get_end_iter(), perfecto["socket"] + "\n  " + perfecto["speed"] + ", "\
			+ perfecto["voltage"] + "\n\n")
			
			self.des.insert(self.des.get_end_iter(), "Screen Resolution: " + perfecto["screen_res"] + "\n")
			#self.des.insert(self.des.get_end_iter(), "Hard Drive Present: " + perfecto["hd_present"] + "\n")
			self.des.insert(self.des.get_end_iter(), "Hard Drive Capacity: " + perfecto["hd_capacity"] + "\n")
				
			self.des.insert(self.des.get_end_iter(), str(perfecto["ram_slots"]) + " " + perfecto["ram_type"] + " RAM Slots\n")
			self.des.insert(self.des.get_end_iter(), "  Sizes: ")
			for i in range(0, int(perfecto["ram_slots"])):
				self.des.insert(self.des.get_end_iter(), perfecto["ram_sizes"][i] + " MB")
				if i != int(perfecto["ram_slots"from xml.dom.minidom import parseString])-1:
					self.des.insert(self.des.get_end_iter(), ", ")
				else: self.des.insert(self.des.get_end_iter(), "\n\n")
			
			if info[7] > 1:
				perfecto["bluetooth"] = True
				self.des.insert(self.des.get_end_iter(), "Bluetooth Enabled")
			if perfecto["ieee1394"] >= 1:
				if perfecto["bluetooth"]:
						self.des.insert(self.des.get_end_iter(), ", ")
				if perfecto["ieee1394"] == 1:
					self.des.insert(self.des.get_end_iter(), "1 IEEE 1394 Port\n")
				elif perfecto["ieee1394"] > 1:
					self.des.insert(self.des.get_end_iter(), perfecto["ieee1394"]+" IEEE 1394 Ports\n")
			else: self.des.insert(self.des.get_end_iter(), "\n")
			self.des_win.show()
			self.has_submit = True
		return True
		
	def about(self, widget, event=""):
		print "self:", str(self)
		self.about_win.show()
		return True
	
	def login(self, widget, event=""):
		done = False
		while done != True:
			if self.un.get_text() == "":
				self.un_empty.show()
			elif self.pw.get_text() == "":
				self.pw_empty.show()
			else:
				done = True
				username = self.un.get_text().rstrip(' \n')
				password = self.pw.get_text().rstrip(' \n')
				f = open('last_login', 'r+')
				f.write(username+"\n"+password)
				f.close()
				self.login_window.hide()
				self.window.show()
		return True
		
	def hide_win(window):
		print window
		self.window.hide()
		return True
		
	"""def readXML(self):
		#open the xml file for reading:
		file = open('lshw.xml','r')
		#convert to string:
		data = file.read()
		#close file because we dont need it anymore:
		file.close()
		#parse the xml you got from the file
		dom = parseString(data)
		#retrieve the first xml tag (<tag>data</tag>) that the parser finds with name tagName:
		xmlTag = dom.getElementsByTagName('tagName')[0].toxml()
		#strip off the tag (<tag>data</tag>  --->   data):
		xmlData=xmlTag.replace('<tagName>','').replace('</tagName>','')
		#print out the xml tag and data in this format: <tag>data</tag>
		#print xmlTag
		#just print the data
		print xmlData"""
		
		
def read_input_file(filename):
	file = open(filename, "r")
	vars = {}
	i = 0
	for line in file:
		vars[i] = line.rstrip(' \n')
		i += 1
	
	#for i in range(9,12): print info[i]
	file.close()
	return vars
    
if __name__ == "__main__":
	info = read_input_file("inf")
	#for i in range(0,len(info)):print "info[" + str(i) + "]: " + info[i]
	dWriter = csv.writer(open('desktops.csv', 'wb'), delimiter=',', quotechar='|')
	#,quoting=csv.QUOTE_MINIMAL)
	dWriter.writerow(attributes)
	
	values = []
	for i in range(0,len(info)):
		if i == 11:
			values.append(info[i].split(" "))
		else: values.append(info[i])
	print values
	dWriter.writerow(values)
	
	perfecto = dict(zip(attributes, values))
	#print "perfecto:", perfecto, "\n\n"
	"""print attributes
	print info
	print attrs"""
	for i in range(0, len(info)):
		attrs.update(dict.fromkeys(attributes[i], info[i]))
		print "attributes[" + str(i) + "]: " + attributes[i] + "\n\tinfo[" + str(i) + "]: " + str(info[i])
	for key in perfecto:
		print key + ": " + str(perfecto[key])
	
	MANUFACTURER = info[0]
	MODEL = info[1]
	app = item()
	gtk.main()