#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import os
import threading
gtk.gdk.threads_init()

import cons
import lib_submanga
import downloader
import viewer

class TreeSearch(gtk.VBox):
	""""""
	def __init__(self, biblioteca):
		""""""
		self.biblioteca=biblioteca
		# Caja contenedor
		gtk.VBox.__init__(self, False, 5)
		frame_url = gtk.Frame(" Obtener desde una dirección ")
		self.pack_start(frame_url, False, True, 0)
		frame_url.show()

		url_bar = gtk.HBox()
		frame_url.add(url_bar)
		url_bar.show()

		text_url = gtk.Label(" Dirección del manga ")
		url_bar.pack_start(text_url, False, True, 0)
		text_url.show ()

		# Entrada de texto para el nombre del manga
		self.entry_url = gtk.Entry()
		url_bar.pack_start(self.entry_url, False, True, 0)
		self.entry_url.show()
		self.entry_url.set_width_chars(40)
		# self.entry_url.set_text("http://submanga.com/Soul_Eater/76/82218")

		# Boton de busqueda
		self.button_url = gtk.Button("Validar dirección")
		url_bar.pack_start(self.button_url, False, False, 0)
		self.button_url.show()
		self.button_url.connect("clicked", self.verDesdeUrl)

		frame_search = gtk.Frame(" Buscar ")
		self.pack_start(frame_search, False, True, 0)
		frame_search.show()

		# Caja horizontal para los campos de busqueda
		self.search_bar = gtk.HBox()
		frame_search.add(self.search_bar)
		self.search_bar.show()

		label1 = gtk.Label(" Nombre ")
		self.search_bar.pack_start(label1, False, True, 0)
		label1.show ()

		# Entrada de texto para el nombre del manga
		self.entry1 = gtk.Entry()
		self.search_bar.pack_start(self.entry1, False, True, 0)
		self.entry1.show()
		# self.entry1.set_text("Naruto")
		# entry1.connect("activate", self.change_manga, entry1, spinbutton1)

		label1 = gtk.Label(" Capitulo ")
		self.search_bar.pack_start(label1, False, True, 0)
		label1.show ()

		# Boton con incremento para el capitulo
		self.spinbutton1_adj = gtk.Adjustment(1.0, 1.0, 999.0, 1.0, 1.0, 0.0)
		self.spinbutton1 = gtk.SpinButton(self.spinbutton1_adj, 1, 0)
		self.search_bar.pack_start(self.spinbutton1, False, True, 0)
		self.spinbutton1.show()

		# Boton de busqueda
		self.button3 = gtk.Button("Buscar")
		self.search_bar.pack_start(self.button3, False, False, 0)
		self.button3.show()
		self.button3.connect("clicked", self.buscarManga)

		self.swSearch = gtk.ScrolledWindow()
		self.swSearch.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.tvSearch = gtk.TreeView(gtk.TreeStore(int, str, str, str, str))
		self.tvSearch.show()
		self.add(self.tvSearch)

		#tree columns
		tree_nid = gtk.TreeViewColumn('')
		nid_cell = gtk.CellRendererText()
		tree_nid.pack_start(nid_cell, True)
		tree_nid.add_attribute(nid_cell, 'text', 0)
		tree_nid.set_sort_column_id(0)
		self.tvSearch.append_column(tree_nid)

		tree_name = gtk.TreeViewColumn('Nombre')
		name_cell = gtk.CellRendererText()
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 1)
		tree_name.set_sort_column_id(1)
		self.tvSearch.append_column(tree_name)

		tree_chapter = gtk.TreeViewColumn('Número')
		chapter_cell = gtk.CellRendererText()
		tree_chapter.pack_start(chapter_cell, False)
		tree_chapter.add_attribute(chapter_cell, 'text', 2)
		tree_chapter.set_sort_column_id(2)
		self.tvSearch.append_column(tree_chapter)


		tree_fansub = gtk.TreeViewColumn('Fansub')
		fansub_cell = gtk.CellRendererText()
		tree_fansub.pack_start(fansub_cell, True)
		tree_fansub.add_attribute(fansub_cell, 'text', 3)
		tree_fansub.set_sort_column_id(3)
		self.tvSearch.append_column(tree_fansub)

		tree_id = gtk.TreeViewColumn('ID Manga')
		id_cell = gtk.CellRendererText()
		tree_id.pack_start(id_cell, True)
		tree_id.add_attribute(id_cell, 'text', 4)
		tree_id.set_sort_column_id(4)
		self.tvSearch.append_column(tree_id)


		self.tvSearch.add_events(gtk.gdk.BUTTON_PRESS_MASK)
		self.tvSearch.connect("button-press-event", self.button_clicked)

		self.swSearch.show()
		self.pack_start(self.swSearch, True, True, 0)
		self.show()

	def buscarManga(self,widget):
		""""""
		self.tvSearch.get_model().clear()
		entry_text = self.entry1.get_text()
		numcap=self.spinbutton1.get_value_as_int()
		numcap=str(numcap)
		print "Buscando "+entry_text+" "+numcap

		self.resBusquedas=lib_submanga.Busqueda(entry_text, numcap)
		self.resBusquedas.realizarBusqueda()
		self.manga=self.resBusquedas.getManga(0)

		self.tvSearch.get_model().append(None, [1,self.manga.nombre, self.manga.numero, self.manga.fansub, self.manga.codigo])

	def button_clicked(self, widget, event):
		""""""
		if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
			treeselection = self.tvSearch.get_selection()
			model, iter = treeselection.get_selected()
			text = model.get_value(iter, 0)
			viewer.Visor(self.manga)

		if event.button == 3:
			print "middle click"
			boton = event.button # obtenemos el boton que se presiono
			pos = (event.x, event.y) # obtenemos las coordenadas
			tiempo = event.time # obtenemos el tiempo
			# widget es TreeView (widget.get_name())
			# Obteniendo datos a partir de coordenadas de evento
			path, columna, xdefondo, ydefondo = widget.get_path_at_pos(event.x, event.y)
			# TreeView.get_path_at_pos(event.x, event.y) devuelve:
			# * La ruta de acceso en el punto especificado (x, y), en relacion con las coordenadas
			self.crear_menu_emergente(widget, boton, pos, tiempo, path)

	def crear_menu_emergente(self, widget, boton, pos, tiempo, path):
		""""""
		# un menu para agregar o eliminar directorios o archivos
		menu = gtk.Menu()
		# Items del menu
		ver = gtk.MenuItem("Ver sin descargar")
		descargar = gtk.MenuItem("Descargar")
		# Agregar los items al menu
		menu.append(ver)
		menu.append(descargar)
		# Se conectan las funciones de retrollamada a la senal "activate"
		ver.connect_object("activate", self.seleccionar_origen, path, "Ver")
		descargar.connect_object("activate", self.seleccionar_origen, path, "Descargar")
		menu.show_all()
		menu.popup(None, None, self.posicionar_menu, boton, tiempo, None)

	def seleccionar_origen(self, path, accion):
		""""""
		# Recibe el path de la fila seleccionada en el modelo y la accion a realizar
		if accion == "Descargar":
			gtk.gdk.threads_init()
			threading.Thread(target=self.iniciarDescarga, args=()).start()
			#~ self.iniciarDescarga(self.manga)
		elif accion == "Ver":
			treeselection = self.tvSearch.get_selection()
			model, iter = treeselection.get_selected()
			text = model.get_value(iter, 0)
			viewer.Visor(self.manga)
		print "Seleccionado: ", path, accion

	def posicionar_menu(self, widget, pos):
		""""""
		# Establece la posicion del menu desplegable
		print "Posicionando menu desplegable"

	def iniciarDescarga(self):
		""""""
		gtk.gdk.threads_enter()
		descarga=downloader.Downloader(self.manga, self.biblioteca)
		descarga.iniciarDescarga()
		gtk.gdk.threads_leave()

	def verDesdeUrl(self, widget):
		""""""
		entry_text = self.entry_url.get_text()
		print entry_text
		partes=entry_text.split('/')
		tam=len(partes)
		codigo=partes[tam-1]
		numero=partes[tam-2]
		nombre=partes[tam-3]

		m=lib_submanga.Manga(nombre, numero, codigo)
		m.getExtraInfo()
		self.manga=m

		self.tvSearch.get_model().clear()
		self.tvSearch.get_model().append(None, [1,self.manga.nombre, self.manga.numero, self.manga.fansub, self.manga.codigo])
