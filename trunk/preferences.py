# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import cons

class Preferences():
	""""""
	def __init__(self, config):
		""""""
		self.configuration = config
		builder = config.builder
		
		#Get objects
		self.dialog = builder.get_object("PreferencesDialog")
		self.newpreferences = builder.get_object("newpreferences")
		self.newpreferences2 = builder.get_object("newpreferences2")
		self.newpreferences3 = builder.get_object("newpreferences3")
		self.colorpreferences = builder.get_object("colorpreferences")
		
		#Get signals
		self.newpreferences.connect("pressed", self.newcall, 1)
		self.newpreferences2.connect("pressed", self.newcall, 3)
		self.newpreferences3.connect("pressed", self.newcall, 7)
		
		self.new = int(self.configuration.getValue("new","newDay"))
		self.newoption()

		self.color=self.configuration.getValue("viewer","viewerBackground")
		self.colorpreferences.set_color(gtk.gdk.color_parse(self.color))
		
		
	def newoption(self):
		""""""
		if self.new == 1:
			self.newpreferences.set_active(True)
		elif self.new == 3:
			self.newpreferences2.set_active(True)
		elif self.new == 7:
			self.newpreferences3.set_active(True)

	def open(self):
		""""""
		auxnew = self.new
		self.newoption()
		self.colorpreferences.set_color(gtk.gdk.color_parse(self.color))
		
		response = self.dialog.run()
		
		if response == 1:
			self.color=self.colorpreferences.get_color().to_string()
			self.configuration.setValue("viewer","viewerBackground",self.color)
			self.configuration.setValue("new","newDay",str(self.new))
		else:
			self.new = auxnew
			
		self.dialog.hide()
		return self.color
	
	def newcall(self, widget, day):
		""""""
		self.new = day


#	def changeLibraryFolder(self, widget=None):
#		print "Cambiando"

#		dialog = gtk.FileChooserDialog("Guardar como ",None,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
#		#~ dialog.set_current_name(namefile)
#		dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)

#		saveaction=False
#		response = dialog.run()
#		if response == gtk.RESPONSE_OK:
#			direccion=dialog.get_filename()
#			saveaction=True
#		dialog.destroy()

#		print direccion

