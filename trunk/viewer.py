#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import httplib
import threading
gtk.gdk.threads_init()

import cons
import lib_submanga

class Visor:
	""""""
	def delete(self, widget, event=None):
		""""""
		widget.destroy()
		#~ gtk.main_quit()
		return False

	def __init__(self, manga):
		""""""
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete)
		self.window.resize(700, 700)
		self.window.set_icon_from_file(cons.ICON_PROGRAM)
		self.window.set_title(manga.nombre+" "+manga.numero+" - Cargando...")
		self.window.set_border_width(0)

		# Variables
		self.manga_select=False
		self.status_fullscreen=False
		self.image_num = 0
		self.manga=manga

		# Caja contenedora de la ventana
		vbox1 = gtk.VBox()
		vbox1.show()
		self.window.add(vbox1)

		# Toolbar
		self.toolbar1 = gtk.Toolbar()
		self.toolbar1.show()
		vbox1.pack_start(self.toolbar1, False, False, 0)

		self.toolbar1.set_style(gtk.TOOLBAR_BOTH)
		self.toolbar1.get_icon_size()

		toolbutton3 = gtk.ToolButton(gtk.STOCK_GO_BACK)
		toolbutton3.show()
		self.toolbar1.add (toolbutton3)
		toolbutton3.connect('clicked',  self.prev_image)

		toolbutton4 = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
		toolbutton4.show()
		self.toolbar1.add (toolbutton4)

		toolbutton4.connect('clicked',  self.next_image)

		separatortoolitem1 = gtk.SeparatorToolItem()
		separatortoolitem1.show()
		self.toolbar1.add (separatortoolitem1)

		toolitem3 = gtk.ToolItem();
		toolitem3.show()
		self.toolbar1.add (toolitem3)

		label2 = gtk.Label(" Pagina ")
		label2.show ()
		toolitem3.add (label2)

		toolitem4 = gtk.ToolItem()
		toolitem4.show()
		self.toolbar1.add (toolitem4)

		self.page_pos = gtk.Entry()
		self.page_pos.show()
		toolitem4.add (self.page_pos)

		self.page_pos.connect("activate", self.goto_image, self.page_pos)
		self.page_pos.set_width_chars (3)
		self.page_pos.set_text("-")

		separatortoolitem2 = gtk.SeparatorToolItem()
		separatortoolitem2.show()
		self.toolbar1.add (separatortoolitem2)

		toolbutton5 = gtk.ToolButton(gtk.STOCK_FULLSCREEN)
		toolbutton5.show()
		self.toolbar1.add (toolbutton5)
		toolbutton5.connect('clicked',  self.full)


		# Scrolled window
		scrolledwindow1 = gtk.ScrolledWindow()
		scrolledwindow1.show()
		vbox1.pack_start(scrolledwindow1, True, True, 0)

		scrolledwindow1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		vadj = scrolledwindow1.get_vadjustment()
		vadj.connect('changed',self.rescroll,vadj, scrolledwindow1)

		# Imagen
		self.image = gtk.Image()
		self.image.show()
		scrolledwindow1.add_with_viewport(self.image)

		# Slideshow control:
		self.slideshow_window = gtk.Window(gtk.WINDOW_POPUP)
		self.slideshow_controls = gtk.HBox()
		self.ss_back = gtk.Button()
		self.ss_back.add(gtk.image_new_from_stock(gtk.STOCK_GO_BACK, gtk.ICON_SIZE_BUTTON))
		self.ss_back.set_property('can-focus', False)
		self.ss_back.connect('clicked', self.prev_image)

		self.ss_forward = gtk.Button()
		self.ss_forward.add(gtk.image_new_from_stock(gtk.STOCK_GO_FORWARD, gtk.ICON_SIZE_BUTTON))
		self.ss_forward.set_property('can-focus', False)
		self.ss_forward.connect('clicked', self.next_image)

		try:
			self.ss_exit = gtk.Button()
			self.ss_exit.add(gtk.image_new_from_stock(gtk.STOCK_LEAVE_FULLSCREEN, gtk.ICON_SIZE_BUTTON))
		except:
			self.ss_exit = gtk.Button()
			self.ss_exit.set_image(gtk.image_new_from_stock('leave-fullscreen', gtk.ICON_SIZE_MENU))
		self.ss_exit.set_property('can-focus', False)
		self.ss_exit.connect('clicked', self.full)

		self.slideshow_controls.pack_start(self.ss_exit, False, False, 0)
		self.slideshow_controls.pack_start(self.ss_back, False, False, 0)
		self.slideshow_controls.pack_start(self.ss_forward, False, False, 0)
		self.slideshow_window.add(self.slideshow_controls)

		(xpos, ypos) = self.window.get_position()
		screen = self.window.get_screen()
		self.slideshow_window.set_screen(screen)

		self.image.set_from_file(cons.PATH_MEDIA+"/loader.gif")

		self.image_num += 1
		#self.show_image_by_number(self,self.image_num)
		threading.Thread(target=self.show_image_by_number, args=(self,self.image_num)).start()

		self.window.show()
		print manga.nombre

	def next_image(self, widget):
		""""""
		self.image_num += 1
		threading.Thread(target=self.show_image_by_number, args=(self,self.image_num)).start()
		return True

	def prev_image(self, widget):
		""""""
		self.image_num -= 1
		if self.image_num != 0:
			threading.Thread(target=self.show_image_by_number, args=(self,self.image_num)).start()
		return True

	def goto_image(self, widget, entry):
		""""""
		entry_text = entry.get_text()
		self.image_num = int(entry_text)
		self.show_image_by_number(self, self.image_num)
		return True

	# Muestra la imagen a partir de un numero
	def show_image_by_number(self, widget, number):
		""""""
		dir_downloads = cons.PATH_TEMP
		dominio = 'img.submanga.com:8080'
		imagen_local = 'img_temp.jpg'
		try:
			# conectamos con el servidor
			conn = httplib.HTTPConnection(dominio)
			# hacemos la peticion a la imagen
			conn.request ("GET", '/' + self.manga.getImagen(number))
			r = conn.getresponse()
			# abrimos o creamos el fichero donde vamos a guardar la imagen
			fichero = file( dir_downloads + '/' + imagen_local, "wb" )
			# guardamos la imagen en el fichero
			fichero.write(r.read())
			# y cerramos el fichero
			fichero.close()
		except:
			print "No se ha podido descargar la imagen"

		# Alctualizamos el numero de imagen actual
		self.image_num=number
		# Actualizamos el indicador de imagen
		self.page_pos.set_text(str(self.image_num))
		# Altualizamos el titulo de ventana
		self.window.set_title("Imagen " + str(self.image_num))
		# Mostrams la imagen
		self.image.set_from_file(self.make_image_name(self.image_num))

		return True

	def rescroll(self, widget, vertAdj, scroll):
		""""""
		vertAdj.set_value(0)
		scroll.set_vadjustment(vertAdj)

	def make_image_name(self, image_number):
		""""""
		return cons.PATH_TEMP+"/img_temp.jpg"

	def full(self, widget):
		""""""
		if self.status_fullscreen:
			self.window.unfullscreen()
			self.status_fullscreen=False
			self.toolbar1.show()
			self.slideshow_window.hide_all()
		else:
			self.window.fullscreen()
			self.status_fullscreen=True
			# Ocultamos la barra de heramientas y de busqueda
			self.toolbar1.hide()
			# Mostramos la barra de control de pantalla completa
			self.slideshow_window.show_all()
