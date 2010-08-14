#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import os
import webbrowser
import threading
gtk.gdk.threads_init()

import cons
import lib_submanga
import downloader
import viewer

import desc_dialog

class TreeSearch(gtk.VBox):
	""""""
	def __init__(self, biblioteca, config):
		""""""
		self.biblioteca=biblioteca
		self.configuration = config

		# Caja contenedor
		gtk.VBox.__init__(self, False, 5)

		frameUrl = gtk.Frame(" Obtener desde una dirección ")
		self.pack_start(frameUrl, False, True, 0)
		frameUrl.show()

		self.urlBar = gtk.HBox()
		frameUrl.add(self.urlBar)
		self.urlBar.show()

		textUrl = gtk.Label(" Dirección del manga ")
		self.urlBar.pack_start(textUrl, False, True, 0)
		textUrl.show ()

		entryUrl = gtk.Entry()
		self.urlBar.pack_start(entryUrl, False, True, 0)
		entryUrl.show()
		entryUrl.set_width_chars(40)
		entryUrl.connect("activate", self.getFromUrl)
		#entryUrl.set_text("http://submanga.com/Soul_Eater/76/82218")

		# Boton de busqueda
		buttonUrl = gtk.Button("Validar dirección")
		self.urlBar.pack_start(buttonUrl, False, False, 0)
		buttonUrl.show()
		buttonUrl.connect("clicked", self.getFromUrl)

		pixbufanim = gtk.gdk.PixbufAnimation(cons.PATH_MEDIA+"search-loader.gif")
		image = gtk.Image()
		image.set_from_animation(pixbufanim)
		self.urlBar.pack_start(image, False, False, 5)

		frameSearch = gtk.Frame(" Buscar ")
		self.pack_start(frameSearch, False, True, 0)
		frameSearch.show()

		self.searchBar = gtk.HBox()
		frameSearch.add(self.searchBar)
		self.searchBar.show()

		labelName = gtk.Label(" Nombre ")
		self.searchBar.pack_start(labelName, False, True, 0)
		labelName.show ()

		# Entrada de texto para el nombre del manga
		entryName = gtk.Entry()
		self.searchBar.pack_start(entryName, False, True, 0)
		entryName.show()
		entryName.connect("activate", self.getFromSearch)
		#entryName.set_text("Soul Eater")
		#

		labelChapter = gtk.Label(" Capítulo ")
		self.searchBar.pack_start(labelChapter, False, True, 0)
		labelChapter.show ()

		entryChapter = gtk.Entry()
		self.searchBar.pack_start(entryChapter, False, True, 0)
		entryChapter.set_width_chars(8)
		entryChapter.show()
		entryChapter.connect("activate", self.getFromSearch)
		#entryChapter.set_text("505")

		# Boton de busqueda
		buttonSearch = gtk.Button("Buscar")
		self.searchBar.pack_start(buttonSearch, False, False, 0)
		buttonSearch.show()
		buttonSearch.connect("clicked", self.getFromSearch)

		pixbufanim = gtk.gdk.PixbufAnimation(cons.PATH_MEDIA+"search-loader.gif")
		image = gtk.Image()
		image.set_from_animation(pixbufanim)
		self.searchBar.pack_start(image, False, False, 5)


		# Listado
		self.swSearch = gtk.ScrolledWindow()
		self.swSearch.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.tvSearch = gtk.TreeView(gtk.TreeStore(int, str, str, str, str))
		self.tvSearch.show()
		self.swSearch.add(self.tvSearch)

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


	def getFromUrl(self, widget):
		""""""
		gtk.gdk.threads_init()
		threading.Thread(target=self.listFromUrl, args=()).start()


	def listFromUrl(self):
		""""""
		self.urlBar.get_children()[3].show()
		gtk.gdk.threads_enter()
		url = self.urlBar.get_children()[1].get_text()

		self.resBusquedas=lib_submanga.Busqueda()
		self.resBusquedas.getFromDirect(url)

		m=self.resBusquedas.getManga(0)

		self.tvSearch.get_model().clear()
		self.tvSearch.get_model().append(None, [1,m.nombre, m.numero, m.fansub, m.codigo])
		gtk.gdk.threads_leave()
		self.urlBar.get_children()[3].hide()


	def getFromSearch(self,widget):
		""""""
		gtk.gdk.threads_init()
		threading.Thread(target=self.listFromSearch, args=()).start()


	def listFromSearch(self):
		""""""
		self.searchBar.get_children()[5].show()
		gtk.gdk.threads_enter()

		name = self.searchBar.get_children()[1].get_text()
		chapter = self.searchBar.get_children()[3].get_text()

		self.tvSearch.get_model().clear()
		self.resBusquedas=lib_submanga.Busqueda()
		self.resBusquedas.realizarBusqueda(name, chapter)

		numMangas=self.resBusquedas.numMangas()

		for i in range(numMangas):
			novManga=self.resBusquedas.getManga(i)
			self.tvSearch.get_model().append(None, [i+1,novManga.nombre, novManga.numero, novManga.fansub, novManga.codigo])

		gtk.gdk.threads_leave()
		self.searchBar.get_children()[5].hide()


	def button_clicked(self, widget, event):
		""""""
		if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
			treeselection = self.tvSearch.get_selection()
			model, iter = treeselection.get_selected()
			text = model.get_value(iter, 0)
			viewer.Visor(self.resBusquedas.getManga(text-1), self.configuration)

		if event.button == 3:
			print "second click"
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
		info = gtk.MenuItem("Información")
		verWeb = gtk.MenuItem("Ver en submanga.com")

		# Agregar los items al menu
		menu.append(ver)
		menu.append(descargar)
		sep = gtk.SeparatorMenuItem()
		menu.append(sep)
		menu.append(info)
		menu.append(verWeb)

		# Se conectan las funciones de retrollamada a la senal "activate"
		ver.connect_object("activate", self.seleccionar_origen, path, "Ver")
		descargar.connect_object("activate", self.seleccionar_origen, path, "Descargar")
		info.connect_object("activate", self.seleccionar_origen, path, "Info")
		verWeb.connect_object("activate", self.seleccionar_origen, path, "VerEnWeb")

		menu.show_all()
		menu.popup(None, None, None, boton, tiempo, None)

	def seleccionar_origen(self, path, accion):
		""""""
		# Recibe el path de la fila seleccionada en el modelo y la accion a realizar
		if accion == "Descargar":
			gtk.gdk.threads_init()
			threading.Thread(target=self.iniciarDescarga, args=()).start()
			# self.iniciarDescarga(self.manga)
		elif accion == "Ver":
			treeselection = self.tvSearch.get_selection()
			model, iter = treeselection.get_selected()
			text = model.get_value(iter, 0)
			viewer.Visor(self.resBusquedas.getManga(text-1), self.configuration)
		elif accion == "VerEnWeb":
			self.openInWebbrowser()
		elif accion == "Info":
			self.openInfoDialog()

		print "Seleccionado: ", path, accion

	def iniciarDescarga(self):
		""""""
		gtk.gdk.threads_enter()
		treeselection = self.tvSearch.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 0)
		manga=self.resBusquedas.getManga(text-1)
		descarga=downloader.Downloader(manga, self.biblioteca)
		descarga.iniciarDescarga()
		gtk.gdk.threads_leave()

	def openInWebbrowser(self):
		""""""
		treeselection = self.tvSearch.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 4)
		webbrowser.open("http://submanga.com/"+text)

	def openInfoDialog(self):
		""""""
		treeselection = self.tvSearch.get_selection()
		model, iter = treeselection.get_selected()
		text1 = model.get_value(iter, 1)
		text2 = model.get_value(iter, 2)
		text3 = model.get_value(iter, 4)
		m=lib_submanga.Manga(text1, text2, text3)

		desc_dialog.Info(m)
