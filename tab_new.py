#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import threading
import webbrowser
gtk.gdk.threads_init()

import cons
import lib_submanga
import downloader
import viewer

class TreeNews(gtk.ScrolledWindow):
	""""""
	def __init__(self, biblioteca):
		""""""
		self.biblioteca=biblioteca

		gtk.ScrolledWindow.__init__(self)
		self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.tvNovedades = gtk.TreeView(gtk.TreeStore(int, str, str, str, str))
		self.tvNovedades.show()
		self.add(self.tvNovedades)

		#tree columns
		tree_nid = gtk.TreeViewColumn('')
		nid_cell = gtk.CellRendererText()
		tree_nid.pack_start(nid_cell, True)
		tree_nid.add_attribute(nid_cell, 'text', 0)
		tree_nid.set_sort_column_id(0)
		self.tvNovedades.append_column(tree_nid)

		tree_name = gtk.TreeViewColumn('Nombre')
		name_cell = gtk.CellRendererText()
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 1)
		tree_name.set_sort_column_id(1)
		self.tvNovedades.append_column(tree_name)

		tree_chapter = gtk.TreeViewColumn('Número')
		chapter_cell = gtk.CellRendererText()
		tree_chapter.pack_start(chapter_cell, False)
		tree_chapter.add_attribute(chapter_cell, 'text', 2)
		tree_chapter.set_sort_column_id(2)
		self.tvNovedades.append_column(tree_chapter)

		tree_fansub = gtk.TreeViewColumn('Fansub')
		fansub_cell = gtk.CellRendererText()
		tree_fansub.pack_start(fansub_cell, True)
		tree_fansub.add_attribute(fansub_cell, 'text', 3)
		tree_fansub.set_sort_column_id(3)
		self.tvNovedades.append_column(tree_fansub)

		tree_id = gtk.TreeViewColumn('ID Manga')
		id_cell = gtk.CellRendererText()
		tree_id.pack_start(id_cell, True)
		tree_id.add_attribute(id_cell, 'text', 4)
		tree_id.set_sort_column_id(4)
		self.tvNovedades.append_column(tree_id)

		self.tvNovedades.add_events(gtk.gdk.BUTTON_PRESS_MASK)
		self.tvNovedades.connect("button-press-event", self.button_clicked)

		self.show()
		self.listar()

	def listar(self):
		""""""
		gtk.gdk.threads_init()
		threading.Thread(target=self.actualizarNovedades, args=()).start()

	def actualizarNovedades(self):
		""""""
		self.tvNovedades.get_model().clear()
		#context_id = self.statusbar.get_context_id("Estado de actualizacion de novedades")
		#self.statusbar.push(context_id, "Actualizando novedades...")
		gtk.gdk.threads_enter()
		#self.vaciar_lista()
		#time.sleep(5)
		self.novedades = lib_submanga.Novedades()
		numMangas=10
		self.novedades.realizarBusqueda(numMangas)

		for i in range(numMangas):
			novManga=self.novedades.getManga(i)
			self.tvNovedades.get_model().append(None, [i+1,novManga.nombre, novManga.numero, novManga.fansub, novManga.codigo])
		gtk.gdk.threads_leave()

	def button_clicked(self, widget, event):
		""""""
		if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
			print "double click"
			self.abrirSeleccion()

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
		verWeb = gtk.MenuItem("Ver en submanga.com")

		# Agregar los items al menu
		menu.append(ver)
		menu.append(descargar)
		sep = gtk.SeparatorMenuItem()
		menu.append(sep)
		menu.append(verWeb)
		# Se conectan las funciones de retrollamada a la senal "activate"
		ver.connect_object("activate", self.seleccionar_origen, path, "Ver")
		descargar.connect_object("activate", self.seleccionar_origen, path, "Descargar")
		verWeb.connect_object("activate", self.seleccionar_origen, path, "VerEnWeb")
		menu.show_all()
		menu.popup(None, None, None, boton, tiempo, None)

	def seleccionar_origen(self, path, accion):
		""""""
		# Recibe el path de la fila seleccionada en el modelo y la accion a realizar
		if accion == "Ver":
			self.abrirSeleccion()
		elif accion == "Descargar":
			gtk.gdk.threads_init()
			threading.Thread(target=self.descargarSeleccion, args=()).start()
			#~ self.iniciarDescarga(self.manga)
		elif accion == "VerEnWeb":
			self.abrirEnWeb()
		print "Seleccionado: ", path, accion



	def abrirSeleccion(self):
		""""""
		treeselection = self.tvNovedades.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 0)
		manga=self.novedades.getManga(text-1)
		viewer.Visor(manga)

	def descargarSeleccion(self):
		""""""
		treeselection = self.tvNovedades.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 0)

		manga=self.novedades.getManga(text-1)

		gtk.gdk.threads_enter()
		descarga=downloader.Downloader(manga, self.biblioteca)
		descarga.iniciarDescarga()
		gtk.gdk.threads_leave()

	def abrirEnWeb(self):
		""""""
		treeselection = self.tvNovedades.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 4)
		webbrowser.open("http://submanga.com/"+text)
