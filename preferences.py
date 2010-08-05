#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk

import cons

class Preferences(gtk.Dialog):
	""""""
	def __init__(self, widget=None, event=None):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon_from_file(cons.PREFERENCES_ICON)
		self.connect("response", self.close)
		self.set_size_request(500,500)
		self.set_title(cons.PROGRAM_NAME+" - Preferencias ")
		frame1 = gtk.Frame(" Dirección de la biblioteca ")
		frame1.set_border_width(10)
		self.vbox.pack_start(frame1, False, True, 0)
		frame1.show()

		hbox = gtk.HBox()
		hbox.set_border_width(10)
		frame1.add(hbox)
		hbox.show()

		label1 = gtk.Label(cons.PATH_LIBRARY)
		hbox.pack_start(label1, False, True, 0)
		label1.show()

		hbbox = gtk.HButtonBox()
		hbbox.set_layout(gtk.BUTTONBOX_END)
		hbox.pack_start(hbbox, True, True, 10)
		hbbox.show()

		button = gtk.Button("Cambiar")
		button.connect("clicked", self.changeLibraryFolder)
		hbbox.pack_start(button)
		button.show()

		cancel_button = gtk.Button(None, gtk.STOCK_CANCEL)
		save_button = gtk.Button(None, gtk.STOCK_SAVE)
		self.action_area.pack_start(cancel_button)
		cancel_button.show()
		self.action_area.pack_start(save_button)
		save_button.show()
		cancel_button.connect("clicked", self.close)
		save_button.connect("clicked", self.close)

		self.show()

	def close(self, widget=None, other=None):
		""""""
		self.destroy()
		
		
		
		
	def changeLibraryFolder(self, widget=None):
		print "Cambiando"

		dialog = gtk.FileChooserDialog("Guardar como ",None,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
		#~ dialog.set_current_name(namefile)
		dialog.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)

		saveaction=False
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			direccion=dialog.get_filename()
			saveaction=True
		dialog.destroy()
		
		print direccion


if __name__ == "__main__":
	p = Preferences()
	gtk.main()
