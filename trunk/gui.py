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
import tab_featured
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

	def get_bar_menu(self):
		""""""
		menubar = gtk.MenuBar()
		menubar.show()

		filemenu = gtk.Menu()
		filemenu.show()
		filem = gtk.MenuItem("_Archivo")
		filem.set_submenu(filemenu)
		filem.show()
		exitmenu = gtk.MenuItem("Salir")
		exitmenu.show()
		exitmenu.connect("activate", gtk.main_quit)
		filemenu.append(exitmenu)
		menubar.append(filem)

		editmenu = gtk.Menu()
		editmenu.show()
		editm = gtk.MenuItem("Editar")
		editm.set_submenu(editmenu)
		editm.show()
		preferencesmenu = gtk.MenuItem("Preferencias")
		preferencesmenu.show()
		preferencesmenu.connect("activate", self.displayPreferences)
		editmenu.append(preferencesmenu)
		menubar.append(editm)

		helpmenu = gtk.Menu()
		helpmenu.show()
		helpm = gtk.MenuItem("Ayuda")
		helpm.set_submenu(helpmenu)
		helpm.show()
		aboutmenu = gtk.MenuItem("Acerca de")
		aboutmenu.show()
		aboutmenu.connect("activate", About)
		helpmenu.append(aboutmenu)
		menubar.append(helpm)

		return menubar

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


		# Caja global
		vboxAdm = gtk.VBox()
		self.window.add(vboxAdm)
		vboxAdm.show()

		# Barra de menus
		menubar = self.get_bar_menu()
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
		self.biblioteca = tab_library.TreeLibrary(self.configuration)
		label = gtk.Label("Biblioteca")
		self.notebook.append_page(self.biblioteca, label)

		# Tab de novedades
		self.novedades = tab_new.TreeNews(self.biblioteca, self.configuration)
		label = gtk.Label("Novedades")
		self.notebook.append_page(self.novedades, label)
		
		# Tab de destacados
		self.destacados = tab_featured.TreeNews(self.biblioteca, self.configuration)
		label = gtk.Label("Destacados")
		self.notebook.append_page(self.destacados, label)

		# Tab de busquedas
		busqueda = tab_search.TreeSearch(self.biblioteca, self.configuration)
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


	def displayPreferences(self, widget=None, event=None):
		""""""
		Preferences(self.configuration)

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
