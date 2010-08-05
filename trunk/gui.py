#!/usr/bin/env python
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
import tab_search
from about import About
from preferences import Preferences

class Gui:
	""""""
	def delete(self, widget, event=None):
		""""""
		gtk.main_quit()
		self.saveToQuit()

		return False

	def get_main_menu(self, window):
		""""""
		accel_group = gtk.AccelGroup()
		item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
		item_factory.create_items(self.menu_items)
		window.add_accel_group(accel_group)
		self.item_factory = item_factory

		return item_factory.get_widget("<main>")

	def __init__(self, conf):
		""""""
		#configuration
		self.configuration = conf

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete)
		self.window.set_icon_from_file(cons.ICON_PROGRAM)
		self.window.set_title(cons.PROGRAM_NAME)
		self.window.set_border_width(0)

		geometry=self.configuration.getValue("main","mainWindowGeometry")
		self.window.parse_geometry(geometry)

		self.menu_items = (
			( "/_Archivo",         None,         None, 0, "<Branch>" ),
			#~ ( "/Archivo/_New",     "<control>N", self.print_hello, 0, None ),
			#~ ( "/Archivo/_Open",    "<control>O", self.print_hello, 0, None ),
			#~ ( "/Archivo/_Save",    "<control>S", self.print_hello, 0, None ),
			#~ ( "/Archivo/Save _As", None,         None, 0, None ),
			#~ ( "/Archivo/sep1",     None,         None, 0, "<Separator>" ),
			( "/Archivo/Quit",     "<control>Q", gtk.main_quit, 0, None ),
			( "/_Editar",      None,         None, 0, "<Branch>" ),
			( "/Editar/_Preferencias",  None,         Preferences, 0, None ),
			( "/Ay_uda",         None,         None, 0, "<LastBranch>" ),
			( "/Ayuda/Acerca de",   None,         About, 0, None ),
			)

		# Caja global
		vboxAdm = gtk.VBox()
		self.window.add(vboxAdm)
		vboxAdm.show()

		menubar = self.get_main_menu(self.window)
		vboxAdm.pack_start(menubar, False, True, 0)
		menubar.show()

		# Toolbar
		self.toolbar1 = gtk.Toolbar()
		self.toolbar1.show()
		vboxAdm.pack_start(self.toolbar1, False, False, 0)

		self.toolbar1.set_style(gtk.TOOLBAR_ICONS)
		self.toolbar1.get_icon_size()

		toolbutton3 = gtk.ToolButton(gtk.STOCK_REFRESH)

		toolbutton3.show()
		toolbutton3.set_property('can-focus', False)
		self.toolbar1.add (toolbutton3)

		toolbutton3.connect('clicked',  self.refresh_buttom)

		self.notebook = gtk.Notebook()
		self.notebook.set_property("homogeneous", True)
		self.notebook.set_tab_pos(gtk.POS_TOP)
		vboxAdm.pack_start(self.notebook, True, True, 0)
		self.notebook.show()

		# Tab de biblioteca
		self.biblioteca = tab_library.TreeLibrary()
		label = gtk.Label("Biblioteca")
		self.notebook.append_page(self.biblioteca, label)

		# Tab de novedades
		self.novedades = tab_new.TreeNews(self.biblioteca)
		label = gtk.Label("Novedades")
		self.notebook.append_page(self.novedades, label)

		# Tab de busquedas
		busqueda = tab_search.TreeSearch(self.biblioteca)
		label = gtk.Label("Buscar")
		self.notebook.append_page(busqueda, label)

		# Tab con el foco al iniciar
		tabSelected=self.configuration.getValue("main","mainTabSelected")
		self.notebook.set_current_page(int(tabSelected))

		# Barra de estado (completamente innecesaria)
		self.statusbar = gtk.Statusbar()
		self.context_id = self.statusbar.get_context_id("Users")
		vboxAdm.pack_end(self.statusbar, False, False, 0)
		self.statusbar.push(0, "Listo")
		self.statusbar.show()

		self.window.show()

	def refresh_buttom(self, widget):
		""""""
		page = self.notebook.get_current_page()
		# Si es la pagina de la biblioteca
		if page==0:
			self.biblioteca.listar()
		elif page==1:
			self.novedades.listar()

	def saveToQuit(self):
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
