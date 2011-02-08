# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import os
import glob
import shutil
import webbrowser
import threading
gtk.gdk.threads_init()

import cons
import lib_submanga
import notifications
import downloader
import zipfile

class TreeDownload():
	""""""
	def __init__(self, config, visor):
		""""""
		self.configuration = config
		builder = config.builder
		self.directorio = cons.PATH_TEMP
		self.visor = visor
		
		#Get objects
		self.tvDownload = builder.get_object("tvDownload")
		self.menuDownload1 = builder.get_object("menuDownload1")
		self.menuDownload2 = builder.get_object("menuDownload2")
		self.menuDownload3 = builder.get_object("menuDownload3")
		guardarDownload = builder.get_object("guardarDownload")
		verDownload = builder.get_object("verDownload")
		continuarDownload = builder.get_object("continuarDownload")
		borrarDownload1 = builder.get_object("borrarDownload1")
		borrarDownload2 = builder.get_object("borrarDownload2")
		redescargarDownload1 = builder.get_object("redescargarDownload1")
		redescargarDownload2 = builder.get_object("redescargarDownload2")
		guardarzipDownload = builder.get_object("guardarzipDownload")
		guardarcbzDownload = builder.get_object("guardarcbzDownload")
		submangaDownload1 = builder.get_object("submangaDownload1")
		submangaDownload2 = builder.get_object("submangaDownload2")
		submangaDownload3 = builder.get_object("submangaDownload3")
		self.filechooserdialog = builder.get_object("filechooserdialog")
		
		#Get signals
		self.tvDownload.connect("button-press-event", self.button_clicked)
		guardarDownload.connect("activate", self.guardarBiblioteca)
		verDownload.connect("activate", self.abrirSeleccion)
		continuarDownload.connect("activate", self.continuarDescarga)
		borrarDownload1.connect("activate", self.borrarSeleccion)
		borrarDownload2.connect("activate", self.borrarSeleccion)
		redescargarDownload1.connect("activate", self.redescargarSeleccion)
		redescargarDownload2.connect("activate", self.redescargarSeleccion)
		guardarzipDownload.connect("activate", self.saveAs, "zip")
		guardarcbzDownload.connect("activate", self.saveAs, "cbz")
		submangaDownload1.connect("activate", self.abrirEnWeb)
		submangaDownload2.connect("activate", self.abrirEnWeb)
		submangaDownload3.connect("activate", self.abrirEnWeb)
		
		#Variables
		self.ok_icon = self.tvDownload.render_icon(gtk.STOCK_YES, gtk.ICON_SIZE_MENU)
		self.nofinish_icon = self.tvDownload.render_icon(gtk.STOCK_MEDIA_PAUSE, gtk.ICON_SIZE_MENU)
		self.down_icon = self.tvDownload.render_icon(gtk.STOCK_GO_DOWN, gtk.ICON_SIZE_MENU)
		
		#Localize
		self.tvDownload.get_column(1).set_title(_("Name"))
		self.tvDownload.get_column(2).set_title(_("Number"))
		self.tvDownload.get_column(3).set_title(_("Progress"))
		self.tvDownload.get_column(5).set_title(_("Images"))
		
		self.listar()

	def listar(self):
		""""""
		self.tvDownload.get_model().clear()
		for root,dirs,files in os.walk(self.directorio):
			for file in [f for f in files if f.lower().endswith("txt")]:
				img=len(glob.glob(root+"/*.jpg"))
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
				
				if img < int(imagenes):
					self.tvDownload.get_model().append([self.nofinish_icon, 2, nombre, int(numero), (img*100)/int(imagenes),
					                                   True, fansub, str(img)+"/"+imagenes, int(imagenes), int(codigo)])
				else:
					self.tvDownload.get_model().append([self.ok_icon, 1, nombre, int(numero), 100, True, fansub, imagenes,
					                                   int(imagenes), int(codigo)])
				
				f.close()
		self.tvDownload.grab_focus()


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
				treeselection = self.tvDownload.get_selection()
				model, iter = treeselection.get_selected()
				estado = model.get_value(iter, 0)
				if estado == self.ok_icon:
					self.menuDownload1.popup( None, None, None, event.button, time)
				elif estado == self.nofinish_icon:
					self.menuDownload2.popup( None, None, None, event.button, time)
				else:
					self.menuDownload3.popup( None, None, None, event.button, time)


	def borrarSeleccion(self, widget):
		""""""
		treeselection = self.tvDownload.get_selection()
		model, iter = treeselection.get_selected()
		text = str(model.get_value(iter, 9))
		directorio=self.directorio+text
		
		if os.path.exists(directorio):
			shutil.rmtree(directorio)
		
		self.deleteRow(iter)

	def abrirSeleccion(self, widget):
		""""""
		treeselection = self.tvDownload.get_selection()
		model, iter = treeselection.get_selected()
		estado = model.get_value(iter, 0)
		if estado == self.ok_icon:
			nombre = model.get_value(iter, 2)
			numero = str(model.get_value(iter, 3))
			codigo = str(model.get_value(iter, 9))
			fansub = model.get_value(iter, 6)
			numpaginas = str(model.get_value(iter, 8))

			manga=lib_submanga.Manga(nombre, numero, codigo, fansub, numpaginas)
			self.visor.open(False, manga, self.directorio)
	
	def guardarBiblioteca(self, widget):
		""""""
		treeselection = self.tvDownload.get_selection()
		model, iter = treeselection.get_selected()
		nombre = model.get_value(iter, 2)
		capitulo = str(model.get_value(iter, 3))
		fansub = model.get_value(iter, 6)
		imagenes = str(model.get_value(iter, 8))
		codigo = str(model.get_value(iter, 9))
		source=self.directorio+codigo
		destination=self.biblioteca.getPath()+codigo
		
		if os.path.exists(destination):
			shutil.rmtree(destination)
		if os.path.exists(source):
			shutil.move(source, destination)
		
		self.deleteRow(iter)
		self.biblioteca.addRow(nombre, capitulo, fansub, imagenes, codigo)
		
	def redescargarSeleccion(self, widget):
		""""""
		treeselection = self.tvDownload.get_selection()
		model, iter = treeselection.get_selected()
		nombre = model.get_value(iter, 2)
		capitulo = str(model.get_value(iter, 3))
		codigo = str(model.get_value(iter, 9))
		fansub = model.get_value(iter, 6)
		m=lib_submanga.Manga(nombre, capitulo, codigo, fansub)

		self.borrarSeleccion(widget)
		self.descargarManga(m)
		
	def continuarDescarga(self, widget):
		""""""
		treeselection = self.tvDownload.get_selection()
		model, iter = treeselection.get_selected()
		model.set_value(iter, 0, self.down_icon)
		model.set_value(iter, 1, 3)
		nombre = model.get_value(iter, 2)
		capitulo = str(model.get_value(iter, 3))
		codigo = str(model.get_value(iter, 9))
		fansub = model.get_value(iter, 6)
		m=lib_submanga.Manga(nombre, capitulo, codigo, fansub)

		iter = gtk.TreeRowReference(model, model.get_path(iter))
		self.descargarManga(m, iter, True)

	def descargarManga(self, manga, iter=-1, continuar=False):
		""""""
		descarga=downloader.Downloader(manga, self)
		task = threading.Thread(target=descarga.iniciarDescarga, args=(iter, continuar,))
		task.setDaemon(True)
		task.start()

	def addRow(self, nombre, numero, fansub, imagenes, codigo):
		""""""
		model=self.tvDownload.get_model()
		i=model.append([self.down_icon, 3, nombre, int(numero), 0, True, fansub, imagenes, int(imagenes), int(codigo)])
		return gtk.TreeRowReference(model, model.get_path(i))

	def deleteRow(self, a):
		""""""
		model=self.tvDownload.get_model()
		model.remove(a)

	def refreshProgress(self, iter, newProgress, numImg):
		""""""
		model=self.tvDownload.get_model()
		iter = model.get_iter(iter.get_path())
		model.set_value(iter, 4, newProgress)
		imageInfo = model.get_value(iter, 7)
		imageInfo = imageInfo.split('/')
		if len(imageInfo)==1:
			model.set_value(iter, 7, str(numImg)+"/"+imageInfo[0])
		else:
			model.set_value(iter, 7, str(numImg)+"/"+imageInfo[1])

		if newProgress == 100:
			model.set_value(iter, 0, self.ok_icon)
			model.set_value(iter, 1, 1)
			model.set_value(iter, 7, str(numImg))
			n=notifications.Notification()
			n.notify(_("Download complete"),_("Has finished downloading ")+model.get_value(iter, 2)+" "+
			         str(model.get_value(iter, 3)))


	def abrirEnWeb(self, widget):
		""""""
		treeselection = self.tvDownload.get_selection()
		model, iter = treeselection.get_selected()
		text = str(model.get_value(iter, 9))
		webbrowser.open("http://submanga.com/"+text)
	
	def setLibrary(self, biblioteca):
		""""""
		self.biblioteca = biblioteca


	def saveAs(self, widget, tipo):
		""""""
		treeselection = self.tvDownload.get_selection()
		model, iter = treeselection.get_selected()
		text = str(model.get_value(iter, 9))
		directorio=self.directorio+text
		name=model.get_value(iter, 2)
		num=str(model.get_value(iter, 3))
		name = name.replace(" ", "_")
		namefile=name+"_"+num+"."+tipo

		self.filechooserdialog.set_title(_("Save as .") + tipo)
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
