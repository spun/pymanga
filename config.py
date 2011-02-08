# -*- coding: utf-8 -*-

import os
import ConfigParser
import cons
import gtk
import locale
import gettext


CONF = "conf"
class Config():
	""""""
	def __init__(self):
		""""""
		self.cfg = ConfigParser.ConfigParser()

		if not os.path.exists(cons.CONFIG_PATH):
			os.mkdir(cons.CONFIG_PATH)
		if not os.path.exists(cons.CONFIG_PATH + CONF):
			self.createDefaultConfig()
			self.configured = False
		if not os.path.exists(cons.PATH_TEMP):
			os.mkdir(cons.PATH_TEMP)
		if not os.path.exists(cons.PATH_LIBRARY):
			os.mkdir(cons.PATH_LIBRARY)

		if not self.cfg.read([cons.CONFIG_PATH + CONF]):
			print "No existe el archivo"
		else:
			self.checkConfig()
			
		#Locale
		locale.setlocale(locale.LC_ALL, '')
		# This is needed to make gtk.Builder work by specifying the
		# translations directory
		locale.bindtextdomain(cons.APP, cons.DIR)
		
		gettext.textdomain(cons.APP)
		gettext.bindtextdomain(cons.APP, cons.DIR)
		 
		#Para usar la función _() y poder traducir textos
		gettext.install(cons.APP, cons.DIR)
		
		#Set the Glade file and signals
		gladefile = "pymanga.glade"
		self.builder = gtk.Builder()
		self.builder.set_translation_domain(cons.APP)
		self.builder.add_from_file(gladefile)
		
		
		
	def setValue(self, section, option, value):
		""""""
		if self.cfg.has_option(section, option):
			self.cfg.set(section, option, value)

		f = open(cons.CONFIG_PATH + CONF, "w")
		self.cfg.write(f)
		f.close()

	def getValue(self, section, option):
		""""""
		if self.cfg.has_option(section, option):
			value = self.cfg.get(section, option)
			return value
		else:
			print "No se encontro el nombre en el archivo de configuracion."

	def createDefaultConfig(self):
		value="800x500+50+50"
		self.cfg.add_section("main")
		self.cfg.set("main","mainWindowGeometry",value)
		self.cfg.set("main","mainTabSelected","0")
		
		self.cfg.add_section("new")
		self.cfg.set("new","newDay","1")

		self.cfg.add_section("viewer")
		self.cfg.set("viewer","viewerBackground","#000")
		

	#Si se tiene un archivo de configuración y se añaden más secciones, actualizar el archivo
	def checkConfig(self):
		""""""
		sections = self.cfg.sections()
		if len(sections) < 3:
			if not self.cfg.has_section("main"):
				value="800x500+50+50"
				self.cfg.add_section("main")
				self.cfg.set("main","mainWindowGeometry",value)
				self.cfg.set("main","mainTabSelected","0")
			if not self.cfg.has_section("new"):
				self.cfg.add_section("new")
				self.cfg.set("new","newDay","1")
			if not self.cfg.has_section("viewer"):
				self.cfg.add_section("viewer")
				self.cfg.set("viewer","viewerBackground","#000")


if __name__ == "__main__":
	c = Config()

