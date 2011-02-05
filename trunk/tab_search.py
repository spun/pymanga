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

class TreeSearch():
	""""""
	def __init__(self, descargas, config, visor, desc_dialog):
		""""""
		self.descargas=descargas
		self.configuration = config
		builder = config.builder
		self.visor = visor
		self.desc_dialog = desc_dialog

		#Get objects
		self.tvSearch = builder.get_object("tvSearch")
		self.menuSearch = builder.get_object("menuSearch")
		verSearch = builder.get_object("verSearch")
		descargarSearch = builder.get_object("descargarSearch")
		infoSearch = builder.get_object("infoSearch")
		verWebSearch = builder.get_object("verWebSearch")
		self.entryUrl = builder.get_object("entryurl")
		self.buttonUrl = builder.get_object("buttonurl")
		self.imageUrl = builder.get_object("imageurl")
		self.entryName = builder.get_object("entryname")
		self.entryChapter = builder.get_object("entrychapter")
		self.buttonSearch = builder.get_object("buttonsearch")
		self.imageSearch = builder.get_object("imagesearch")
		
		#Get signals
		self.tvSearch.connect("button-press-event", self.button_clicked)
		verSearch.connect("activate", self.abrirSeleccion)
		descargarSearch.connect("activate", self.iniciarDescarga)
		infoSearch.connect("activate", self.openInfoDialog)
		verWebSearch.connect("activate", self.openInWebbrowser)
		self.entryUrl.connect("activate", self.getFromUrl)
		self.buttonUrl.connect("clicked", self.getFromUrl)
		self.entryName.connect("activate", self.getFromSearch)
		self.entryChapter.connect("activate", self.getFromSearch)
		self.buttonSearch.connect("clicked", self.getFromSearch)
		
		#Localize
		self.tvSearch.get_column(1).set_title(_("Name"))
		self.tvSearch.get_column(2).set_title(_("Number"))
		
		pixbufanim = gtk.gdk.PixbufAnimation(cons.PATH_MEDIA+"search-loader.gif")
		self.imageUrl.set_from_animation(pixbufanim)
		self.imageSearch.set_from_animation(pixbufanim)


	def getFromUrl(self, widget):
		""""""
		gtk.gdk.threads_init()
		threading.Thread(target=self.listFromUrl, args=()).start()


	def listFromUrl(self):
		""""""
		self.imageUrl.show()
		gtk.gdk.threads_enter()
		url = self.entryUrl.get_text()

		self.resBusquedas=lib_submanga.Busqueda()
		self.resBusquedas.getFromDirect(url)

		m=self.resBusquedas.getManga(0)

		self.tvSearch.get_model().clear()
		self.tvSearch.get_model().append(None, [1,m.nombre, m.numero, m.fansub, m.codigo])
		gtk.gdk.threads_leave()
		self.imageUrl.hide()


	def getFromSearch(self,widget):
		""""""
		gtk.gdk.threads_init()
		threading.Thread(target=self.listFromSearch, args=()).start()


	def listFromSearch(self):
		""""""
		self.imageSearch.show()
		gtk.gdk.threads_enter()

		name = self.entryName.get_text()
		chapter = self.entryChapter.get_text()

		self.tvSearch.get_model().clear()
		self.resBusquedas=lib_submanga.Busqueda()
		self.resBusquedas.realizarBusqueda(name, chapter)

		numMangas=self.resBusquedas.numMangas()

		for i in range(numMangas):
			novManga=self.resBusquedas.getManga(i)
			self.tvSearch.get_model().append([i+1,novManga.nombre, int(novManga.numero), novManga.fansub, int(novManga.codigo)])

		gtk.gdk.threads_leave()
		self.imageSearch.hide()


	def button_clicked(self, widget, event):
		""""""
		if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
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
				self.menuSearch.popup( None, None, None, event.button, time)


	def abrirSeleccion(self, widget):
		""""""
		treeselection = self.tvSearch.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 0)
		self.visor.open(True, self.resBusquedas.getManga(text-1))

	def iniciarDescarga(self):
		""""""
		#gtk.gdk.threads_enter()
		treeselection = self.tvSearch.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 0)
		manga=self.resBusquedas.getManga(text-1)
		descarga=downloader.Downloader(manga, self.descargas)
		#iter = self.descargas.getIter(manga.codigo)
		threading.Thread(target=descarga.iniciarDescarga, args=()).start()
		#descarga.iniciarDescarga()
		#gtk.gdk.threads_leave()

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

		self.desc_dialog.open(m)
