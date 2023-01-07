from math import *
import pygame

# Definimos algunos colores

#NEGRO = 	(0, 0 ,0)
#BLANCO = 	(255, 255, 255)
#ROJO = 		(255, 0, 0)
#AZUL = 		(0, 0, 255)
#VIOLETA = 	(98, 0, 255)


class Matriz():

	def __init__(self):
		#self.matriz= []
		self.prueba = 0
		

	#------------------------------------------------------ 
	#	Imprime Matriz con formato
	
	def imprimeMatriz(self, titulo,M):
		"""
		Imprime formateada una matriz

		"""
		print ()
		print (titulo)
		for i in range(len(M)):
			#print ('[',end="")
			for j in range(len(M[i])):
				print ('{:>8.5s}'.format(str(M[i][j])),end="")
			print ()
			#print (']')
 		

	#----------------------------------------------------------------
	#	

	def matriz2str(self, matriz):
		"""
		Contruye y devuelve un texto con la matriz formateda, para luego ser impresa 
		"""
		cadena = ""
		for i in range(len(matriz)):
			cadena += "["
			for j in range(len(matriz[i])):
				cadena += "{:>8.5s}".format(str(matriz[i][j]))
			cadena += "]\n"
		returncadena

	#----------------------------------------------------------------
	#	

	def creaMatriz(self, n, m):
		'''
		Esta funcion crea una matriz vacia con n filas y m columnas.

			param n : Numero de filas.
			param m : Numero de columnas
			type n: int
			type m: int
			return: devuelve una matriz n por m
			rtype: matriz (lista de listas)
		'''
		matriz = []
		for i in range(n):
			a = [0]*m
			matriz.append(a)
		return matriz

	#----------------------------------------------------------------
	#	
	
	def creaMatrizDato(self, n ,m, dato):
		'''
		Esta funcion crea una matriz con n filas y n columnas.
		Cada celda contiene el valor "dato"

			param n : Numero de filas.
			param m : Numero de columnas
			param dato: Un valor
			type n: entero
			type m: entero
			type dato: tipo simple
			return: devuelve una matriz n por m
			rtype: matriz (lista de listas)
		'''

		matriz = []
		for i in range(n):
			a = [dato]*m
			matriz.append(a)
		return matriz

	#----------------------------------------------------------------
	#	

	def matrizCorrecta(self, M):
		'''
		Nos dice si una matriz es correcta.

			param M: una matriz
			type M: matriz
			return: True si es correcta, False en caso contrario
		'''

		Nfilas = 	len(M)
		Ncolumnas = len(M[0])
		correcto = True
		i = 1
		while i < Nfilas and correcto:
			correcto = (len(M[i]) == Ncolumnas)
			i += 1
		return correcto

	#----------------------------------------------------------------
	#	

	def filas(self, M):
		'''
		Nos dice el número de filas de una matriz correcta.

			param M: una matriz
			type M: matriz
			return: número de filas
		'''
		
		if self.matrizCorrecta(M):
			return len(M)

	#----------------------------------------------------------------
	#	

	def columnas(self, M):
		'''
		Nos dice el número de columnas de una matriz correcta.

			param M: una matriz
			type M: matriz
			return: número de columnas
		'''
		
		if self.matrizCorrecta(M):
			return len(M[0])

	#----------------------------------------------------------------
	#	

	def matrizIdentidad(self, n):
		'''
		Crea una matriz identidad de tamaÃ±o n

			param n : número de filas.
			type n : entero
			return: matriz identidad de tamaÃ±o n
		'''
		m = self.creaMatriz(n,n)
		for i in range(n):
			m[i][i] = 1
		return m

	#----------------------------------------------------------------
	#	

	def copy(self, m):
		'''
		Realiza una copia independiente de la matriz
		'''

		result=[]
		for f in m:
			result.append(f[:])
		return result

	#----------------------------------------------------------------
	#	

	def leeMatriz(self, n, m):
		'''
		Esta función lee por teclado una matríz con n filas y n columnas.

			param n : Número de filas.
			param m : Número de columnas
			type n: entero
			type m: entero
			return: devuelve una matriz n por m
		'''
		A = self.creaMatriz(n,m)
		for i in range(n):
			for j in range(m):
				A[i][j] = int(raw_input("Introduce la componente (%d,%d): "%(i,j)))
		return A


	#----------------------------------------------------------------
	#	

	def sumaMatriz(self, A, B):
		'''
		Suma dos matrices. Las dos matrices deben ser de la misma dimensión

			param A: una matriz nxm
			param B: una matriz nxm
			type A: Matriz
			type B: Matriz
			return: Matriz suma
		'''

		if self.filas(A) == self.filas(B) and self.columnas(A) == self.columnas(B):
			C = self.creaMatriz(self.filas(A), self.columnas(A))
			for i in range(self.filas(A)):
				for j in range(self.columnas(A)):
					C[i][j] = A[i][j] + B[i][j]
			return C

	#----------------------------------------------------------------
	#	

	def multiplicaMatriz(self, A, B):

		'''
		Multiplica dos matrices. El número de columnas de 
		la primera debe ser igual al número de filas de la segunda.

			param A: una matriz nxm
			param B: una matriz mxk
			type A: Matriz
			type B: Matriz
			return: Matriz multiplicación nxk
		'''
		#self.col = self.columnas(A)
		#self.fil = self.filas(B)
		#if self.col == self.fil:
		if self.columnas(A) == self.filas(B):
			C = self.creaMatriz(self.filas(A), self.columnas(B))
			for i in range(self.filas(C)):
				for j in range(self.columnas(C)):
					for k in range(self.columnas(A)):
						C[i][j] += A[i][k] * B[k][j]
			return C

	#----------------------------------------------------------------
	#	

	def traspuesta(self, M):
		'''
		Calcula la matriz traspuesta de M
		'''
		m = len(M) 					# filas
		n = len(M[0]) 				# columnas
		T = self.creaMatriz(n,m)			# crea una nueva matriz
		for i in range(n):
			for j in range(m):
				T[i][j] = M[j][i]	#	traspone los datos 
		return T

	#----------------------------------------------------------------
	#	Convierte vector de puntos en una matriz homogenea

	def	homogeniza(self, lista):
		"""
		Convierte lista de coordenadas normal a formato homofgenea 
		"""
		for punto in lista:
			punto.append(1)
		return lista

	#----------------------------------------------------------------
	#	Convierte vector de puntos en una matriz homogenea

	def	normaliza(self, M, dim):
		"""
		Convierte lista de coordenadas homofgeneas a formato normal
		"""

		if dim < 3 and dim >= 1:
			m = len(M) 				# filas
			n = len(M[0]) 			# columnas (solo x, y, z)
			#print("m {:2d} n {:2d}".format(m,n))
			T = self.creaMatriz(dim, n)		# crea una nueva matriz
			for j in range(n):
				for i in range(dim):
					T[i][j]= M[i][j]/M[3][j]
			return T
		else:
			print("Error en el tipo de normalizacion: tipo = {}".format(tipo))
			return []
	#----------------------------------------------------------------
	#	Convierte vector de puntos en coordenadas del dispositivo

	def mapea(self, valor, VlMax, VlMin, Max):
		"""
			Mapea un punto de ordenada logica a un punto ren loa pantalla 
			segun la transformasion sigueinte:

			Coordenada Logica  	  	Xl_min             Xl                  Xl_max 	  								
									  |----------------|---------------------|
			Coordenada dispositivo	Xd_min             Xd                  Xd_max

			Xd = (Xl - Xd_min)*((Xl_max -Xd_min)/(Xl_max - Xl_min))
		"""

		Pc = []
		for pto in valor:
			Xd = ( pto[0] - VlMin[0] )*( Max[0] / ( VlMax[0] - VlMin[0] ))
			Yd = ( pto[1] - VlMin[1] )*( Max[1] / ( VlMax[1] - VlMin[1] ))
			punto = [Xd, Yd]
			Pc.append(punto)

		return Pc
	
	
	#----------------------------------------------------------------
	#	Convierte vector de puntos en coordenadas del dispositivo
	"""
	def grafica(self, pantalla, color, Vertice, secuencia):
		
			Grafica lineas de una secuencia de referncias (indices inicio y fin) a
			coorednadas
		
		for pto in secuencia: 
			pygame.draw.line(pantalla, color, Vertice[pto[0]], Vertice[pto[1]])
				
	"""		
