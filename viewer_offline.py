#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import os

import cons
import lib_submanga

class Visor:
	""""""
	def delete(self, widget, event=None):
		""""""
		self.window.destroy()
		#widget.destroy()
		#gtk.main_quit()
		return False

	def __init__(self, manga):
		""""""
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete)
		self.window.resize(700, 700)
		self.window.set_icon_from_file(cons.ICON_PROGRAM)
		self.window.set_border_width(0)
		self.window.connect('key-press-event', self.topwindow_keypress)

		# Variables
		self.manga_select=False
		self.status_fullscreen=False
		self.image_num = 1
		self.manga=manga
		self.directorio=os.path.join(cons.PATH_LIBRARY, self.manga.codigo, "")

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

		toolitem7 = gtk.ToolItem();
		toolitem7.show()
		self.toolbar1.add (toolitem7)

		label3 = gtk.Label(" de "+self.manga.numpaginas)
		label3.show ()
		toolitem7.add (label3)

		separatortoolitem2 = gtk.SeparatorToolItem()
		separatortoolitem2.show()
		self.toolbar1.add (separatortoolitem2)

		toolbutton5 = gtk.ToolButton(gtk.STOCK_FULLSCREEN)
		toolbutton5.show()
		self.toolbar1.add (toolbutton5)
		toolbutton5.connect('clicked',  self.full)

		separatortoolitem3 = gtk.SeparatorToolItem()
		separatortoolitem3.show()
		self.toolbar1.add (separatortoolitem3)

		toolbutton6 = gtk.ToolButton(gtk.STOCK_QUIT)
		toolbutton6.show()
		self.toolbar1.add (toolbutton6)
		toolbutton6.connect('clicked',  self.delete)

		# Scrolled window
		event_box = gtk.EventBox()
		vbox1.pack_start(event_box, True, True, 0)
		event_box.show()
		event_box.set_events(gtk.gdk.BUTTON_PRESS_MASK)
		event_box.connect("button_press_event", self.button_clicked)

		self.scrolledwindow1 = gtk.ScrolledWindow()
		event_box.add(self.scrolledwindow1)
		self.scrolledwindow1.show()

		self.scrolledwindow1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		self.vadj = self.scrolledwindow1.get_vadjustment()
		self.vadj.connect('changed',self.rescroll)

		# Imagen
		self.image = gtk.Image()
		self.image.show()
		self.scrolledwindow1.add_with_viewport(self.image)

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

		self.set_image(self.image_num)
		self.window.show()

	def set_image(self, num):
		""""""
		if num <= int(self.manga.numpaginas) and num >= 1:
			self.image_num = num
			digadd=3-len(str(num))
			self.image.set_from_file(self.directorio+"/"+(digadd*"0")+str(self.image_num)+".jpg")
			self.page_pos.set_text(str(self.image_num))
			self.window.set_title(self.manga.nombre+" "+self.manga.numero+" - "+"Imagen "+str(num))
			return True
		else:
			print "No se pudo cambiar la pagina"
			return False

	def next_image(self, widget):
		""""""
		self.set_image(self.image_num+1)

	def prev_image(self, widget):
		""""""
		self.set_image(self.image_num-1)

	def goto_image(self, widget, entry):
		""""""
		entry_text = entry.get_text()
		self.set_image(int(entry_text))
		return True

	def rescroll(self, widget):
		""""""
		self.scrolledwindow1.get_vadjustment().set_value(0)

	def scroll_up(self, widget):
		""""""
		yadjust = self.scrolledwindow1.get_vadjustment()
		vActual=yadjust.get_value()
		newy=vActual-60
		if newy >= yadjust.lower and newy <= yadjust.upper - yadjust.page_size:
			self.scroll_pos=newy
		else:
			newy=yadjust.lower
		yadjust.set_value(newy)

	def scroll_down(self, widget):
		""""""
		yadjust = self.scrolledwindow1.get_vadjustment()
		vActual=yadjust.get_value()
		newy=vActual+60
		if newy >= yadjust.lower and newy <= yadjust.upper - yadjust.page_size:
			self.scroll_pos=newy
		else:
			newy=yadjust.upper - yadjust.page_size
		yadjust.set_value(newy)

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

	def topwindow_keypress(self, widget, event):
		""""""
		print event
		if event.keyval == gtk.gdk.keyval_from_name('Left'):
			self.prev_image(self)
		elif event.keyval == gtk.gdk.keyval_from_name('Right'):
			self.next_image(self)
		elif event.keyval == gtk.gdk.keyval_from_name('Up'):
			self.scroll_up(self)
		elif event.keyval == gtk.gdk.keyval_from_name('Down'):
			self.scroll_down(self)
		shortcut = gtk.accelerator_name(event.keyval, event.state)
		if "Escape" in shortcut:
			if self.status_fullscreen:
				self.full(self)
			else:
				self.window.destroy()

	def button_clicked(self, widget, event):
		""""""
		if event.button == 1 and event.type == gtk.gdk.BUTTON_PRESS:
			self.next_image(widget)
		elif event.button == 3 and event.type == gtk.gdk.BUTTON_PRESS:
			self.prev_image(widget)
