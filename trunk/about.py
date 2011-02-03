# -*- coding: utf-8 -*-

import sys
import pygtk
if not sys.platform == 'win32':
        pygtk.require('2.0')
import gtk

class About():
	""""""
	def __init__(self, config):
		""""""
		builder = config.builder
		
		self.aboutdialog = builder.get_object("aboutdialog")
		#LLamar a hide() en lugar de destroy() al cerrar la ventana
		self.aboutdialog.connect("response", self.aboutdialog.hide_on_delete)
		
	def open(self):
		""""""
		self.aboutdialog.run()
