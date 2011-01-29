# -*- coding: utf-8 -*-

import httplib
import sys
import os
import urllib, urllib2
import shutil
import glob
import notifications

import lib_submanga
import cons

class Downloader:
	""""""
	def __init__(self, manga, descargas):
		""""""
		self.manga=manga
		self.descargas=descargas
		self.n=notifications.Notification()
		self.directorio = cons.PATH_TEMP
		self.biblioteca = cons.PATH_LIBRARY

	def iniciarDescarga(self, iter=-1, continuar=False):
		""""""
		self.existe=self.crearDirectorio(continuar)
		if not self.existe:
			self.manga.getExtraInfo()
			self.creaFicheroInfo()
			if iter == -1:
				self.itera=self.agregarDescarga()
			else:
				self.itera = iter
			self.procesarDescarga()

	def procesarDescarga(self):
		""""""
		self.n.notify("Descargando manga","Ha empezado la descarga de "+self.manga.nombre+" "+self.manga.numero)
		numImg=1
		archivos = glob.glob(self.directorio+"/"+self.manga.codigo+"/*.jpg")
		if len(archivos) > 0:
			#Sobreescribir ultima imagen si se creo un archivo sin contendio(0 bytes)
			#No suele pasar, pero alguna vez se ha creado una imagen asi al bloquearse al programa
			if os.stat(archivos[-1]).st_size == 0:
				numImg = len(archivos)
			else:
				numImg = len(archivos)+1
		
		self.actualizaProgreso(numImg)
		limit=self.manga.numpaginas
		while numImg<=int(limit):
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
		dir_downloads = self.directorio+self.manga.codigo
		dominio = 'img.submanga.com'
		directorio=self.manga.getDirectorio()
		image = urllib.URLopener()
		try:
			digadd=3-len(str(num))
			imagen_local = (digadd*"0")+str(num)+'.jpg'
			image.retrieve("http://img.submanga.com/"+self.manga.getImagen(num), dir_downloads + '/' + imagen_local)
			print "Imagen "+str(num)+" descargada"
			realizado=True
		except:
			print "No se ha podido descargar la imagen"
			realizado=False

		return realizado

	def crearDirectorio(self, continuar):
		""""""
		directorio=self.directorio+self.manga.codigo
		biblioteca=self.biblioteca+self.manga.codigo
		n=notifications.Notification()
		if os.path.exists(biblioteca):
			self.n.notify("Manga descargado","El manga "+self.manga.nombre+" "+self.manga.numero+" ya se encuentra en la Biblioteca")
			return True
		elif os.path.exists(directorio):
			#shutil.rmtree(directorio)
			if continuar:
				return False
			else:
				self.n.notify("Manga descargado","El manga "+self.manga.nombre+" "+self.manga.numero+" ya esta en Descargas")
				return True
		else:
			os.mkdir(directorio)
			return False

	def actualizaProgreso(self, n):
		""""""
		if n==self.manga.numpaginas:
			self.descargas.refreshProgress(self.itera, 100, n)
		else:
			self.descargas.refreshProgress(self.itera, (n*100)/int(self.manga.numpaginas) , n)

	def agregarDescarga(self):
		""""""
		m=self.manga
		i=self.descargas.addRow(m.nombre, m.numero, m.fansub, m.numpaginas, m.codigo)
		return i

	def creaFicheroInfo(self):
		""""""
		m=self.manga
		f = open (self.directorio+m.codigo+"/infomanga.txt", "w")
		f.write(m.nombre+"\n")
		f.write(m.numero+"\n")
		f.write(m.codigo+"\n")
		f.write(m.fansub+"\n")
		f.write(str(m.numpaginas)+"\n")
		f.close()
