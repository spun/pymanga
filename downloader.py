#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib
import sys
import os
import urllib, urllib2
import shutil

import lib_submanga
import cons

class Downloader:
	""""""
	def __init__(self, manga, biblio):
		""""""
		self.manga=manga
		self.biblioteca=biblio
		self.estado=False

	def iniciarDescarga(self):
		""""""
		self.estado=True
		self.crearDirectorio()
		self.manga.getExtraInfo()
		self.itera=self.agregarDescarga()
		self.procesarDescarga()
		self.creaFicheroInfo()
		self.estado=False

	def procesarDescarga(self):
		""""""
		limit=self.manga.numpaginas
		numImg=1
		while numImg<=int(limit) and self.estado==True:
			accion=self.descargarImagen(numImg)
			if accion==False:
				print "No se pudo descargar la imagen "+str(numImg)+ ". Reintentando..."
			else:
				self.actualizaProgreso(numImg)
				numImg=numImg+1
		print "Descarga finalizada, se descargaron "+str(numImg-1)+" de "+limit+" imagenes."

	def descargarImagen(self, num):
		""""""
		realizado=False
		dir_downloads = cons.PATH_LIBRARY+self.manga.codigo
		dominio = 'img.submanga.com:8080'
		directorio=self.manga.getDirectorio()
		image = urllib.URLopener()
		try:
			digadd=3-len(str(num))
			imagen_local = (digadd*"0")+str(num)+'.jpg'
			image.retrieve("http://img.submanga.com:8080/"+self.manga.getImagen(num), dir_downloads + '/' + imagen_local)
			print "Imagen "+str(num)+" descargada"
			realizado=True
		except:
			print "No se ha podido descargar la imagen"
			realizado=False

		return realizado

	def crearDirectorio(self):
		""""""
		if not os.path.exists(cons.PATH_LIBRARY):
			os.mkdir(cons.PATH_LIBRARY)

		directorio=cons.PATH_LIBRARY+self.manga.codigo
		if os.path.exists(directorio):
			print "ya existe"
			shutil.rmtree(directorio)
		os.mkdir(directorio)

	def actualizaProgreso(self, n):
		""""""
		if n==self.manga.numpaginas:
			self.biblioteca.refreshProgress(self.itera, 100, n)
		else:
			self.biblioteca.refreshProgress(self.itera, (n*100)/int(self.manga.numpaginas) , n)

	def agregarDescarga(self):
		""""""
		m=self.manga
		i=self.biblioteca.addRow(m.nombre, m.numero,m.fansub, m.codigo, m.numpaginas)
		return i

	def creaFicheroInfo(self):
		""""""
		m=self.manga
		f = open (cons.PATH_LIBRARY+m.codigo+"/infomanga.txt", "w")
		f.write(m.nombre+"\n")
		f.write(m.numero+"\n")
		f.write(m.codigo+"\n")
		f.write(m.fansub+"\n")
		f.write(str(m.numpaginas)+"\n")
		f.close()
