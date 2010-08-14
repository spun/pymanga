#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import urllib, urllib2

import cons
import lib_submanga
import config

class Info(gtk.Dialog):
	""""""
	def close(self, widget=None, other=None):
		""""""
		self.destroy()
		#gtk.main_quit()


	def __init__(self, manga):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon_from_file(cons.INFO_ICON)
		self.connect("response", self.close)
		self.resize(600,500)
		self.set_title("Información de \""+manga.nombre+"\"")
		self.manga=manga

		self.infoHbox = gtk.HBox()
		self.vbox.pack_start(self.infoHbox, False, False, 0)
		self.infoHbox.show()

		viewport = gtk.Viewport()
		self.infoHbox.pack_start(viewport, False, False, 0)
		viewport.show()

		self.image = gtk.Image()
		viewport.add(self.image)
		self.image.show()


		self.getImagen()
		self.getInfoText()

		close_button = gtk.Button(None, gtk.STOCK_CLOSE)
		self.action_area.pack_start(close_button)
		close_button.connect("clicked", self.close)
		close_button.show()

		self.show()


	def getImagen(self):
		""""""
		nombre=self.manga.nombre.replace(" ","_")
		try:
			direccion="http://submanga.com/static/media/"+nombre+".jpg"
			dir_downloads = cons.PATH_TEMP
			imagen_local="imgManga.jpg"
			image = urllib.URLopener()
			image.retrieve(direccion, dir_downloads + '/' + imagen_local)
			realizado=True
			pixbuf = gtk.gdk.pixbuf_new_from_file(cons.PATH_TEMP+"imgManga.jpg")
			#~ ancho_pixbuf = float(pixbuf.get_width())
			#~ alto_pixbuf = float(pixbuf.get_height())
			self.image.set_from_pixbuf(pixbuf)
		except:
			print "No se pudo descargar"
			realizado=False
			pixbuf = gtk.gdk.pixbuf_new_from_file(cons.PATH_MEDIA+"question-icon.png")
			#~ ancho_pixbuf = float(pixbuf.get_width())
			#~ alto_pixbuf = float(pixbuf.get_height())
			self.image.set_from_pixbuf(pixbuf)

		return realizado

	def getInfoText(self):
		""""""
		nombre=self.manga.nombre.replace(" ","_")

		url="http://submanga.com/"+nombre
		f = urllib2.urlopen(url)
		info=""
		comienzo=False
		seguir=True
		while seguir:
			linea = f.readline()
			if not linea: break

			encontrado = linea.find('<div id="info" class="cb u pad"><p>')
			if encontrado != -1:
				pos=encontrado+len('<div id="info" class="cb u pad"><p>')
				finl=len(linea)-len('</p></div><div id="more"></div> ')
				info=linea[pos:finl]
				comienzo=True
				break

		f.close()

		info=info.replace("<br/>","\n")
		textview = gtk.TextView()
		textbuffer = textview.get_buffer()
		textbuffer.set_text(info)
		self.infoHbox.pack_start(textview, True, True, 0)
		textview.show()
		textview.set_wrap_mode(gtk.WRAP_WORD)
		textview.set_left_margin(10)
		textview.set_cursor_visible(False)
		textview.set_editable(False)


if __name__ == "__main__":
	m=lib_submanga.Manga("Bleach", "505", "83567", "CONCEPT", "20")
	i = Info(m)
	gtk.main()
