#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cons
import os

class Notification:
	""""""
	def notify(self, title="Hola usuario", text="Estas viendo una caracteristica aun en prueba"):
		""""""
		os.popen('notify-send "%s" "%s" -i "%s"'%(title,text,cons.ICON_PROGRAM))
