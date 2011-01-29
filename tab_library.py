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
import viewer_offline
import lib_submanga
import downloader
import zipfile

class TreeLibrary(gtk.ScrolledWindow):
	""""""
	def __init__(self, config):
		""""""
		self.configuration = config
		self.directorio = cons.PATH_LIBRARY

		gtk.ScrolledWindow.__init__(self)
		self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.tvLibrary = gtk.TreeView(gtk.TreeStore(int, str, str, str, str, str))
		self.tvLibrary.show()
		self.add(self.tvLibrary)

		#tree columns
		tree_nid = gtk.TreeViewColumn('#')
		nid_cell = gtk.CellRendererText()
		tree_nid.pack_start(nid_cell, True)
		tree_nid.add_attribute(nid_cell, 'text', 0)
		tree_nid.set_sort_column_id(0)
		self.tvLibrary.append_column(tree_nid)

		tree_name = gtk.TreeViewColumn('Nombre')
		tree_name.set_property('resizable', True)
		name_cell = gtk.CellRendererText()
		tree_name.pack_start(name_cell, False)
		tree_name.add_attribute(name_cell, 'text', 1)
		tree_name.set_sort_column_id(1)
		self.tvLibrary.append_column(tree_name)

		tree_chapter = gtk.TreeViewColumn('Número')
		tree_chapter.set_property('resizable', True)
		chapter_cell = gtk.CellRendererText()
		tree_chapter.pack_start(chapter_cell, False)
		tree_chapter.add_attribute(chapter_cell, 'text', 2)
		tree_chapter.set_sort_column_id(2)
		self.tvLibrary.append_column(tree_chapter)

		tree_fansub = gtk.TreeViewColumn('Fansub')
		tree_fansub.set_property('resizable', True)
		fansub_cell = gtk.CellRendererText()
		tree_fansub.pack_start(fansub_cell, True)
		tree_fansub.add_attribute(fansub_cell, 'text', 3)
		tree_fansub.set_sort_column_id(3)
		self.tvLibrary.append_column(tree_fansub)

		tree_imgnum = gtk.TreeViewColumn('Imágenes')
		tree_imgnum.set_property('resizable', True)
		imgnum_cell = gtk.CellRendererText()
		tree_imgnum.pack_start(imgnum_cell, True)
		tree_imgnum.add_attribute(imgnum_cell, 'text', 4)
		tree_imgnum.set_sort_column_id(4)
		self.tvLibrary.append_column(tree_imgnum)		
		
		tree_id = gtk.TreeViewColumn('ID Manga')
		id_cell = gtk.CellRendererText()
		tree_id.pack_start(id_cell, True)
		tree_id.add_attribute(id_cell, 'text', 5)
		tree_id.set_sort_column_id(5)
		self.tvLibrary.append_column(tree_id)

		self.tvLibrary.add_events(gtk.gdk.BUTTON_PRESS_MASK)
		self.tvLibrary.connect("button-press-event", self.button_clicked)

		self.show()
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
				
				self.tvLibrary.get_model().append(None, [index, nombre, numero, fansub, imagenes, codigo])
				f.close()
		self.tvLibrary.grab_focus()

	def button_clicked(self, widget, event):
		""""""
		if event.button == 1 and event.type == gtk.gdk._2BUTTON_PRESS:
			print "double click"
			print "Abrimos manga"
			self.abrirSeleccion()

		if event.button == 3:
			print "right click"
			boton = event.button # obtenemos el boton que se presiono
			pos = (event.x, event.y) # obtenemos las coordenadas
			tiempo = event.time # obtenemos el tiempo
			self.crear_menu_emergente(widget, boton, pos, tiempo)

	def crear_menu_emergente(self, widget, boton, pos, tiempo):
		""""""
		# un menu para agregar o eliminar directorios o archivos
		menu = gtk.Menu()
		# Items del menu
		
		ver = gtk.MenuItem("Ver capitulo")
		borrar = gtk.MenuItem("Borrar de la biblioteca")
		redescargar = gtk.MenuItem("Volver a descargar")
		saveas = gtk.MenuItem("Guardar como...")
		verWeb = gtk.MenuItem("Ver en submanga.com")

		# Agregar los items al menu
		#menu.append(ver)
		menu.append(ver)
		menu.append(borrar)
		menu.append(redescargar)
		menu.append(saveas)
		sep = gtk.SeparatorMenuItem()
		menu.append(sep)
		menu.append(verWeb)

		savemenu = gtk.Menu()
		saveaszip = gtk.MenuItem("Archivo .zip")
		saveascbz = gtk.MenuItem("Archivo .cbz")
		saveas.set_submenu(savemenu)

		savemenu.append(saveaszip)
		savemenu.append(saveascbz)

		# Se conectan las funciones de retrollamada a la senal "activate"
		#ver.connect_object("activate", self.seleccionar_origen, "Ver")
		ver.connect_object("activate", self.seleccionar_origen, "Ver")
		borrar.connect_object("activate", self.seleccionar_origen, "Borrar")
		redescargar.connect_object("activate", self.seleccionar_origen, "Redescargar")
		saveaszip.connect_object("activate", self.seleccionar_origen, "GuardarZIP")
		saveascbz.connect_object("activate", self.seleccionar_origen, "GuardarCBZ")
		verWeb.connect_object("activate", self.seleccionar_origen, "VerEnWeb")

		menu.show_all()
		menu.popup(None, None, None, boton, tiempo, None)

	def seleccionar_origen(self, accion):
		""""""
		if accion == "Ver":
			print "Abriendo..."
			self.abrirSeleccion()
		elif accion == "Borrar":
			print "Borrando"
			self.borrarSeleccion()
		elif accion == "Redescargar":
			print "Redescargando"
			self.redescargarSeleccion()
		elif accion == "GuardarZIP":
			print "GuardarZIP"
			self.saveAs("zip")
		elif accion == "GuardarCBZ":
			print "GuardarCBZ"
			self.saveAs("cbz")
		elif accion == "VerEnWeb":
			self.abrirEnWeb()


	def borrarSeleccion(self):
		""""""
		treeselection = self.tvLibrary.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 5)
		directorio=self.directorio+text
		
		if os.path.exists(directorio):
			shutil.rmtree(directorio)
		
		self.deleteRow(iter)

	def abrirSeleccion(self):
		""""""
		treeselection = self.tvLibrary.get_selection()
		model, iter = treeselection.get_selected()
		nombre = model.get_value(iter, 1)
		numero = model.get_value(iter, 2)
		codigo = model.get_value(iter, 5)
		fansub = model.get_value(iter, 3)
		numpaginas = model.get_value(iter, 4)
		npaginas=numpaginas.split("/")
		if len(npaginas)==2:
			numpaginas=npaginas[1]

		manga=lib_submanga.Manga(nombre, numero, codigo, fansub, numpaginas)
		viewer_offline.Visor(manga, self.configuration, self.directorio)

	def redescargarSeleccion(self):
		""""""
		treeselection = self.tvLibrary.get_selection()
		model, iter = treeselection.get_selected()
		nombre = model.get_value(iter, 1)
		capitulo = model.get_value(iter, 2)
		codigo = model.get_value(iter, 5)
		fansub = model.get_value(iter, 3)
		manga=lib_submanga.Manga(nombre, capitulo, codigo, fansub)

		self.borrarSeleccion()

		descarga=downloader.Downloader(manga, self)
		threading.Thread(target=descarga.iniciarDescarga, args=()).start()

	def deleteRow(self, a):
		""""""
		model=self.tvLibrary.get_model()
		model.remove(a)

	def abrirEnWeb(self):
		""""""
		treeselection = self.tvLibrary.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 5)
		webbrowser.open("http://submanga.com/"+text)
		
	def getPath(self):
		""""""
		return self.directorio

	def saveAs(self, tipo):
		""""""
		treeselection = self.tvLibrary.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 5)
		directorio=self.directorio+text
		name=model.get_value(iter, 1)
		num=model.get_value(iter, 2)
		namefile=name+"_"+num+"."+tipo

		dialog = gtk.FileChooserDialog("Guardar como ."+tipo,None,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE, gtk.RESPONSE_OK))
		dialog.set_current_name(namefile)

		saveaction=False
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			direccion=dialog.get_filename()
			saveaction=True
		dialog.destroy()

		if saveaction:
			if os.path.exists(directorio):
				file = zipfile.ZipFile(direccion, "w")
				for root,dirs,files in os.walk(directorio):
					for fich in [f for f in files if f.lower().endswith("jpg")]:
						name=directorio+"/"+fich
						file.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)
				file.close()
