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
			direccion_manga= "http://submanga.com/c/"+str(self.codigo)
			f = urllib2.urlopen(direccion_manga)
			while True:
				linea = f.readline()
				if not linea: break
				encontrado = linea.find('src="http://img.submanga.com:8081/')
				if encontrado != -1:
					break
			f.close()

			cont = encontrado+len('src="http://img.submanga.com:8081/')
			direccion = ""
			while linea[cont]!='"':
				direccion = direccion+linea[cont]
				cont=cont+1

			self.directorio=direccion.replace("1.jpg", "")
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
			encontradoPag = linea.find('</option></select>')
			encontradoScan = linea.find('<a href="./scanlation/')
			if encontradoPag != -1 and encontradoScan != -1:

				origen = encontradoPag-1;
				while linea[origen]!=">":
					num=linea[origen]+num
					origen=origen-1

				origen = encontradoScan+len('<a href="./scanlation/');
				while linea[origen]!='"':
					fansub=fansub+linea[origen]
					origen=origen+1

		f.close()
		self.numpaginas=num
		self.fansub = fansub.replace("_"," ")

class Busqueda:
	""""""
	def __init__(self):
		""""""
		self.nombre=""
		self.numero=""
		self.resultados=[]


	def getFromDirect(self, url):
		partes=url.split('/')
		tam=len(partes)
		codigo=partes[tam-1]
		numero=partes[tam-2].replace("_"," ")
		nombre=partes[tam-3].replace("_"," ")
		m=Manga(nombre, numero, codigo)
		m.getExtraInfo()

		self.resultados[:].remove
		self.resultados.append(m)

	def realizarBusqueda(self, nombre, numero):
		self.nombre=nombre
		self.numero=numero

		if numero!="":
			self.busquedaExacta()
		else:
			self.realizarBusquedaGlobal()

	def realizarBusquedaGlobal(self):
		""""""
		self.resultados[:].remove
		nameManga=self.nombre.replace(" ","_")
		f = urllib2.urlopen("http://submanga.com/"+nameManga+"/completa")
		while True:
			linea = f.readline()
			if not linea: break
			encontrado = linea.find('<td><a href="http://submanga.com/'+nameManga+'/')
			if encontrado != -1:
				cont = encontrado+len('<td><a href="http://submanga.com/'+nameManga+'/')

				completo=False
				modo=0
				numang=""
				numChapter=""
				while completo==False:
					if modo==0:
						if linea[cont]!='/':
							numChapter = numChapter+linea[cont]
						else:
							modo=1
					else:
						if linea[cont]!='"':
							numang = numang+linea[cont]
						else:
							completo = True
					cont=cont+1

				name=nameManga.replace("_"," ")
				numChapter=numChapter.replace("_"," ")
				manga = Manga(name,numChapter, numang)
				self.resultados.append(manga)

		f.close()

	def busquedaExacta(self, numres=10):
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
	m=Manga("Gantz", "306", "51545", fansub="CONCEPT", numpaginas="")
	print m.numpaginas
	print m.fansub
	m.getExtraInfo()
	print m.numpaginas
	print m.fansub
