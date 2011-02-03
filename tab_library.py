# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import os
import shutil
import webbrowser
import threading
gtk.gdk.threads_init()

import cons
import lib_submanga
import downloader
import zipfile

class TreeLibrary():
	""""""
	def __init__(self, config, visor):
		""""""
		self.configuration = config
		builder = config.builder
		self.directorio = cons.PATH_LIBRARY
		self.visor = visor
		
		#Get objects
		self.tvLibrary = builder.get_object("tvLibrary")
		self.menuLibrary = builder.get_object("menuLibrary")
		verLibrary = builder.get_object("verLibrary")
		borrarLibrary = builder.get_object("borrarLibrary")
		redescargarLibrary = builder.get_object("redescargarLibrary")
		guardarzipLibrary = builder.get_object("guardarzipLibrary")
		guardarcbzLibrary = builder.get_object("guardarcbzLibrary")
		submangaLibrary = builder.get_object("submangaLibrary")
		self.filechooserdialog = builder.get_object("filechooserdialog")
		
		#Get signals
		self.tvLibrary.connect("button-press-event", self.button_clicked)
		verLibrary.connect("activate", self.abrirSeleccion)
		borrarLibrary.connect("activate", self.borrarSeleccion)
		redescargarLibrary.connect("activate", self.redescargarSeleccion)
		guardarzipLibrary.connect("activate", self.saveAs, "zip")
		guardarcbzLibrary.connect("activate", self.saveAs, "cbz")
		submangaLibrary.connect("activate", self.abrirEnWeb)

		self.listar()

	def listar(self):
		""""""
		index=0
		self.tvLibrary.get_model().clear()
		for root,dirs,files in os.walk(self.directorio):
			for file in [f for f in files if f.lower().endswith("txt")]:
				index=index+1
				fichero= os.path.join(root, file)
				f = open(fichero)
				nombre = f.readline()
				nombre=nombre.replace("\n","")
				numero = f.readline()
				numero=numero.replace("\n","")
				codigo = f.readline()
				codigo=codigo.replace("\n","")
				fansub = f.readline()
				fansub=fansub.replace("\n","")
				imagenes = f.readline()
				imagenes=imagenes.replace("\n","")
				
				self.tvLibrary.get_model().append([index, nombre, int(numero), fansub, int(imagenes), int(codigo)])

				f.close()
		self.tvLibrary.grab_focus()

	def button_clicked(self, widget, event):
		""""""
		if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
			print "double click"
			print "Abrimos manga"
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
				self.menuLibrary.popup( None, None, None, event.button, time)


	def borrarSeleccion(self, widget):
		""""""
		treeselection = self.tvLibrary.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 5)
		directorio=self.directorio+text
		
		if os.path.exists(directorio):
			shutil.rmtree(directorio)
		
		self.deleteRow(iter)

	def abrirSeleccion(self, widget):
		""""""
		treeselection = self.tvLibrary.get_selection()
		model, iter = treeselection.get_selected()
		nombre = model.get_value(iter, 1)
		numero = str(model.get_value(iter, 2))
		codigo = str(model.get_value(iter, 5))
		fansub = model.get_value(iter, 3)
		numpaginas = str(model.get_value(iter, 4))
		npaginas=numpaginas.split("/")
		if len(npaginas)==2:
			numpaginas=npaginas[1]

		manga=lib_submanga.Manga(nombre, numero, codigo, fansub, numpaginas)
		self.visor.open(False, manga, self.directorio)

	def redescargarSeleccion(self, widget):
		""""""
		treeselection = self.tvLibrary.get_selection()
		model, iter = treeselection.get_selected()
		nombre = model.get_value(iter, 1)
		capitulo = str(model.get_value(iter, 2))
		codigo = str(model.get_value(iter, 5))
		fansub = model.get_value(iter, 3)
		manga=lib_submanga.Manga(nombre, capitulo, codigo, fansub)

		self.borrarSeleccion()

		descarga=downloader.Downloader(manga, self)
		threading.Thread(target=descarga.iniciarDescarga, args=()).start()

	def deleteRow(self, a):
		""""""
		model=self.tvLibrary.get_model()
		model.remove(a)

	def abrirEnWeb(self, widget):
		""""""
		print widget
		treeselection = self.tvLibrary.get_selection()
		model, iter = treeselection.get_selected()
		text = str(model.get_value(iter, 5))
		webbrowser.open("http://submanga.com/"+text)
		
	def getPath(self):
		""""""
		return self.directorio

	def saveAs(self, widget, tipo):
		""""""
		treeselection = self.tvLibrary.get_selection()
		model, iter = treeselection.get_selected()
		text = str(model.get_value(iter, 5))
		directorio=self.directorio+text
		name=model.get_value(iter, 1)
		num=str(model.get_value(iter, 2))
		namefile=name+"_"+num+"."+tipo

		self.filechooserdialog.set_title("Guardar como ." + tipo)
		self.filechooserdialog.set_current_name(namefile)

		response = self.filechooserdialog.run()
		if response == 1:
			direccion=self.filechooserdialog.get_filename()
			if os.path.exists(directorio):
				file = zipfile.ZipFile(direccion, "w")
				for root,dirs,files in os.walk(directorio):
					for fich in [f for f in files if f.lower().endswith("jpg")]:
						name=directorio+"/"+fich
						file.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)
				file.close()
		
		self.filechooserdialog.hide()
