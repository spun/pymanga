import os
import ConfigParser
import cons


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
			print "aaa"

		if not self.cfg.read([cons.CONFIG_PATH + CONF]):
			print "No existe el archivo"

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

		print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
		self.cfg.add_section("viewer")
		self.cfg.set("viewer","viewerBackground","#000")



if __name__ == "__main__":
	c = Config()

