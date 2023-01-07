from math import *
import pygame
from  matrices import *

# Definimos algunos colores

NEGRO = 	(0, 0 ,0)
BLANCO = 	(255, 255, 255)
VERDE = 	(0, 255, 0)
ROJO = 		(255, 0, 0)
AZUL = 		(0, 0, 255)
VIOLETA = 	(98, 0, 255)

#----------------------------------------------------------------
#	Parametros geomnetricos del problema

ESCALA =    100
LIMAXIS =   30

D= 			50
L=			10
Lambda = 	10
lados = 	12
vertices = 	8

#-------------------------------------------------------------
#   M A I N
#-------------------------------------------------------------

if __name__ == "__main__":


	# -------------------------------------------------------------   
	# Inicia motor gráfico

	pygame.init()

	# -------------------------------------------------------------   
	# Establecemos las dimensiones de la pantalla [largo,altura]

	dimensiones = [700,500]     # width, Hight
	pantalla = pygame.display.set_mode(dimensiones) 
	pygame.display.set_caption("Prueba matrices de transformaciones ")

	# -------------------------------------------------------------   
	#   El bucle se ejecuta hasta que el usuario hace click sobre el botón de cierre.

	hecho = False

	reloj = pygame.time.Clock() # Se usa para establecer cuan rápido se actualiza la pantalla

	#-----------------------------------------------------
	#	Matrices  de transformación
	#-----------------------------------------------------

	#-----------------------------------------------------
	# Traslacion, matriz homogenea
		
	Xo = 8		#	Translada distancia en el eje  X
	Yo = 5		#	Translada distancia en el eje  Y
	Zo = 0		#	Translada distancia en el eje  Z
		
	Tra =  [[1, 0, 0, Xo],
		[0, 1, 0, Yo],
		[0, 0, 1, Zo],
		[0, 0, 0,  1]]
	
	#imprimeMatriz("Traslacion",Tra)

	#-----------------------------------------------------
	# Escalado
	
	Sx = 100;
	Sy = 100;
	Sz = 100;
	
	Esc = [[ Sx, 0,  0,  0],
                [0, Sy,  0,  0],
		[0,  0, Sz,  0],
		[0,  0,  0,  1]]

	#imprimeMatriz("Escalamiento",Esc)
	
	#-----------------------------------------------------
	# Rotacion un angulo  alrededor del eje Z

	theta = 30				#	Angulo de rotacion respecto al eje z
	theta = theta*pi/180

	Roz = [ [ cos(theta), sin(theta), 0,  0],
		[-sin(theta), cos(theta), 0,  0],
		[	0,          0,        1,  0],
		[	0,          0,        0,  1]]

	#imprimeMatriz("Rotacion respecto Z",Roz)

	#-----------------------------------------------------
	# Rotacion un angulo  alrededor del eje x

	alfa = 30				#	Angulo de rotacion respecto al eje x
	alfa = alfa*pi/180
	Rox = [ [1,     0,         0,      0],
		[0,  cos(alfa), sin(alfa), 0],
		[0, -sin(alfa), cos(alfa), 0],
		[0,     0,         0,      1]]

	#imprimeMatriz("Rotacion respecto X",Rox)

	#-----------------------------------------------------
	# Rotacion un angulo  alrededor del eje y

	beta = 45				#	Angulo de rotacion respecto al eje y
	beta = beta*pi/180
	Roy = [ [ cos(beta), 0, -sin(beta), 0],
		[    0,      1,      0,     0],
		[ sin(beta), 0,  cos(beta), 0],
		[    0,      0,      0,     1]]
			
	#imprimeMatriz("Rotacion respecto Y",Roy)

	#-----------------------------------------------------
	#	Transformacion en Perspectiva 
	#	NOTA: 	
	#		- 	Para un punto de coordenada en el espacio 
	#			(X,Y,Z) al transformar en homogenea se debe multiplicar
	#			por ubna constante K arbitraria: 

	#			(	X, Y, Z, 1)*K = (KX, KY, KZ, K)

	#		- 	Después de hacer las transformaciones correspondientes
	#			el resultado es una coordenada homogenea. Para convertila 
	#			a coordenada normal, se dividen las tres primeros elementos
	#			entra el cuarto, pero como es una proyección al plano xy
	#			la ccordenada z resultante no tiene significado, por lo que se
	#			descarta
	#				(xh,yh,zh, val) -> (xh,yh,zh)/val = (x,y,z) -> (x,y)

	# 	Lambda = 

	K = 1;

	Per = [ [ 1,    0,     0,      0],
		[ 0,    1,     0,      0],
		[ 0,    0,     1,      0],
		[ 0,    0, -1/Lambda,  1]]

	#imprimeMatriz("Perspectiva",Per)

	#-----------------------------------------------------

	#-----------------------------------------------------
	#	Coordenadas del modelo
	#-----------------------------------------------------
	#	Coordenadas de los vértices de un cubo de lado 2L en el espacio
	#	a una distancia D del plano de proyección, usanso lente con distancia
	#	focal L

	p1= [-L, -L, D]
	p2= [-L,  L, D]
	p3= [ L, -L, D]
	p4= [ L,  L, D]
	p5= [-L, -L, D+L]
	p6= [-L,  L, D+L]
	p7= [ L, -L, D+L]
	p8= [ L,  L, D+L]

	Lista = [p1, p2, p3, p4, p5, p6, p7, p8]	# Lista de puntos  de vertices
	imprimeMatriz("Lista de vertices  =         ",Lista)
	
	#-----------------------------------------------------
	#	Secuencia de pares de puntos para la generación de
	# lineas -lados del cubo-
	
	#sec = [[1, 2], [1, 3], [3, 4], [2, 4], [5, 6], [5, 7], [7, 8], [6, 8], [1, 5], [2, 6], [3, 7], [4, 8]]
	sec = [[0, 1], [0, 2], [2, 3], [1, 3], [4, 5], [4, 6], [6, 7], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]]

	Ph= homogenea(Lista)
	imprimeMatriz("Ph - Lista homogenea de vertices= ",Ph)
		
	Ph =  traspuesta(Ph)
	imprimeMatriz("Ph - Lista traspuesta de vertices=",Ph)
		
	#	Operaciones

	#Ph = multiplicaMatriz(Esc,Ph)					#	Escala uniformmente 
	#Ph = multiplicaMatriz(Tra,Ph)					#	Traslada 
	Ph = multiplicaMatriz(Roz,Ph) 	#	Rota en torno a eje z
	Ph = multiplicaMatriz(Roy,Ph) 	#	Rota en torno a eje y
	Ph = multiplicaMatriz(Rox,Ph)	#	Rota en torno a eje x
		
	Po = multiplicaMatriz(Per, Ph)
	imprimeMatriz("Po - Puntos de perspectiva=", Po)
		
	Pn = normaliza(Po,2)
	imprimeMatriz("Pn - Coordenadas x, y mormalizadas=", Pn)
		
	Pn = traspuesta(Pn)
	imprimeMatriz("Pn - Coordenadas traspuesta", Pn)
	
	Pc = mapea(Pn,[LIMAXIS,LIMAXIS],[-LIMAXIS,-LIMAXIS],[dimensiones[1],dimensiones[1]])
	imprimeMatriz("Pc - Coordenadas dispositivo", Pc)
	
	#-----------------------------------------------------

	while not hecho:

		# --- Bucle principal de eventos

		for evento in pygame.event.get():
			if evento.type == pygame.QUIT: 
				hecho = True
	
		# Primero, limpia la pantalla con blanco. No vayas a poner otros comandos de dibujo encima 
		# de esto, de otra forma serán borrados por este comando:

		pantalla.fill(BLANCO)

		# ***** grafica aqui ***

		grafica(pantalla, ROJO, Pc, sec)

		# --- Avanzamos y actualizamos la pantalla con lo que hemos dibujado.

		pygame.display.flip()

		# --- Limitamos a 60 fotogramas por segundo (frames per second)

		reloj.tick(60)

	# -------------------------------------------------------------   
	# Cerramos la ventana y salimos.
	# Si te olvidas de esta última línea, el programa se 'colgará'
	# al salir si lo hemos estado ejecutando desde el IDLE.

	pygame.quit()
	
	#-------------------------------------------------------------
	#   Ejecuta M A I N
	
