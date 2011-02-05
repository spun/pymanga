# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import threading
gtk.gdk.threads_init()

import lib_submanga
import viewer
import cons
import tab_library
import tab_new
import tab_featured
import tab_search
import tab_download
import viewer
from desc_dialog import Info
from preferences import Preferences

class Gui:
	""""""
	def __init__(self, conf):
		""""""
		#configuration
		self.configuration = conf
		builder = conf.builder

		#Get objects
		self.window = builder.get_object("MainWindow")
		exitmenu = builder.get_object("exitmenu")
		preferencesmenu = builder.get_object("preferencesmenu")
		aboutmenu = builder.get_object("aboutmenu")
		refreshbutton = builder.get_object("refreshbutton")
		self.aboutdialog = builder.get_object("aboutdialog")

		#Connect signals
		self.window.connect("delete-event", self.delete)
		exitmenu.connect("activate", self.delete)
		preferencesmenu.connect("activate", self.displayPreferences)
		aboutmenu.connect("activate", self.displayAbout)
		refreshbutton.connect("clicked", self.refresh_button)

		geometry=self.configuration.getValue("main","mainWindowGeometry")
		self.window.parse_geometry(geometry)
		
		self.preferences = Preferences(self.configuration)
		self.visor = viewer.Visor(self.configuration)
		desc_dialog = Info(self.configuration)
		self.biblioteca = tab_library.TreeLibrary(self.configuration, self.visor)
		self.descargas = tab_download.TreeDownload(self.biblioteca, self.configuration, self.visor)
		self.novedades = tab_new.TreeNew(self.descargas, self.configuration, self.visor, desc_dialog)
		busqueda = tab_search.TreeSearch(self.descargas, self.configuration, self.visor, desc_dialog)
		self.destacados = tab_featured.TreeFeatured(self.descargas, self.configuration, self.visor, desc_dialog)
		
		# Tab con el foco al iniciar
		tabSelected=self.configuration.getValue("main","mainTabSelected")
		self.notebook = builder.get_object("notebook")
		self.notebook.set_current_page(int(tabSelected))
		
		self.window.show()

		
	def refresh_button(self, widget):
		""""""
		page = self.notebook.get_current_page()
		# Si es la pagina de la biblioteca
		if page==0:
			self.biblioteca.listar()
		elif page==1:
			self.novedades.listar()
		elif page==2:
			self.destacados.listar()


	def displayPreferences(self, widget=None, event=None):
		""""""
		color = self.preferences.open()
		self.visor.set_background(color)
	
	def displayAbout(self, widget=None, event=None):
		""""""
		self.aboutdialog.run()
		self.aboutdialog.hide()
		
	def delete(self, widget, event=None):
		""""""
		gtk.main_quit()
		self.saveToQuit()

		return False		

	def saveToQuit(self):
		""""""
		x, y = self.window.get_position()
		allocation=self.window.allocation
		width = allocation.width
		height = allocation.height
		value=str(width)+"x"+str(height)+"+"+str(x)+"+"+str(y)
		self.configuration.setValue("main","mainWindowGeometry",value)

		tabSelected=self.notebook.get_current_page()
		self.configuration.setValue("main","mainTabSelected",str(tabSelected))

def main():
	gtk.main()
	return 0

if __name__ == "__main__":
	Gui()
	main()
