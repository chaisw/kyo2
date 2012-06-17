#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gtk
import MySQLdb

attrs = dict.fromkeys(["manufac","prod_name","socket","family","cpu_manufac","voltage","speed","ram_type","ram_slots"], "")
MODEL = ""
MODEL_DES = ""
PROD_DES = ""
info = {}
has_submit = False
db = MySQLdb.connect(host="localhost", user="root", passwd="lined1", db="inventory")

class kyo(object):
	has_submit = False
	db = MySQLdb.connect(host="localhost", user="root", passwd="lined1", db="inventory")
	def __init__(self):
		#has_submit = False
		builder = gtk.Builder()
		builder.add_from_file("main_win.glade")
		#builder.add_from_file("main_win_libglade.glade")
		self.un_empty = builder.get_object("un_empty")
		self.pw_empty = builder.get_object("pw_empty")
		builder.connect_signals({ "on_window_destroy" : self.quit, "gtk_main_quit" : self.quit, "on_submit_clicked" : self.nextWin, "on_clear_clicked" : self.clearBoxes, "on_des_submit_clicked" : self.submit, "on_about_activate" : self.about, "on_login_submit_button_press_event" : self.login, "on_button1_clicked" : self.un_hide, "on_button2_clicked" : self.pw_hide})
		self.login_window = builder.get_object("login_window")
		self.window = builder.get_object("window")
		self.about = builder.get_object("aboutdialog")
		self.manu = builder.get_object("manufac")
		self.mod = builder.get_object("model")
		self.moddes = builder.get_object("modeldes")
		self.des_win = builder.get_object("des_window")
		self.des = builder.get_object("prod_des_textbuffer")
		self.un = builder.get_object("username")
		self.pw = builder.get_object("password")
		self.done = builder.get_object("exit_window")
		self.combo = builder.get_object("combobox")
		self.dup_window = builder.get_object("dup_window")
		
		f = open('last_username', 'r+')
		lun = f.readline().rstrip(" \n")
		if lun != "":
			self.un.set_text(lun)
		self.manu.set_text(attrs["manufac"])
		self.mod.set_text(attrs["prod_name"])
		self.moddes.set_text(MODEL_DES)
		
		self.login_window.show()
	
	def submit(self, widget):
		print "YO SUBMIT"
		MODEL = self.mod.get_text()
		"""print self.manu.get_text()
		print self.mod.get_text()
		print self.moddes.get_text()
		print self.des.get_text(self.des.get_start_iter(), self.des.get_end_iter(), True)"""
		# add item to local database via SQL
		c = self.db.cursor()
		sqlq = "INSERT INTO desktops (model, cpu, manufacturer, ram) VALUES (\'" + MODEL + "\', \'" + attrs["cpu_manufac"] + " " + attrs["family"] + " " + attrs["socket"] + " " + attrs["speed"] + " " + attrs["voltage"] + "\', \'" + attrs["manufac"] + " " + attrs["prod_name"] + "\', \'" + attrs["ram_slots"] + " " + attrs["ram_type"] + " " + attrs["ram_sizes"] + "\');"
		#print sqlq
		#db.query(sqlq)
		sqlq2 = ""
		try:
			sqlq2 = str("INSERT INTO desktops (model) VALUE (\'" + MODEL + "\');")
		except:
			self.dup_window.show()
		#print sqlq2
		#self.db.query(sqlq2)
		#print self.db.query("SELECT * FROM desktops")
		try:
			c.execute(sqlq2)
		except:
			self.dup_window.show()
		#c.execute("INSERT INTO desktops (additional_desc) VALUE (%s);", self.des.get_text(self.des.get_start_iter(), self.des.get_end_iter(), True),)
		#print c.execute("SELECT * FROM desktops")
		#max_price=5; c.execute("SELECT spam, eggs, sausage FROM breakfast WHERE price < %s", (max_price,))
		self.des_win.hide()
		self.done.show()
		#self.clearBoxes(widget)
		return True
		
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
		#print attrs["speed"], attrs["voltage"]
		
		if self.has_submit == False:
			self.des.insert(self.des.get_end_iter(), attrs["manufac"] + " " + attrs["prod_name"] + "\n\n")
			self.des.insert(self.des.get_end_iter(), attrs["cpu_manufac"] + " " + attrs["family"] + "\n")
			self.des.insert(self.des.get_end_iter(), attrs["socket"] + "\n")
			self.des.insert(self.des.get_end_iter(), attrs["speed"] + ", ")
			self.des.insert(self.des.get_end_iter(), attrs["voltage"] + "\n\n")
			print info[7], info[8]
			bt = False
			i3e = False
			if len(info[7]) >= 1:
				bt = True
				self.des.insert(self.des.get_end_iter(), "Bluetooth Enabled")
			if len(info[8]) >= 1:
				i3e = True
				if bt:
						self.des.insert(self.des.get_end_iter(), ", ")
				self.des.insert(self.des.get_end_iter(), "IEEE 1394 Port\n\n")
			self.des.insert(self.des.get_end_iter(), attrs["ram_slots"] + " " + attrs["ram_type"] + " RAM Slots\n")
			self.des.insert(self.des.get_end_iter(),"  Sizes: " + attrs["ram_sizes"])
			
			print self, widget
			self.des_win.show()
			#gtk.widget_show(widget)
		self.has_submit = True
		return True
		
	def about(self, widget, event):
		self.about.show()
		return True
	
	def login(self, widget, event=""):
		username = self.un.get_text().rstrip(' \n')
		password = self.pw.get_text().rstrip(' \n')
		print username, password
		if username == "":
			self.un_empty.show()
		elif password == "":
			self.pw_empty.show()
		else:
			f = open('last_username', 'r+')
			f.write(username)
			f.close()
			self.login_window.hide()
			self.window.show()
		return True
		
	def un_hide(self, widget):
		self.un_empty.hide()
		return True
	def pw_hide(self, widget):
		self.pw_empty.hide()
		return True
		
def read_input_file(filename):
	file = open(filename, "r")
	vars = {}
	i = 0
	for line in file:
		vars[i] = line.rstrip(' \n')
		i += 1
	file.close()
	return vars
    
if __name__ == "__main__":
	info = read_input_file("inf")
	attrs.update(dict.fromkeys(["manufac"], info[0]))
	attrs.update(dict.fromkeys(["prod_name"], info[1]))
	attrs.update(dict.fromkeys(["socket"], info[2]))
	attrs.update(dict.fromkeys(["family"], info[3]))
	attrs.update(dict.fromkeys(["cpu_manufac"], info[4]))
	attrs.update(dict.fromkeys(["voltage"], info[5]))
	attrs.update(dict.fromkeys(["speed"], info[6]))
	attrs.update(dict.fromkeys(["ram_type"], info[10]))
	attrs.update(dict.fromkeys(["ram_slots"], info[11]))
	attrs.update(dict.fromkeys(["ram_sizes"], info[12]))
	print attrs["ram_sizes"]
	#for i in range(9,12): print info[i]
	
	MODEL = info[1]
	app = kyo()
	gtk.main()