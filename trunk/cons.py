# -*- coding: utf-8 -*-

import sys
import os
import locale

# Constantes del proyecto
#PROGRAM_NAME = "pyManga"
#PROGRAM_VERSION = "0.1.7 beta"
#WEBPAGE = "http://code.google.com/p/pymanga/"
#DOC = "http://code.google.com/p/pymanga/"

#Locale 
APP="pymanga"
DIR="po"

# Directorio del proyecto
if "win" in sys.platform:
	PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
	DEFAULT_PATH = os.path.join(os.path.expanduser("~"), "").decode(locale.getdefaultlocale()[1])
	if PATH not in sys.path:
		sys.path.insert(0, PATH)
else:
	PATH = os.path.join(sys.path[0], "")
	DEFAULT_PATH = os.path.join(os.path.expanduser("~"), "")

CONFIG_PATH = os.path.join(DEFAULT_PATH, ".pymanga" ,"")
#CONFIG_PATH = os.path.join(PATH, ".pymanga" ,"")

# Direciones utiles
#PATH_TEMP = os.path.join(PATH, "temp", "")
PATH_TEMP = os.path.join(CONFIG_PATH, "temp", "")
PATH_MEDIA = os.path.join(PATH, "media", "")
PATH_LIBRARY = os.path.join(CONFIG_PATH, "library", "")
ICON_PROGRAM = PATH_MEDIA + "icon.png"
#LOGO_PROGRAM = PATH_MEDIA + "logo.png"
#ICON_OPEN = PATH_MEDIA + "open.png"
#ICON_RELOAD = PATH_MEDIA + "reload.png"
#PREFERENCES_ICON = PATH_MEDIA + "preferences-icon.png"
#INFO_ICON = PATH_MEDIA + "information_icon.png"
