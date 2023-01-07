from math import *
from  ClaseMatrices import *
import pygame

#-----------------------------------------------------
#	Matrices  de transformacion
#-----------------------------------------------------

class Modela():
		
	def __init__(self):

		"""
		Inicializador
			
		"""
		
		self.Opera = Matriz()  # se creainstancia de clase matriz paralas operaciones
		
		self.Acumula= []
		self.Lista = []
		
		self.tipo = 	2  		# Tipo de modelo cartesiano tipo = 2, 2D; tipo = 3, 3D 
		
		#-----------------------------------------------------
		# 	Parametros de traslacion
			
		self.Xo = 0		#	Translada distancia en el eje  X
		self.Yo = 0		#	Translada distancia en el eje  Y
		self.Zo = 0		#	Translada distancia en el eje  Z
	
		#-----------------------------------------------------
		# 	Parametros de escalado
		
		self.Sx = 0		#	Escala valor en el eje  X
		self.Sy = 0		#	Escala valor en el eje  y
		self.Sz = 0		#	Escala valor en el eje  z
		
		#-----------------------------------------------------
		# 	Parametros de rotacion
	
		self.theta = 	0	#	Angulo de rotacion respecto al eje z
		self.alfa = 	0	#	Angulo de rotacion respecto al eje x
		self.beta = 	0	#	Angulo de rotacion respecto al eje y
	
		#-----------------------------------------------------
		#TPunto focal Perspectiva 
	
		self.Lambda = 1
	
		self.K = 1;
	
	
	
	#-----------------------------------------------------

	def traslada(self, matriz, Tx, Ty, Tz = 0):
		"""
		"""
		self.Xo = Tx		#	Translada distancia en el eje  X
		self.Yo = Ty		#	Translada distancia en el eje  Y
		self.Zo = Tz		#	Translada distancia en el eje  Z
		self.Tra =  [[1, 0, 0, self.Xo],
					 [0, 1, 0, self.Yo],
					 [0, 0, 1, self.Zo],
					 [0, 0, 0,    1]]
		
		self.Acumula = self.Opera.multiplicaMatriz(self.Tra, matriz)					#	Escala uniformmente 
		return self.Acumula

	#-----------------------------------------------------

	def escala(self, matriz, Ex, Ey, Ez = 0):
		"""
		"""
		self.Sx = Ex		#	Translada distancia en el eje  X
		self.Sy = Ey		#	Translada distancia en el eje  Y
		self.Sz = Ez		#	Translada distancia en el eje  Z
		self.Esc = [[ self.Sx, 0,  0,  0],
	                [0, self.Sy,   0,  0],
					[0,  0, self.Sz,   0],
					[0,  0,    0,      1]]
		
		self.Acumula =self.Opera.multiplicaMatriz(self.Esc ,matriz)					#	Escala uniformmente 
		return self.Acumula

	#-----------------------------------------------------

	def RotaX(self, matriz, Ang):
		"""
		"""
		self.alfa = Ang*pi/180		#	Translada distancia en el eje  X
		self.Rox = [ [1,     0,         0,      0],
					 [0,  cos(self.alfa), sin(self.alfa), 0],
					 [0, -sin(self.alfa), cos(self.alfa), 0],
					 [0,     0,         0,      1]]
		
		self.Acumula = self.Opera.multiplicaMatriz(self.Rox ,matriz)					#	Escala uniformmente 
		return self.Acumula

	#-----------------------------------------------------

	def RotaY(self, matriz, Ang):
		"""
		"""
		self.beta = Ang*pi/180		#	Translada distancia en el eje  X
		self.Roy = [[ cos(self.beta), 0, -sin(self.beta), 0],
					[    0,      1,      0,     0],
					[ sin(self.beta), 0,  cos(self.beta), 0],
					[    0,      0,      0,     1]]
		
		self.Acumula = self.Opera.multiplicaMatriz(self.Roy ,matriz)					#	Escala uniformmente 
		return self.Acumula

	#-----------------------------------------------------

	def RotaZ(self, matriz, Ang):
		"""
			Rota punto un angulo <ang> 
		"""

		self.theta = Ang*pi/180
		self.Roz = [ [ cos(self.theta), sin(self.theta), 0, 0],
					[-sin(self.theta), cos(self.theta), 0,  0],
					[	0,          0,        1,            0],
					[	0,          0,        0,            1]]
		
		self.Acumula = self.Opera.multiplicaMatriz(self.Roz ,matriz)					#	Escala uniformmente 
		return self.Acumula

	#-----------------------------------------------------

	def proyecta_vista(self, matriz, factor):
		"""
		"""
		if factor > 0:
			self.Lambda= factor
			self.Per = [ [ 1,    0,     0,      0],
				[ 0,    1,     0,      0],
				[ 0,    0,     1,      0],
				[ 0,    0, -1/self.Lambda,  1]]
			
			self.Acumula = self.Opera.multiplicaMatriz(self.Per ,matriz)					#	Escala uniformmente 
		return self.Acumula
	#-----------------------------------------------------
	
	def mapea_en_ventana(self,  lista, VlMax, VlMin, Max):
		self.Lista  = 	self.Opera.mapea(lista, VlMax, VlMin, Max)
		return self.Lista
		
	#-----------------------------------------------------	
		
	def grafica(self, pantalla, color, Vertices, secuencia):
		"""
			Grafica lineas de una secuencia de referncias (indices inicio y fin) a
			coorednadas
		"""
		for pto in secuencia: 
			pygame.draw.line(pantalla, color, Vertices[pto[0]], Vertices[pto[1]])

	#-----------------------------------------------------	
		
	def convierte_coordenadas(self, matriz):
		"""
		"""
		dato = self.Opera.homogeniza(matriz)
		dato = self.Opera.traspuesta(dato) 
		return dato
		
	#-----------------------------------------------------	
		
	def repone_coordenadas(self, matriz,tipo):
		"""
		"""
		if tipo > 1 and tipo <= 3:
			dato = self.Opera.normaliza(matriz,tipo)
			dato = self.Opera.traspuesta(dato) 
			return dato
