#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
import pygtk
if not sys.platform == 'win32':
        pygtk.require('2.0')
import gtk
import webbrowser

import cons

NAME = cons.PROGRAM_NAME
COPYRIGHT = u"© 2010 " + cons.PROGRAM_NAME
AUTHORS = ["neo"]
LICENSE = """
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
	"""

class About(gtk.AboutDialog):
	""""""
	def __init__(self, widget=None, event=None):
		""""""
		gtk.AboutDialog.__init__(self)
		self.set_position(gtk.WIN_POS_CENTER)
		self.set_icon_from_file(cons.ICON_PROGRAM)
		self.set_logo(gtk.gdk.pixbuf_new_from_file(cons.LOGO_PROGRAM))
		self.set_name(NAME)
		self.set_version(cons.PROGRAM_VERSION)
		self.set_copyright(COPYRIGHT)
		self.set_license(LICENSE)
		self.set_website(cons.WEBPAGE)
		self.connect("response", self.close)
		self.show_all()
		self.run()

	def close(self, widget=None, other=None):
		""""""
		self.destroy()

if __name__ == "__main__":
	g = About()
	gtk.main()
