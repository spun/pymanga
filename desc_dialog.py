# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import threading
import urllib, urllib2
import cons
import lib_submanga

class Info():
	""""""
	def __init__(self, config):
		""""""
		builder = config.builder
		
		#Get objects
		self.InfoDialog = builder.get_object("InfoDialog")
		self.imageinfo = builder.get_object("imageinfo")
		self.textinfo = builder.get_object("textinfo")
	
	def open(self, manga):
		""""""
		self.InfoDialog.set_title(_("Loading information..."))
		textbuffer = self.textinfo.get_buffer()
		textbuffer.set_text("")
		self.imageinfo.clear()
		self.manga=manga
		
		gtk.gdk.threads_init()
		
		threading.Thread(target=self.getImagen(), args=()).start()
		threading.Thread(target=self.getInfoText(), args=()).start()
		
		self.InfoDialog.run()
		self.InfoDialog.hide()
		
	def getImagen(self):
		""""""
		nombre=self.manga.nombre.replace(" ","_")

		url="http://submanga.com/"+nombre
		f = urllib2.urlopen(url)
		imageName=""
		seguir=True
		while seguir:
			linea = f.readline()
			if not linea: break

			encontrado = linea.find('http://submanga.com/static/media/')
			if encontrado != -1:
				cont=encontrado+len('http://submanga.com/static/media/')
				while linea[cont]!='"':
					imageName=imageName+linea[cont]
					cont=cont+1
				seguir=False
		f.close()



		try:
			direccion="http://submanga.com/static/media/"+imageName
			dir_downloads = cons.PATH_TEMP
			imagen_local="imgManga.jpg"
			image = urllib.URLopener()
			image.retrieve(direccion, dir_downloads + '/' + imagen_local)
			realizado=True
			pixbuf = gtk.gdk.pixbuf_new_from_file(cons.PATH_TEMP+"imgManga.jpg")
			#~ ancho_pixbuf = float(pixbuf.get_width())
			#~ alto_pixbuf = float(pixbuf.get_height())
		except:
			print "No se pudo descargar"
			realizado=False
			pixbuf = gtk.gdk.pixbuf_new_from_file(cons.PATH_MEDIA+"question-icon.png")
			#~ ancho_pixbuf = float(pixbuf.get_width())
			#~ alto_pixbuf = float(pixbuf.get_height())
			
		self.imageinfo.set_from_pixbuf(pixbuf)
		self.InfoDialog.set_title(_("Information of \"")+self.manga.nombre+"\"")
		

	def getInfoText(self):
		""""""
		nombre=self.manga.nombre.replace(" ","_")

		url="http://submanga.com/"+nombre
		f = urllib2.urlopen(url)
		info=""

		linea = f.read()
		if linea:
			encontrado = linea.find('src="http://submanga.com/static')
			encontrado = linea.find('<p>',encontrado+1)
			encontrado = linea.find('<p>',encontrado+1)

			if encontrado != -1:
				pos=encontrado+len('<p>')
				finl=encontrado = linea.find('</p>',encontrado+1)
				info=linea[pos:finl]

			f.close()

			info=info.replace("<br/>","\n")
			textbuffer = self.textinfo.get_buffer()
			textbuffer.set_text("\n" + info + "\n")


