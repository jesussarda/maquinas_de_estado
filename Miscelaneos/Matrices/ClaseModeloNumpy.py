'''
Created on 25/6/2019

@author: Jesùs Enrique Sardá
'''

from math import cos, sin
from  numpy import set_printoptions, matrix, ones, zeros, pi
import pygame

NEGRO = 	(0, 0 ,0)
BLANCO = 	(255, 255, 255)
VERDE = 	(0, 255, 0)
ROJO = 		(255, 0, 0)
AZUL = 		(0, 0, 255)
VIOLETA = 	(98, 0, 255)

DOS_D =		2
TRES_D =	3

#-----------------------------------------------------
#	Matrices de transformación
#-----------------------------------------------------

class Modela():
	"""
		Colección de operadores de matrices homogéneas para graficar.
	"""
		
	def __init__(self):
		"""
		Inicializador
		"""

		self.acumula= None	# Matriz acumulada después de una operación

	
	#-----------------------------------------------------

	def imprime_Matriz(self, titulo, matriz, decimales = 2):
		"""

			Imprime formateada una matriz

		:param titulo: 		Identificación o descripción de la naturaleza de la matriz
		:param matriz: 		matriz a peresntar
		:param decimales: 	Precisión numérica
		:return: 			None
		"""

		print ()
		print (titulo)
		set_printoptions(precision= decimales)	
		print(matriz)
		print ()

	#-----------------------------------------------------

	def traslada(self, Tx= 0, Ty= 0, Tz = 0, matriz= None):
		"""

		Traslada puntos de coordenada a lo largo de los ejes las cantidades definidas en T

		:param Tx: 		Traslada por el eje X. Por defecto no hay traslado.
		:param Ty: 		Traslada por el eje Y. Por defecto no hay traslado.
		:param Tz:  	Traslada por el eje Z. Por defecto no hay traslado.
		:param matriz: 	Matriz anterior de la cadena de operaciones
		:return: 		Matriz acumulada
		"""

		Tra =   matrix([[1, 0, 0, Tx],
					 	[0, 1, 0, Ty],
					 	[0, 0, 1, Tz],
					 	[0, 0, 0,  1]])
		
		if matriz == None:
			matriz = self.acumula
			
		self.acumula = Tra.dot(matriz)					#	Escala uniformmente 
		return self.acumula

	
	#-----------------------------------------------------

	def escala(self, Ex = 1, Ey = 1, Ez = 1, matriz = None):
		"""

			Escala puntos de coordenada en las cantidades definidas en E
			Si no se incluye la matriz como parámetro, se procesa con la matriz acumulada

		:param Ex:		Ampliación o reducción en el eje X. Por defecto queda igual
		:param Ey:		Ampliación o reducción en el eje X. Por defecto queda igual
		:param Ez:		Ampliación o reducción en el eje X. Por defecto queda igual
		:param matriz:  Matriz anterior de la cadena de operaciones
		:return:        Matriz acumulada
		"""

		Esc =   matrix([[ Ex,  0, 0,  0],
	                	[  0, Ey, 0,  0],
						[  0,  0, Ez, 0],
						[  0,  0, 0,  1]])
		
		if matriz == None:
			matriz= self.acumula
			
		self.acumula = Esc.dot(matriz)					#	Escala uniformmente 
		return self.acumula


	#-----------------------------------------------------

	def RotaX(self, Ang, matriz = None):
		"""

			Rota puntos de coordenada en torno al eje X
			Si no se incluye la matriz como parámetro, se procesa con la matriz acumulada

		:param Ang:    	Ángulo de rotación
		:param matriz: 	Matriz anterior de la cadena de operaciones
		:return:       	Matriz acumulada
		"""
		"""
		
		"""
		alfa = Ang*pi/180		#	Translada distancia en el eje  X
		Rox =   matrix([[1,     0,         0,      0],
					 	[0,  cos(alfa), sin(alfa), 0],
					 	[0, -sin(alfa), cos(alfa), 0],
					 	[0,     0,         0,      1]])
		
		if matriz == None:
			matriz= self.acumula
			
		self.acumula = Rox.dot(matriz)					#	Escala uniformmente 
		return self.acumula


	#-----------------------------------------------------

	def RotaY(self, Ang, matriz = None):
		"""
			Rota puntos de coordenada en torno al eje Y
			Si no se incluye la matriz como parámetro, se procesa con la matriz acumulada

		:param Ang: 	Ángulo de rotación
		:param matriz: 	Matriz anterior de la cadena de operaciones
		:return:       	Matriz acumulada
		"""

		beta = Ang*pi/180		#	Translada distancia en el eje  X
		Roy =   matrix([[ cos(beta), 0, -sin(beta), 0],
						[    0,      1,     0,      0],
						[ sin(beta), 0,  cos(beta), 0],
						[    0,      0,     0,      1]])
		
		if matriz == None:
			matriz= self.acumula
			
		self.acumula = Roy.dot(matriz)					#	Escala uniformmente 
		return self.acumula


	#-----------------------------------------------------

	def RotaZ(self, Ang, matriz = None):
		"""
			Rota puntos de coordenada en torno al eje Z
			Si no se incluye la matriz como parámetro, se procesa con la matriz acumulada

		:param Ang:		Ángulo de rotación
		:param matriz:	Matriz anterior de la cadena de operaciones
		:return:		Matriz acumulada
		"""

		theta = Ang*pi/180		#	Translada angulo a radianes
		Roz =   matrix([[ cos(theta), sin(theta), 0,  0],
						[-sin(theta), cos(theta), 0,  0],
					 	[	 0,          0,       1,  0],
						[	 0,          0,       0,  1]])
		
		if matriz == None:
			matriz= self.acumula
			
		self.acumula = Roz.dot(matriz)					#	Escala uniformmente 
		return self.acumula


	#-----------------------------------------------------

	def perspectiva(self, focal, matriz = None):
		"""
			Proyecta los puntos de coordenada en un plano, en perspectiva
			con una distancia focal <focal>.

		:param focal:	Distancia focal de la perspectiva
		:param matriz:	Matriz anterior de la cadena de operaciones
		:return:		Matriz acumulada
		"""

		persp = None
		if focal > 0:
			persp =   matrix([[ 1,    0,    0,       0],
							[ 0,    1,    0,       0],
							[ 0,    0,    1,       0],
							[ 0,    0, -1/focal,  1]])
			
		if matriz == None:
			matriz= self.acumula
			
		self.acumula =  persp.dot(matriz)		#	Escala uniformmente
		return self.acumula

		
	#-----------------------------------------------------	

	def convierte_a_homogenea(self, matriz):
		"""
			Convierte una matriz de coordenadas cartesianas normales a coordenadas
			homogéneas, es decir se le añade un uno a la coordenada:

				(x,y,z) => (x,y,z,1)

			para poder operar con matrices de transformación homogéneas (dim 4x4)

		:param matriz: 	Matriz no homogénea (dim 3X3)
		:return: 		Matriz acumulada
		"""

		dim= matriz.shape						# lee dimensiones de la matriz
		if dim[0] != 3 or dim[1]!= 3:
			print(f'\n\tERROR: <convierte_a_homogenea>, se está tratando de usar una matrix de {dim[0]}X{dim[1]}.')
			exit()

		dato = ones([dim[0], dim[1]+1])			# crea matriz homogénea. Añade columna de unos
		dato[0:dim[0] ,0:dim[1]] = matriz		# copia matriz original
		self.acumula = dato.T
		return self.acumula						# retorna matriz traspuesta
		

	#-----------------------------------------------------	

	def convierte_a_normal(self, tipo_dim, matriz = None):
		"""
			Convierte una matriz con el sistema de coordenadas homogeneas a una
			matriz  normal de coordenadas cartesianas de dos o tres dimensiones
			dependiendo de la variable <tipo_dim>
			
		:param tipo_dim: 
		:param matriz: 	
		:return: 	Matriz normalizada 
		"""

		if matriz == None:
			matriz= self.acumula
			
		if tipo_dim > 1 and tipo_dim <= 3:
			matriz_normal= matriz[:tipo_dim]/ matriz[3]
			return matriz_normal.T						# retorna matriz traspuesta
		else:
			print(f"\n\tERROR: <convierte_a_normal> En la dimensión de normalizacion: dim = {tipo_dim}")
			exit()

		
	#-----------------------------------------------------
	
	def mapea_en_pantalla(self,  lista, Vl_Max, Vl_Min, Vd_Max):
		"""
			Mapea una lista de puntos de coordenadas 3D lógica 3D a una lista punto en coordenadas 2D de pantalla
			según la transformación siguiente:

			Coordenada Lógica  	  	Xl_min             <Xl>                  Xl_max
									  |----------------|---------------------|
			Coordenada dispositivo	Xd_min = 0         Xd                  Xd_max

			Xd = (<Xl> - Xd_min)*((Xd_max - Xd_min)/(Xl_max - Xl_min))
			Yd = (<Xl> - Xd_min)*(Xd_max/(Xl_max - Xl_min))

		:param self:
		:param lista: 	Matriz con los vactores X, Y y Z en coordenadas Logicas
		:param Vl_Max: 	Dimensiones máximas de la ventana  Lógica.
		:param Vl_Min:  Dimensiones mínimas de la ventana  Lógica.
		:param Vd_Max: 	Ancho y largo de la pantalla
		:return: 		Matriz con los vectores X y Y en coordenadas de pantalla
		"""

		factor = min(Vd_Max)/max(Vd_Max)	#	Obtiene relación entre ancho y alto  de la pantalla
		if Vd_Max[0] > Vd_Max[1]:			
			lista[:,0] = lista[:,0]*factor	#	Compensa eje X
		else:
			lista[:,1] = lista[:,1]*factor	#	Compensa eje Y
			
		Pc = zeros(lista.shape)				#	Crea una nueva matriz 
		for i in range(len(lista)):		
			pto= lista[i]
			Xd = (pto.item(0) - Vl_Min[0])*(Vd_Max[0]/(Vl_Max[0] - Vl_Min[0])) # Para el eje x
			Yd = (pto.item(1) - Vl_Min[1])*(Vd_Max[1]/(Vl_Max[1] - Vl_Min[1])) # Para el eje y
			Pc[i] = [Xd, Yd]
		return Pc
		
	#-----------------------------------------------------	
		
	def grafica(self, pantalla, color, Vertices, secuencia, grueso):
		"""
			Grafica lineas entre vertices de una secuencia de indices de inicio y fin a
			sus puntos de coordenada (x, y)

		:param pantalla:	Token de la ventana creada.
		:param color:		Color de las lineas.
		:param Vertices:	coordenadas de la linea a dibujar.
		:param secuencia:	Vector de coordenada .
		:param grueso:		Grosor de las lineas.
		:return:			None
		"""

		for pto in secuencia:
			pygame.draw.line(pantalla, color, Vertices[pto.item(0)], Vertices[pto.item(1)], grueso)

	#-----------------------------------------------------	

	def grafica_ejes(self, pantalla, largo = 0, grueso = 1):
		"""
			Grafica lineas de ejes de referencias

		:param pantalla:	Token de la ventana creada
		:param largo:		Longitud de las líneas
		:param grueso:		Grosor de las líneas.
		:return:			None
		"""

		dim= pygame.display.Info()
		CentroV= dim.current_h/2
		CentroH= dim.current_w/2
		if largo > CentroV:
			largo = CentroV
		if largo > CentroH:
			largo = CentroH
					
		pygame.draw.line(pantalla, ROJO, [0, CentroV], [dim.current_w, CentroV],grueso)
		pygame.draw.line(pantalla, VERDE, [CentroH, 0], [CentroH, dim.current_h],grueso)
																	
		