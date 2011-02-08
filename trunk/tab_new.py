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

class TreeNew():
	""""""
	def __init__(self, descargas, config, visor, desc_dialog):
		""""""
		self.descargas=descargas
		self.configuration = config
		builder = config.builder
		self.visor = visor
		self.desc_dialog = desc_dialog

		#Get objects
		self.tvNew = builder.get_object("tvNew")
		self.menuNew = builder.get_object("menuNew")
		verNew = builder.get_object("verNew")
		descargarNew = builder.get_object("descargarNew")
		infoNew = builder.get_object("infoNew")
		verWebNew = builder.get_object("verWebNew")
		
		#Get signals
		self.tvNew.connect("button-press-event", self.button_clicked)
		verNew.connect("activate", self.abrirSeleccion)
		descargarNew.connect("activate", self.descargarSeleccion)
		infoNew.connect("activate", self.openInfoDialog)
		verWebNew.connect("activate", self.abrirEnWeb)
		
		#Localize
		self.tvNew.get_column(1).set_title(_("Name"))
		self.tvNew.get_column(2).set_title(_("Number"))
		self.tvNew.get_column(4).set_title(_("Date"))

		#self.listar()

	def listar(self):
		""""""
		gtk.gdk.threads_init()
		list = threading.Thread(target=self.actualizarNovedades, args=())
		list.setDaemon(True)
		list.start()

	def actualizarNovedades(self):
		""""""
		self.tvNew.get_model().clear()
		#context_id = self.statusbar.get_context_id("Estado de actualizacion de novedades")
		gtk.gdk.threads_enter()
		#self.statusbar.push(0, " Actualizando novedades... Espere por favor")
		#self.vaciar_lista()
		#time.sleep(5)
		self.novedades = lib_submanga.Novedades()
		numDias=int(self.configuration.getValue("new","newDay"))
		self.novedades.realizarBusqueda(numDias)

		for i in range(self.novedades.numMangas()):
			novManga=self.novedades.getManga(i)
			self.tvNew.get_model().append([i+1, novManga.nombre, int(novManga.numero), novManga.fansub,novManga.fecha, int(novManga.codigo)])
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
				self.menuNew.popup( None, None, None, event.button, time)


	def abrirSeleccion(self, widget):
		""""""
		treeselection = self.tvNew.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 0)
		manga=self.novedades.getManga(text-1)
		self.visor.open(True, manga)

	def descargarSeleccion(self, widget):
		""""""
		#gtk.gdk.threads_enter()
		treeselection = self.tvNew.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 0)

		manga=self.novedades.getManga(text-1)

		descarga=downloader.Downloader(manga, self.descargas)
		task = threading.Thread(target=descarga.iniciarDescarga, args=())
		task.setDaemon(True)
		task.start()
		#descarga.iniciarDescarga()
		#gtk.gdk.threads_leave()

	def abrirEnWeb(self, widget):
		""""""
		treeselection = self.tvNew.get_selection()
		model, iter = treeselection.get_selected()
		text = str(model.get_value(iter, 5))
		webbrowser.open("http://submanga.com/"+text)

	def openInfoDialog(self, widget):
		""""""
		treeselection = self.tvNew.get_selection()
		model, iter = treeselection.get_selected()
		text1 = model.get_value(iter, 1)
		text2 = str(model.get_value(iter, 2))
		text3 = str(model.get_value(iter, 5))
		m=lib_submanga.Manga(text1, text2, text3)

		self.desc_dialog.open(m)




