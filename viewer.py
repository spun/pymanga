# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import urllib, urllib2
import threading
gtk.gdk.threads_init()

import os
import cons
import lib_submanga

class Visor:
	""""""
	def delete(self, widget, event=None):
		""""""
		self.window.destroy()
		# gtk.main_quit()
		return False

	def __init__(self, manga, config):
		""""""
		self.configuration = config

		# Variables
		self.zoomLevel=100
		self.zoomMode="Normal"
		self.status_fullscreen=False
		self.status_adj=False
		self.image_num = 0
		self.manga=manga
		self.directorio=os.path.join(cons.PATH_LIBRARY, self.manga.codigo, "")

		col=self.configuration.getValue("viewer","viewerBackground")
		self.bgcolor = gtk.gdk.color_parse(col)

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete)
		self.window.resize(700, 700)
		self.window.set_icon_from_file(cons.ICON_PROGRAM)
		self.window.set_border_width(0)
		self.window.set_title(self.manga.nombre+" "+self.manga.numero+" - "+"Cargando...")


		vboxAdm = gtk.VBox()
		vboxAdm.show()
		self.window.add(vboxAdm)

		# Toolbar
		self.toolbar = gtk.Toolbar()
		self.toolbar.show()
		vboxAdm.pack_start(self.toolbar, False, False, 0)

		self.toolbar.set_style(gtk.TOOLBAR_ICONS)

		toolButtonBack = gtk.ToolButton(gtk.STOCK_GO_BACK)
		toolButtonBack.show()
		self.toolbar.add (toolButtonBack)
		toolButtonBack.connect('clicked',  self.prev_image)

		toolButtonNext = gtk.ToolButton(gtk.STOCK_GO_FORWARD)
		toolButtonNext.show()
		self.toolbar.add (toolButtonNext)
		toolButtonNext.connect('clicked',  self.next_image)

		toolSeparator = gtk.SeparatorToolItem()
		self.toolbar.add (toolSeparator)
		toolSeparator.show()

		toolItem1 = gtk.ToolItem();
		toolItem1.show()
		self.toolbar.add (toolItem1)

		pageLabel = gtk.Label(" Pagina ")
		toolItem1.add(pageLabel)
		pageLabel.show ()

		toolItem2 = gtk.ToolItem()
		self.toolbar.add (toolItem2)
		toolItem2.show()

		self.page_pos = gtk.Entry()
		toolItem2.add (self.page_pos)
		self.page_pos.show()

		self.page_pos.connect("activate", self.goto_image, self.page_pos)
		self.page_pos.set_width_chars (3)
		self.page_pos.set_text("0")

		self.toolItem3 = gtk.ToolItem();
		self.toolbar.add (self.toolItem3)
		self.toolItem3.show()

		toolSeparator2 = gtk.SeparatorToolItem()
		self.toolbar.add (toolSeparator2)
		toolSeparator2.show()

		toolButtonBack = gtk.ToolButton(gtk.STOCK_ZOOM_IN)
		toolButtonBack.show()
		self.toolbar.add (toolButtonBack)
		toolButtonBack.connect('clicked',  self.changeZoomLevel, "up")

		toolButtonNext = gtk.ToolButton(gtk.STOCK_ZOOM_OUT)
		toolButtonNext.show()
		self.toolbar.add (toolButtonNext)
		toolButtonNext.connect('clicked',  self.changeZoomLevel, "down")

		toolButtonBack = gtk.ToolButton(gtk.STOCK_ZOOM_100)
		toolButtonBack.show()
		self.toolbar.add (toolButtonBack)
		toolButtonBack.connect('clicked',  self.changeZoomLevel, "reset")

		toolButtonNext = gtk.ToolButton(gtk.STOCK_ZOOM_FIT)
		toolButtonNext.show()
		self.toolbar.add (toolButtonNext)
		toolButtonNext.connect('clicked',  self.changeZoomLevel, "adj")

		toolSeparator3 = gtk.SeparatorToolItem()
		self.toolbar.add (toolSeparator3)
		toolSeparator3.show()

		toolButtonFull = gtk.ToolButton(gtk.STOCK_FULLSCREEN)
		self.toolbar.add (toolButtonFull)
		toolButtonFull.show()
		toolButtonFull.connect('clicked',  self.full)

		toolSeparator4 = gtk.SeparatorToolItem()
		toolSeparator4.show()
		self.toolbar.add (toolSeparator4)

		toolButtonQuit = gtk.ToolButton(gtk.STOCK_QUIT)
		self.toolbar.add (toolButtonQuit)
		toolButtonQuit.show()
		toolButtonQuit.connect('clicked',  self.delete)

		self.scrolledwindow = gtk.ScrolledWindow()
		self.scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		vboxAdm.pack_start(self.scrolledwindow, True, True, 0)
		self.scrolledwindow.show()

		self.viewport = gtk.Viewport()
		self.scrolledwindow.add(self.viewport)
		self.viewport.show()

		self.viewport.modify_bg(gtk.STATE_NORMAL, self.bgcolor)
		self.viewport.add_events(gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.BUTTON2_MOTION_MASK) # No están por defecto, los agrego
		self.viewport.connect('button-press-event',   self.on_button_pressed)
		self.viewport.connect('button-release-event', self.on_button_released)
		self.viewport.connect('motion-notify-event',  self.on_mouse_moved)
		self.window.connect('key-press-event',        self.on_key_press) # Lo conecto a la ventana, ya que siempre tiene el foco

		self.pixbuf = gtk.gdk.pixbuf_new_from_file(cons.PATH_MEDIA+"question-icon.png")
		self.ancho_pixbuf = float(self.pixbuf.get_width())
		self.alto_pixbuf = float(self.pixbuf.get_height())
		self.image = gtk.Image()
		self.image.set_from_file(cons.PATH_MEDIA+"/loader.gif")
		self.viewport.add(self.image)
		self.image.show()

		# Barra de estado
		self.statusbar = gtk.Statusbar()
		self.context_id = self.statusbar.get_context_id("Users")
		vboxAdm.pack_end(self.statusbar, False, False, 0)
		self.statusbar.push(0, "Listo")
		self.statusbar.show()

		# Slideshow control:
		self.slideshow_window = gtk.Window(gtk.WINDOW_POPUP)
		self.slideshow_window.modify_bg(gtk.STATE_NORMAL, self.bgcolor)
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

		self.ss_back.modify_bg(gtk.STATE_NORMAL, self.bgcolor)
		self.ss_exit.modify_bg(gtk.STATE_NORMAL, self.bgcolor)
		self.ss_forward.modify_bg(gtk.STATE_NORMAL, self.bgcolor)

		self.slideshow_controls.pack_start(self.ss_exit, False, False, 0)
		self.slideshow_controls.pack_start(self.ss_back, False, False, 0)
		self.slideshow_controls.pack_start(self.ss_forward, False, False, 0)
		self.slideshow_window.add(self.slideshow_controls)

		(xpos, ypos) = self.window.get_position()
		screen = self.window.get_screen()
		self.slideshow_window.set_screen(screen)

		self.window.show()
		gtk.gdk.threads_init()


		threading.Thread(target=self.initialInfoManga, args=()).start()
		threading.Thread(target=self.set_image, args=(1,)).start()



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
		shortcut = gtk.accelerator_name(event.keyval, event.state)
		if "Escape" in shortcut:
			if self.status_fullscreen:
				self.full(self)
			else:
				self.window.destroy()

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
		context_id = self.statusbar.get_context_id("Estado de descarga de imagenes")
		self.statusbar.push(context_id, "Descargando imagen "+str(num)+", por favor espere...")

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

				self.page_pos.set_text(str(num))
				self.window.set_title(self.manga.nombre+" "+self.manga.numero+" - "+"Imagen "+str(num))
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


	def next_image(self, widget):
		""""""
		if self.image_num+1 <= int(self.manga.numpaginas):
			threading.Thread(target=self.set_image, args=(self.image_num+1,)).start()

	def prev_image(self, widget):
		""""""
		if self.image_num-1 >= 1:
			threading.Thread(target=self.set_image, args=(self.image_num-1,)).start()

	def goto_image(self, widget, entry):
		""""""
		entry_text = entry.get_text()
		if int(entry_text) <= int(self.manga.numpaginas) and int(entry_text) >= 1:
			threading.Thread(target=self.set_image, args=(int(entry_text),)).start()

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
		else:
			self.window.fullscreen()
			self.status_fullscreen=True
			# Ocultamos la barra de heramientas y de busqueda
			self.toolbar.hide()
			# Mostramos la barra de control de pantalla completa
			self.slideshow_window.show_all()

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
		self.manga.getExtraInfo()

		label = gtk.Label(" de "+self.manga.numpaginas)
		label.show()
		self.toolItem3.add(label)
