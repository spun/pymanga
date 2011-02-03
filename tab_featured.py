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

class TreeFeatured():
	""""""
	def __init__(self, descargas, config, visor, desc_dialog):
		""""""
		self.descargas=descargas
		self.configuration = config
		builder = config.builder
		self.visor = visor
		self.desc_dialog = desc_dialog

		#Get objects
		self.tvFeatured = builder.get_object("tvFeatured")
		self.menuFeatured = builder.get_object("menuFeatured")
		verFeatured = builder.get_object("verFeatured")
		descargarFeatured = builder.get_object("descargarFeatured")
		infoFeatured = builder.get_object("infoFeatured")
		verWebFeatured = builder.get_object("verWebFeatured")
		
		#Get signals
		self.tvFeatured.connect("button-press-event", self.button_clicked)
		verFeatured.connect("activate", self.abrirSeleccion)
		descargarFeatured.connect("activate", self.descargarSeleccion)
		infoFeatured.connect("activate", self.openInfoDialog)
		verWebFeatured.connect("activate", self.abrirEnWeb)

		#self.listar()

	def listar(self):
		""""""
		gtk.gdk.threads_init()
		threading.Thread(target=self.actualizarDestacados, args=()).start()

	def actualizarDestacados(self):
		""""""
		self.tvFeatured.get_model().clear()
		#context_id = self.statusbar.get_context_id("Estado de actualizacion de destacados")
		#self.statusbar.push(context_id, "Actualizando destacados...")
		gtk.gdk.threads_enter()
		#self.vaciar_lista()
		#time.sleep(5)
		self.destacados = lib_submanga.Destacados()
		self.destacados.realizarBusqueda()
		
		for i in range(self.destacados.numMangas()):
			novManga=self.destacados.getManga(i)
			self.tvFeatured.get_model().append([i+1,novManga.nombre, int(novManga.numero), novManga.fansub, int(novManga.codigo)])
		gtk.gdk.threads_leave()

	def button_clicked(self, widget, event):
		""""""
		if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
			print "double click"
			self.abrirSeleccion(widget)

		if event.button == 3:
			x = int(event.x)
			y = int(event.y)
			time = event.time
			pthinfo = widget.get_path_at_pos(x, y)
			if pthinfo is not None:
				path, col, cellx, celly = pthinfo
				widget.grab_focus()
				widget.set_cursor( path, col, 0)
				self.menuFeatured.popup( None, None, None, event.button, time)


	def abrirSeleccion(self, widget):
		""""""
		treeselection = self.tvFeatured.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 0)
		manga=self.destacados.getManga(text-1)
		self.visor.open(True, manga)

	def descargarSeleccion(self, widget):
		""""""
		#gtk.gdk.threads_enter()
		treeselection = self.tvFeatured.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 0)
		
		manga=self.destacados.getManga(text-1)
		
		descarga=downloader.Downloader(manga, self.descargas)
		#iter = self.descargas.getIter(manga.codigo)
		threading.Thread(target=descarga.iniciarDescarga, args=()).start()
		#descarga.iniciarDescarga()
		#gtk.gdk.threads_leave()

	def abrirEnWeb(self, widget):
		""""""
		treeselection = self.tvFeatured.get_selection()
		model, iter = treeselection.get_selected()
		text = str(model.get_value(iter, 4))
		webbrowser.open("http://submanga.com/"+text)

	def openInfoDialog(self, widget):
		""""""
		treeselection = self.tvFeatured.get_selection()
		model, iter = treeselection.get_selected()
		text1 = model.get_value(iter, 1)
		text2 = str(model.get_value(iter, 2))
		text3 = str(model.get_value(iter, 4))
		m=lib_submanga.Manga(text1, text2, text3)

		self.desc_dialog.open(m)

