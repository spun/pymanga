#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2

class Novedades:
	""""""
	def __init__(self):
		""""""
		self.resultados=[]

	def realizarBusqueda(self, numres=10):
		""""""
		self.resultados[:].remove
		f = urllib2.urlopen("http://submanga.com/p/1")
		fin=False

		nom=""
		num=""
		cod=""
		numeroMangas=0
		mode=0
		while fin==False:
			linea = f.readline()
			if not linea: break
			# Si buscamos un manga
			if mode==0:
				encontrado = linea.find('<td><a href="http://submanga.com/')
				if encontrado != -1:
					completo=False
					cont = encontrado+len('<td><a href="http://submanga.com/')

					parte=0
					nom=""
					num=""
					cod=""
					while completo==False:
						if linea[cont]!='"':
							if linea[cont]=='/':
								parte=parte+1
							else:
								if parte==0:
									nom = nom+linea[cont]
								elif parte==1:
									num = num+linea[cont]
								elif parte==2:
									cod = cod+linea[cont]

							cont=cont+1
						else:
							completo = True
					mode=1
			# Si buscamos una scanlation
			else:
				encontrado = linea.find('<td class="grey s"><a rel="nofollow" href="http://submanga.com/'+nom+'/scanlation/')
				if encontrado != -1:
					cont = encontrado+len('<td class="grey s"><a rel="nofollow" href="http://submanga.com/'+nom+'/scanlation/')
					fansub=""
					while linea[cont]!='"' and linea[cont+1]!='>':
						fansub+=linea[cont]
						cont=cont+1

					nom=nom.replace("_"," ")
					num=num.replace("_"," ")
					fansub=fansub.replace("_"," ")
					manga = Manga(nom,num,cod,fansub)
					self.resultados.append(manga)

					numeroMangas=numeroMangas+1
					mode=0

					if numeroMangas>=numres:
						fin=True

		f.close()

	def getManga(self, num):
		""""""
		return self.resultados[num]

	def numMangas(self):
		""""""
		return len(self.resultados)


class Manga:
	""""""
	def __init__(self, nombre, numero, codigo, fansub="CONCEPT", numpaginas=""):
		""""""
		self.nombre=nombre
		self.numero=numero
		self.codigo = codigo
		self.fansub = fansub
		self.numpaginas = numpaginas
		self.directorio = ""

	def getDirectorio(self):
		""""""
		if self.directorio == "":
			direccion_manga= "http://submanga.com/leer?mode=abajo&n=1&id="+str(self.codigo)
			f = urllib2.urlopen(direccion_manga)
			while True:
				linea = f.readline()
				if not linea: break
				encontrado = linea.find('var u = "')
				if encontrado != -1:
					break
			f.close()

			cont = encontrado+len('var u = "http://img.submanga.com:8080/')
			direccion = ""
			completo=False
			while completo==False:
				if linea[cont]!='"':
					direccion = direccion+linea[cont]
					cont=cont+1
				else:
					completo = True

			self.directorio=direccion
		return self.directorio

	def getImagen(self, pag):
		""""""
		imagen=self.getDirectorio()+str(pag)+".jpg"
		return imagen

	def getExtraInfo(self):
		""""""
		url="http://submanga.com/c/"+self.codigo
		f = urllib2.urlopen(url)
		num=""
		fansub=""
		while True:
			linea = f.readline()
			if not linea: break
			encontrado = linea.find('src="./leer?mode=abajo&n=1&m=')
			if encontrado != -1:
				tamPatron=len('src="./leer?mode=abajo&n=1&m=')
				origen=encontrado+tamPatron

				while linea[origen]!="&":
					num=num+linea[origen]
					origen=origen+1
				origen=origen+1
				resto=linea[origen:]
				resto=resto.split('&')
				fansubc=resto[2].split('=')
				fansub=fansubc[1]
		f.close()
		self.numpaginas=num
		self.fansub = fansub.replace("_"," ")

class Busqueda:
	""""""
	def __init__(self, nombre, numero):
		""""""
		self.nombre=nombre
		self.numero=numero
		self.resultados=[]

	def realizarBusqueda(self, numres=10):
		""""""
		self.resultados[:].remove
		nameManga=self.nombre.replace(" ","_")
		f = urllib2.urlopen("http://submanga.com/"+nameManga+"/completa")
		while True:
			linea = f.readline()
			if not linea: break
			encontrado = linea.find('<td><a href="http://submanga.com/'+nameManga+'/'+str(self.numero)+'/')
			if encontrado != -1:
				cont = encontrado+len('<td><a href="http://submanga.com/'+nameManga+'/'+str(self.numero)+'/')

				completo=False
				numang=""
				while completo==False:
					if linea[cont]!='"':
						numang = numang+linea[cont]
						cont=cont+1
					else:
						completo = True

				nameManga=nameManga.replace("_"," ")
				manga = Manga(nameManga,str(self.numero), numang)
				self.resultados.append(manga)
		f.close()

	def getManga(self, num):
		""""""
		return self.resultados[num]

	def numMangas(self):
		""""""
		return len(self.resultados)

if __name__ == "__main__":
	n = Novedades()
	n.realizarBusqueda(10)
	print n.numMangas()
