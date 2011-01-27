# -*- coding: utf-8 -*-

import urllib, urllib2
import time

class Novedades:
	""""""
	def __init__(self):
		""""""
		self.resultados=[]

	def realizarBusqueda(self, numres):
		""""""
		self.resultados[:].remove
		f = urllib2.urlopen("http://submanga.com")
		
		numeroDias=0
		
		etiquetaManga = "<td class=\"s\"><a rel=\"nofollow\" href=\"http://submanga.com/"
		etiquetaFansub = "/scanlation/"
		etiquetaFecha = "<th class=\"l\" colspan=\"3\"><a name=\""

		tamEtiquetaManga = 0
		tamEtiquetaFansub = len(etiquetaFansub)
		tamEtiquetaFecha = len(etiquetaFecha)
		
		encontradoManga = 0
		encontradoFansub = 0
		encontradoFecha = 0

		origen=0
		linea = ""
		result = ""
		fansub = ""
		fecha = ""
		auxFecha = ""
		recientes = 0
		
		while True:
			linea = f.readline()
			if not linea: break
			encontradoManga = linea.find(etiquetaManga);
			if encontradoManga != -1: break	
				
		while True:
			if linea:
				encontradoManga = linea.find(etiquetaManga)
				tamEtiquetaManga = len(etiquetaManga)		
				encontradoFecha = linea.find(etiquetaFecha)

				while encontradoManga!=-1:
					if encontradoFecha < encontradoManga and encontradoFecha != -1:
						origen=encontradoFecha+tamEtiquetaFecha
						aux=auxFecha
						fecha=""
						while linea[origen]!='"':
							fecha=fecha+linea[origen]
							origen=origen+1

						encontradoFecha = linea.find(etiquetaFecha, encontradoFecha+1)
						auxFecha = time.strptime(fecha, "%d/%m/%Y")
						if aux != auxFecha:
							numeroDias = numeroDias + 1
						if numeroDias>numres: break

					origen=encontradoManga+tamEtiquetaManga;
					result=""
					while linea[origen]!='"':
						result=result+linea[origen]
						origen=origen+1
					result=result.replace("_"," ")

					encontradoFansub = linea.find(etiquetaFansub, encontradoManga)
					origen=encontradoFansub+tamEtiquetaFansub
					fansub=""
					while linea[origen]!='"':
						fansub=fansub+linea[origen]
						origen=origen+1
					fansub=fansub.replace("_"," ")

					list1 = result.split("/");
					manga = Manga(list1[0],list1[1],list1[2], fansub, "", fecha);
					self.resultados.append(manga)
			
					encontradoManga = linea.find(etiquetaManga, encontradoManga+1)
					
			f.close()
			if numeroDias>numres: break
			recientes = recientes + 1
			f = urllib2.urlopen("http://submanga.com/p/" + str(recientes))
			etiquetaManga = "<td class=\"s\"><a href=\"http://submanga.com/"
			while True:
				linea = f.readline()
				if not linea: break
				encontradoManga = linea.find(etiquetaManga);
				if encontradoManga != -1: break
			
		#En la pagina inicial aparece una lista mas actualizada que en la primera hoja de recientes.
		#En la pagina inicial y la primera hoja de recientes, se repiten mangas.
		#En todas las paginas aparecen los mangas de 50 en 50.
		if len(self.resultados) > 50:
			index = 0
			for i in range(50):
				if self.resultados[50].codigo >= self.resultados[i].codigo:
					index = i+1
					break
			self.resultados = self.resultados[0:index] + self.resultados[51:]

	def getManga(self, num):
		""""""
		return self.resultados[num]

	def numMangas(self):
		""""""
		return len(self.resultados)


class Destacados:
	""""""
	def __init__(self):
		""""""
		self.resultados=[]

	def realizarBusqueda(self, numres=10):
		""""""
		self.resultados[:].remove
		f = urllib2.urlopen("http://submanga.com")
		linea = ""
		encontradoManga = 0;
		etiquetaManga = "<td><a href=\"http://submanga.com/"
		
		while True:
			linea = f.readline()
			if not linea: break
			encontradoManga = linea.find(etiquetaManga);
			if encontradoManga != -1: break
		
		if linea:
			encontradoFansub = 0;
			etiquetaFansub = "<span class=\"grey s\">"
		
			tamEtiquetaManga = len(etiquetaManga);
			tamEtiquetaFansub = len(etiquetaFansub);

			origen=0;
			result = "";
			fansub = "";

			while encontradoManga!=-1:
				origen=encontradoManga+tamEtiquetaManga;
				result=""
				while linea[origen]!='"':
					result=result+linea[origen]
					origen=origen+1
				result=result.replace("_"," ")

				encontradoFansub = linea.find(etiquetaFansub, encontradoManga)
				origen=encontradoFansub+tamEtiquetaFansub
				fansub=""
				while linea[origen]!='<':
					fansub=fansub+linea[origen]
					origen=origen+1

				list1 = result.split("/");
				manga = Manga(list1[0],list1[1],list1[2], fansub);
				self.resultados.append(manga)

				encontradoManga = linea.find(etiquetaManga, encontradoManga+1);
		
		f.close()

	def getManga(self, num):
		""""""
		return self.resultados[num]

	def numMangas(self):
		""""""
		return len(self.resultados)


class Manga:
	""""""
	def __init__(self, nombre, numero, codigo, fansub="CONCEPT", numpaginas="", fecha=""):
		""""""
		self.nombre=nombre
		self.numero=numero
		self.codigo = codigo
		self.fansub = fansub
		self.numpaginas = numpaginas
		self.fecha = fecha
		self.directorio = ""

	def getDirectorio(self):
		""""""
		if self.directorio == "":
			direccion_manga= "http://submanga.com/c/"+str(self.codigo)+"/1"
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

			fin = False
			origen=0
			encontrado=0
			while fin == False:
				result=""
				encontrado=linea.find('<td class="s"><a href="http://submanga.com/', encontrado)
				if encontrado != -1:
					origen = encontrado+len('<td class="s"><a href="http://submanga.com/')

					while linea[origen]!='"':
						result=result+linea[origen]
						origen=origen+1
					result=result.replace("_"," ")
						
					encontrado = linea.find("/scanlation/", encontrado)
					origen=encontrado+len("/scanlation/")
					fansub=""
					while linea[origen]!='"':
						fansub=fansub+linea[origen]
						origen=origen+1
					fansub=fansub.replace("_"," ")

					list1 = result.split("/");
					manga = Manga(list1[0],list1[1],list1[2],fansub);
					self.resultados.append(manga)
				else:
					fin=True
		f.close()

	def busquedaExacta(self, numres=10):
		""""""
		self.resultados[:].remove
		nameManga=self.nombre.replace(" ","_")
		f = urllib2.urlopen("http://submanga.com/"+nameManga+"/completa")
		while True:
			linea = f.readline()
			if not linea: break

			fin = False
			origen=0
			encontrado=0
			while fin == False:
				result=""
				encontrado=linea.find('<td class="s"><a href="http://submanga.com/'+nameManga+'/'+str(self.numero)+'/', encontrado+1)
				if encontrado != -1:
					origen = encontrado+len('<td class="s"><a href="http://submanga.com/')

					while linea[origen]!='"':
						result=result+linea[origen]
						origen=origen+1
					result=result.replace("_"," ")

					list1 = result.split("/");
					manga = Manga(list1[0],list1[1],list1[2]);
					self.resultados.append(manga)
				else:
					fin=True
		f.close()


	def getManga(self, num):
		""""""
		return self.resultados[num]

	def numMangas(self):
		""""""
		return len(self.resultados)

if __name__ == "__main__":
	#~ m=Manga("Gantz", "306", "51545", fansub="CONCEPT", numpaginas="")
	#~ print m.numpaginas
	#~ print m.fansub
	#~ m.getExtraInfo()
	#~ print m.numpaginas
	#~ print m.fansub
	#~ print m.getDirectorio()
	b=Busqueda()
	b.realizarBusqueda("Naruto", "")
	print b.resultados
