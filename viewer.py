# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import os
import urllib, urllib2
import threading
import cons
import lib_submanga

class Visor:
	""""""
	def __init__(self, config):
		""""""
		self.configuration = config
		builder = config.builder
		
		#Get objects
		self.window = builder.get_object("ViewerMain")
		self.toolbar = builder.get_object("viewertoolbar")
		toolButtonBack = builder.get_object("toolbuttonback")
		toolButtonNext = builder.get_object("toolbuttonnext")
		self.page_pos = builder.get_object("pagepos")
		self.numpaginas = builder.get_object("viewernumpaginas")
		toolButtonZoomUp = builder.get_object("toolbuttonzoomup")
		toolButtonZoomDown = builder.get_object("toolbuttonzoomdown")
		toolButtonZoomReset = builder.get_object("toolbuttonzoomreset")
		toolButtonZoomAdj = builder.get_object("toolbuttonzoomadj")
		toolButtonFull = builder.get_object("toolbuttonfull")
		toolButtonQuit = builder.get_object("toolbuttonquit")
		self.scrolledwindow = builder.get_object("viewerscrolledwindow")
		self.viewport = builder.get_object("viewport")
		self.image = builder.get_object("viewerimage")
		self.statusbar = builder.get_object("viewerstatusbar")
		
		self.slideshow_window = builder.get_object("SlideshowWindow")
		self.ss_back = builder.get_object("ss_back")
		self.ss_forward = builder.get_object("ss_forward")
		self.ss_exit = builder.get_object("ss_exit")
		
		#Get signals
		toolButtonBack.connect("clicked", self.prev_image)
		toolButtonNext.connect("clicked", self.next_image)
		self.id = self.page_pos.connect("changed", self.goto_image)
		toolButtonZoomUp.connect("clicked", self.changeZoomLevel, "up")
		toolButtonZoomDown.connect("clicked", self.changeZoomLevel, "down")
		toolButtonZoomReset.connect("clicked", self.changeZoomLevel, "reset")
		toolButtonZoomAdj.connect("clicked", self.changeZoomLevel, "adj")
		toolButtonFull.connect("clicked", self.full)
		toolButtonQuit.connect("clicked",  self.delete)
		self.viewport.connect("button-press-event", self.on_button_pressed)
		self.viewport.connect("button-release-event", self.on_button_released)
		self.viewport.connect("motion-notify-event", self.on_mouse_moved)
		self.window.connect("key-press-event", self.on_key_press) # Lo conecto a la ventana, ya que siempre tiene el foco
		#LLamar a hide() en lugar de destroy() al cerrar la ventana
		self.window.connect("delete-event", self.window.hide_on_delete)
		
		self.ss_back.connect("clicked", self.prev_image)
		self.ss_forward.connect("clicked", self.next_image)
		self.ss_exit.connect("clicked", self.full)
		
		#Background
		col = self.configuration.getValue("viewer","viewerBackground")
		self.bgcolor = gtk.gdk.color_parse(col)
		self.viewport.modify_bg(gtk.STATE_NORMAL, self.bgcolor)
		
		self.slideshow_window.modify_bg(gtk.STATE_NORMAL, self.bgcolor)
		self.ss_back.modify_bg(gtk.STATE_NORMAL, self.bgcolor)
		self.ss_exit.modify_bg(gtk.STATE_NORMAL, self.bgcolor)
		self.ss_forward.modify_bg(gtk.STATE_NORMAL, self.bgcolor)

		
	def open(self, status, manga, directorio=""):
		""""""
		# Variables
		self.zoomLevel=100
		self.zoomMode="Normal"
		self.status_fullscreen=False
		self.status_adj=False
		self.image_num = 0
		self.manga=manga
		self.status = status # True = onlie, False = offline

		#Configuration
		self.pixbuf = gtk.gdk.pixbuf_new_from_file(cons.PATH_MEDIA+"question-icon.png")
		self.ancho_pixbuf = float(self.pixbuf.get_width())
		self.alto_pixbuf = float(self.pixbuf.get_height())
		self.image.set_from_pixbuf(self.pixbuf)
		self.window.grab_focus()
		self.window.set_title(self.manga.nombre+" "+self.manga.numero+" - "+_("Loading..."))
		self.numpaginas.set_text(_(" of ") + self.manga.numpaginas + " ")
		#clear() se va posicionando en el último elemento y lo borra. Cada vez que cambia de elemento se llama 
		#a la señal changed y entra en goto_image, por ello bloqueamos durante el clear() la señal changed
		self.page_pos.handler_block(self.id)
		self.page_pos.get_model().clear()
		self.page_pos.handler_unblock(self.id)
		
		(xpos, ypos) = self.window.get_position()
		screen = self.window.get_screen()
		self.slideshow_window.set_screen(screen)

		self.window.present()
		
		if self.status:
			self.statusbar.show()
			self.image.set_from_file(cons.PATH_MEDIA+"/loader.gif")
			gtk.gdk.threads_init()

			threading.Thread(target=self.initialInfoManga, args=()).start()
		else:
			self.directorio=os.path.join(directorio, self.manga.codigo, "")
			self.statusbar.hide()
			for i in range(int(self.manga.numpaginas)):
				self.page_pos.get_model().append([i+1])
			
			self.page_pos.set_active(0)
	
	def set_background(self, col):
		""""""
		self.bgcolor = gtk.gdk.color_parse(col)
		self.viewport.modify_bg(gtk.STATE_NORMAL, self.bgcolor)
		
		self.slideshow_window.modify_bg(gtk.STATE_NORMAL, self.bgcolor)
		self.ss_back.modify_bg(gtk.STATE_NORMAL, self.bgcolor)
		self.ss_exit.modify_bg(gtk.STATE_NORMAL, self.bgcolor)
		self.ss_forward.modify_bg(gtk.STATE_NORMAL, self.bgcolor)
	
		
	def delete(self, widget, event=None):
		""""""
		self.window.hide()
		# gtk.main_quit()
		return False

	def on_button_pressed(self, widget=None, event=None):
		""""""
		if event.button == 1 and event.type == gtk.gdk.BUTTON_PRESS:
			self.next_image(widget)
		elif event.button == 3 and event.type == gtk.gdk.BUTTON_PRESS:
			self.prev_image(widget)
		elif event.button == 2:
			self.viewport.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.FLEUR))
			self.prevmousex = event.x_root
			self.prevmousey = event.y_root

	def on_button_released(self, widget=None, event=None):
		""""""
		if event.button == 2:
			self.viewport.window.set_cursor(None)

	def on_mouse_moved(self, widget, event):
		""""""
		# Ver: http://www.pygtk.org/pygtk2tutorial-es/sec-EventHandling.html
		if event.is_hint:
			x, y, state = event.window.get_pointer()
		else:
			state = event.state
		x, y = event.x_root, event.y_root
		if state & gtk.gdk.BUTTON2_MASK:
			offset_x = self.prevmousex - x
			offset_y = self.prevmousey - y
			self._move_image(offset_x, offset_y)
		self.prevmousex = x
		self.prevmousey = y

	def on_key_press(self, widget=None, event=None):
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
		elif event.keyval == gtk.gdk.keyval_from_name('F11'):
			self.full(self)
		elif event.keyval == gtk.gdk.keyval_from_name('plus'):
			self.changeZoomLevel(self, "up")
		elif event.keyval == gtk.gdk.keyval_from_name('minus'):
			self.changeZoomLevel(self, "down")
		elif event.keyval == gtk.gdk.keyval_from_name('a'):
			if self.status_adj:
				self.changeZoomLevel(self, "reset")
				self.status_adj=False
			else:
				self.changeZoomLevel(self, "adj")
				self.status_adj=True
		elif event.keyval == gtk.gdk.keyval_from_name('c'):
			if self.slideshow_window.get_opacity() == 1:
				self.slideshow_window.set_opacity(0)
			else:
				self.slideshow_window.set_opacity(1)
		shortcut = gtk.accelerator_name(event.keyval, event.state)
		if "Escape" in shortcut:
			if self.status_fullscreen:
				self.full(self)
			else:
				self.window.hide()

	def _move_image(self, offset_x, offset_y):
		""""""
		vport = self.viewport
		xadjust = vport.props.hadjustment
		newx = xadjust.value + offset_x
		yadjust = vport.props.vadjustment
		newy = yadjust.value + offset_y
		# Si las cosas están dentro de los bordes, seteo
		if (newx >= xadjust.lower) and (newx <= (xadjust.upper - xadjust.page_size)):
			xadjust.value = newx
			vport.set_hadjustment(xadjust)
		if (newy >= yadjust.lower) and (newy <= (yadjust.upper - yadjust.page_size)):
			yadjust.value = newy
			vport.set_vadjustment(yadjust)

	def set_image(self, num):
		""""""
		if self.status:
			context_id = self.statusbar.get_context_id(_("Image download status"))
			self.statusbar.push(context_id, _("Downloading image ")+str(num)+_(", please wait..."))

			dir_downloads = cons.PATH_TEMP

			# Si ya existe una imagen anterior la borramos
			imgUbic=dir_downloads+"img_temp.jpg"
			if os.path.exists(imgUbic):
				os.remove(imgUbic)

			dominio = 'img.submanga.com'
			directorio=self.manga.getDirectorio()
			image = urllib.URLopener()
			try:
				imagen_local = "img_temp.jpg"
				image.retrieve("http://img.submanga.com/"+self.manga.getImagen(num), dir_downloads + '/' + imagen_local)
				print "Imagen "+str(num)+" descargada"

				self.pixbuf = gtk.gdk.pixbuf_new_from_file(cons.PATH_TEMP+"/img_temp.jpg")
				self.image.set_from_pixbuf(self.pixbuf)

				# Si se ha descargado la imagen la mostramos
				if os.path.exists(imgUbic):
					self.pixbuf = gtk.gdk.pixbuf_new_from_file(cons.PATH_TEMP+"/img_temp.jpg")
					self.image.set_from_pixbuf(self.pixbuf)

					self.page_pos.set_active(num-1)
					self.window.set_title(self.manga.nombre+" "+self.manga.numero+" - "+_("Image ")+str(num))
					self.ancho_pixbuf = float(self.pixbuf.get_width())
					self.alto_pixbuf = float(self.pixbuf.get_height())
					if self.zoomMode=="Normal":
						self.update_image(self.zoomLevel)
					elif self.zoomMode=="AdjX":
						self.changeZoomLevel(None, "adj")

					self.image_num = num
					self.rescroll()

			except:
				print "No se ha podido descargar la imagen"
				realizado=False

			self.statusbar.pop(context_id)
		else:
			if num <= int(self.manga.numpaginas) and num >= 1:
				digadd=3-len(str(num))
				imgUbic=self.directorio+(digadd*"0")+str(num)+".jpg"
				if os.path.exists(imgUbic):
					self.pixbuf = gtk.gdk.pixbuf_new_from_file(imgUbic)
					self.image.set_from_pixbuf(self.pixbuf)
					self.page_pos.set_active(num-1)
					self.window.set_title(self.manga.nombre+" "+self.manga.numero+" - "+_("Image ")+str(num))
					self.ancho_pixbuf = float(self.pixbuf.get_width())
					self.alto_pixbuf = float(self.pixbuf.get_height())
					if self.zoomMode=="Normal":
						self.update_image(self.zoomLevel)
					elif self.zoomMode=="AdjX":
						self.changeZoomLevel(None, "adj")

					self.image_num = num
					self.rescroll()
					return True
				else:
					print "No existe "+imgUbic
					return False


			else:
				print "No se pudo cambiar la pagina"
				return False
		

	def next_image(self, widget):
		""""""
		entry = self.page_pos.get_active()+1
		if entry+1 <= int(self.manga.numpaginas):
			self.page_pos.set_active(entry)

	def prev_image(self, widget):
		""""""
		entry = self.page_pos.get_active()-1
		if entry+1 >= 1:
			self.page_pos.set_active(entry)

	def goto_image(self, widget):
		""""""
		entry = self.page_pos.get_active()+1
		if self.status:
			self.image.set_from_file(cons.PATH_MEDIA+"/loader.gif")
			threading.Thread(target=self.set_image, args=(entry,)).start()
		else:	
			self.set_image(entry)
		return True

	def rescroll(self, widget=None):
		""""""
		self.scrolledwindow.get_vadjustment().set_value(0)

	def scroll_up(self, widget):
		""""""
		yadjust = self.scrolledwindow.get_vadjustment()
		vActual=yadjust.get_value()
		newy=vActual-60
		if newy >= yadjust.lower and newy <= yadjust.upper - yadjust.page_size:
			self.scroll_pos=newy
		else:
			newy=yadjust.lower
		yadjust.set_value(newy)

	def scroll_down(self, widget):
		""""""
		yadjust = self.scrolledwindow.get_vadjustment()
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
			self.toolbar.show()
			self.slideshow_window.hide_all()
			if self.status: self.statusbar.show()
		else:
			self.window.fullscreen()
			self.status_fullscreen=True
			# Ocultamos la barra de heramientas y de busqueda
			self.toolbar.hide()
			# Mostramos la barra de control de pantalla completa
			self.slideshow_window.show_all()
			if self.status: self.statusbar.hide()

	def changeZoomLevel(self, widget, zoom_ratio):
		""""""
		zoom=self.zoomLevel
		self.zoomMode="Normal"
		if zoom_ratio=="up":
			zoom+=15
		elif zoom_ratio=="down":
			zoom-=15
		elif zoom_ratio=="reset":
			zoom=100
		elif zoom_ratio=="adj":
			rect = self.viewport.get_allocation()
			zoom=(rect.width*100.0)/self.ancho_pixbuf
			self.zoomMode="AdjX"
		self.update_image(zoom)

	def update_image(self,  zoom_ratio):
		""""""
		relacion=zoom_ratio/100.0
		ancho = int(self.ancho_pixbuf*relacion)
		alto = int(self.alto_pixbuf*relacion)
		scaled_buf = self.pixbuf.scale_simple(ancho, alto, gtk.gdk.INTERP_BILINEAR)
		self.image.set_from_pixbuf(scaled_buf)
		self.zoomLevel=zoom_ratio
	
	def initialInfoManga(self):
		""""""
		self.manga.getExtraInfo()
		self.numpaginas.set_text(_(" of ") + self.manga.numpaginas + " ")
		for i in range(int(self.manga.numpaginas)):
			self.page_pos.get_model().append([i+1])
		
		self.page_pos.set_active(0)
