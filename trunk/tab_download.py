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
import viewer_offline
import lib_submanga
import notifications
import downloader
import zipfile

class TreeDownload(gtk.ScrolledWindow):
	""""""
	def __init__(self, biblioteca, config):
		""""""
		self.biblioteca=biblioteca
		self.configuration = config
		self.directorio = cons.PATH_TEMP

		gtk.ScrolledWindow.__init__(self)
		self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.tvDownload = gtk.TreeView(gtk.TreeStore(gtk.gdk.Pixbuf, str, str, int, bool, str, str, str))
		self.tvDownload.show()
		self.add(self.tvDownload)

		#tree columns
		tree_icon = gtk.TreeViewColumn('')
		icon_cell = gtk.CellRendererPixbuf()
		tree_icon.pack_start(icon_cell, False)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.tvDownload.append_column(tree_icon)

		tree_name = gtk.TreeViewColumn('Nombre')
		tree_name.set_property('resizable', True)
		name_cell = gtk.CellRendererText()
		tree_name.pack_start(name_cell, False)
		tree_name.add_attribute(name_cell, 'text', 1)
		tree_name.set_sort_column_id(1)
		self.tvDownload.append_column(tree_name)

		tree_chapter = gtk.TreeViewColumn('Número')
		tree_chapter.set_property('resizable', True)
		chapter_cell = gtk.CellRendererText()
		tree_chapter.pack_start(chapter_cell, False)
		tree_chapter.add_attribute(chapter_cell, 'text', 2)
		tree_chapter.set_sort_column_id(2)
		self.tvDownload.append_column(tree_chapter)

		tree_progress = gtk.TreeViewColumn('Progreso')
		tree_progress.set_property('resizable', True)
		tree_progress.set_min_width(150)
		progress_cell = gtk.CellRendererProgress()
		tree_progress.pack_start(progress_cell, True)
		tree_progress.add_attribute(progress_cell, 'value', 3)
		tree_progress.add_attribute(progress_cell, 'visible', 4)
		tree_progress.set_sort_column_id(3)
		self.tvDownload.append_column(tree_progress)

		tree_fansub = gtk.TreeViewColumn('Fansub')
		tree_fansub.set_property('resizable', True)
		fansub_cell = gtk.CellRendererText()
		tree_fansub.pack_start(fansub_cell, True)
		tree_fansub.add_attribute(fansub_cell, 'text', 5)
		tree_fansub.set_sort_column_id(5)
		self.tvDownload.append_column(tree_fansub)

		tree_imgnum = gtk.TreeViewColumn('Imágenes')
		tree_imgnum.set_property('resizable', True)
		imgnum_cell = gtk.CellRendererText()
		tree_imgnum.pack_start(imgnum_cell, True)
		tree_imgnum.add_attribute(imgnum_cell, 'text', 6)
		tree_imgnum.set_sort_column_id(6)
		self.tvDownload.append_column(tree_imgnum)		
		
		tree_id = gtk.TreeViewColumn('ID Manga')
		id_cell = gtk.CellRendererText()
		tree_id.pack_start(id_cell, True)
		tree_id.add_attribute(id_cell, 'text', 7)
		tree_id.set_sort_column_id(7)
		self.tvDownload.append_column(tree_id)

		self.tvDownload.add_events(gtk.gdk.BUTTON_PRESS_MASK)
		self.tvDownload.connect("button-press-event", self.button_clicked)

		self.ok_icon = self.tvDownload.render_icon(gtk.STOCK_YES, gtk.ICON_SIZE_MENU)
		self.nofinish_icon = self.tvDownload.render_icon(gtk.STOCK_NO, gtk.ICON_SIZE_MENU)
		self.down_icon = self.tvDownload.render_icon(gtk.STOCK_GO_DOWN, gtk.ICON_SIZE_MENU)
		self.show()
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
					self.tvDownload.get_model().append(None, [self.nofinish_icon, nombre, numero, (img*100)/int(imagenes),
					                                   True, fansub, str(img)+"/"+imagenes, codigo])
				else:
					self.tvDownload.get_model().append(None, [self.ok_icon, nombre, numero, 100, True, fansub, imagenes, codigo])
				f.close()
		self.tvDownload.grab_focus()


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
		guardar = gtk.MenuItem("Guardar en Biblioteca")
		continuar = gtk.MenuItem("Continuar descarga")
		borrar = gtk.MenuItem("Borrar del disco")
		redescargar = gtk.MenuItem("Volver a descargar")
		saveas = gtk.MenuItem("Guardar como...")
		verWeb = gtk.MenuItem("Ver en submanga.com")

		# Agregar los items al menu
		menu.append(ver)
		menu.append(guardar)
		menu.append(continuar)
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
		ver.connect_object("activate", self.seleccionar_origen, "Ver")
		guardar.connect_object("activate", self.seleccionar_origen, "Guardar")
		continuar.connect_object("activate", self.seleccionar_origen, "Continuar")
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
		elif accion == "Continuar":
			print "Continuando descarga..."
			self.continuarDescarga()
		elif accion == "Guardar":
			print "Guardado en la biblioteca"
			self.guardarBiblioteca()
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
		treeselection = self.tvDownload.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 7)
		directorio=self.directorio+text
		
		if os.path.exists(directorio):
			shutil.rmtree(directorio)
		
		self.deleteRow(iter)

	def abrirSeleccion(self):
		""""""
		treeselection = self.tvDownload.get_selection()
		model, iter = treeselection.get_selected()
		estado = model.get_value(iter, 0)
		if estado == self.ok_icon:
			nombre = model.get_value(iter, 1)
			numero = model.get_value(iter, 2)
			codigo = model.get_value(iter, 7)
			fansub = model.get_value(iter, 5)
			numpaginas = model.get_value(iter, 6)
			npaginas=numpaginas.split("/")
			if len(npaginas)==2:
				numpaginas=npaginas[1]

			manga=lib_submanga.Manga(nombre, numero, codigo, fansub, numpaginas)
			viewer_offline.Visor(manga, self.configuration, self.directorio)
	
	def guardarBiblioteca(self):
		""""""
		treeselection = self.tvDownload.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 7)
		source=self.directorio+text
		destination=self.biblioteca.getPath()+text
		
		if os.path.exists(destination):
			shutil.rmtree(destination)
		if os.path.exists(source):
			shutil.move(source, destination)
		
		self.deleteRow(iter)
		self.biblioteca.listar()
		
	def redescargarSeleccion(self):
		""""""
		treeselection = self.tvDownload.get_selection()
		model, iter = treeselection.get_selected()
		nombre = model.get_value(iter, 1)
		capitulo = model.get_value(iter, 2)
		codigo = model.get_value(iter, 7)
		fansub = model.get_value(iter, 5)
		m=lib_submanga.Manga(nombre, capitulo, codigo, fansub)

		#self.borrarSeleccion()
		self.descargarManga(m, iter)
		
	def continuarDescarga(self):
		""""""
		treeselection = self.tvDownload.get_selection()
		model, iter = treeselection.get_selected()
		estado = model.get_value(iter, 0)
		if estado == self.nofinish_icon:
			nombre = model.get_value(iter, 1)
			capitulo = model.get_value(iter, 2)
			codigo = model.get_value(iter, 7)
			fansub = model.get_value(iter, 5)
			m=lib_submanga.Manga(nombre, capitulo, codigo, fansub)

			self.descargarManga(m, iter, True)

	def descargarManga(self, manga, iter, continuar=False):
		""""""
		descarga=downloader.Downloader(manga, self)
		threading.Thread(target=descarga.iniciarDescarga, args=(iter, continuar,)).start()

	def addRow(self, nombre, numero,fansub, imagenes, codigo):
		""""""
		i=self.tvDownload.get_model().append(None, [self.down_icon, nombre, numero, 0, True, fansub, imagenes, codigo])
		return i

	def deleteRow(self, a):
		""""""
		model=self.tvDownload.get_model()
		model.remove(a)
	
	#Aun no ha sido probada debidamente
	def getIter(self, codigo):
		""""""
		lista = self.tvDownload.get_model()
		for i in range(len(lista)):
			if int(lista[i][7]) == int(codigo):
				return lista[i].iter
		return -1

	def refreshProgress(self, iter, newProgress, numImg):
		""""""
		model=self.tvDownload.get_model()
		model.set_value(iter, 3, newProgress)
		imageInfo = model.get_value(iter, 6)
		imageInfo = imageInfo.split('/')
		if len(imageInfo)==1:
			model.set_value(iter, 6, str(numImg)+"/"+imageInfo[0])
		else:
			model.set_value(iter, 6, str(numImg)+"/"+imageInfo[1])

		if newProgress == 100:
			model.set_value(iter, 0, self.ok_icon)
			#model.set_value(iter, 4, False)
			model.set_value(iter, 6, str(numImg))
			n=notifications.Notification()
			n.notify("Descarga completada","Ha terminado la descarga de "+model.get_value(iter, 1)+" "+model.get_value(iter, 2))
		else:
			model.set_value(iter, 0, self.down_icon)


	def abrirEnWeb(self):
		""""""
		treeselection = self.tvDownload.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 7)
		webbrowser.open("http://submanga.com/"+text)


	def saveAs(self, tipo):
		""""""
		treeselection = self.tvDownload.get_selection()
		model, iter = treeselection.get_selected()
		text = model.get_value(iter, 7)
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
