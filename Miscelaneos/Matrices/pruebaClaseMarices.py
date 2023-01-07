from math import *
import pygame
from  ClaseMatrices import *
from  ClaseModelo import *

# Definimos algunos colores

NEGRO = 	(0, 0 ,0)
BLANCO = 	(255, 255, 255)
VERDE = 	(0, 255, 0)
ROJO = 		(255, 0, 0)
AZUL = 		(0, 0, 255)
VIOLETA = 	(98, 0, 255)

#----------------------------------------------------------------
#	Parametros geomnetricos del problema

DOS_D =		2
TRES_D =	3

ESCALA =   			100
LIMAXIS =			30
NUMERO_LADOS = 		12
NUMERO_VERTICES = 	8


#-------------------------------------------------------------
#   M A I Nº
#-------------------------------------------------------------

if __name__ == "__main__":

	# -------------------------------------------------------------   
	# Inicia motor gráfico

	pygame.init()

	# -------------------------------------------------------------   
	# Establecemos las dimensiones de la pantalla [largo,altura]

	dimensiones = [700,500]     # width, Hight
	pantalla = pygame.display.set_mode(dimensiones) 
	pygame.display.set_caption("Prueba clase matrices de transformaciones ")

	# -------------------------------------------------------------   
	#   El bucle se ejecuta hasta que el usuario hace click sobre el botón de cierre.

	hecho = False

	reloj = pygame.time.Clock() # Se usa para establecer cuan rápido se actualiza la pantalla
		
		

	#imprimeMatriz("Perspectiva",Per)

	#-----------------------------------------------------
	
	Datos= Matriz()			# Instancia de clase matriz
	Modelo= Modela()		# Instancia de clase modelo
	
	D= 			50			# Distancia del modelo al plano de proyeccion
	L=			5			# Largo de los lados
	Lambda = 	10			# Distancia focal

	#-----------------------------------------------------
	#	Coordenadas del Modelo:	cubo
	#-----------------------------------------------------
	#	Coordenadas de los vertices de un cubo de lado 2L en el espacio
	#	a una distancia <D> del plano de proyeccion, usanso lente con distancia
	#	focal L

	p1= [-L, -L, D]
	p2= [-L,  L, D]
	p3= [ L, -L, D]
	p4= [ L,  L, D]
	p5= [-L, -L, D+L]
	p6= [-L,  L, D+L]
	p7= [ L, -L, D+L]
	p8= [ L,  L, D+L]

	Lista = [p1, p2, p3, p4, p5, p6, p7, p8]		# Lista de coordenadas  de los vertices

	#-----------------------------------------------------
	#	Modelo:	cubo, Secuencia de pares de puntos para la generacion de
	# 	lineas -los lados del cubo-
	
	sec = [[0, 1], [0, 2], [2, 3], [1, 3], [4, 5], [4, 6], [6, 7], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]]

	Ph = Modelo.convierte_coordenadas(Lista)		# Convierte coordenadas a Homogenea y traspone para poder operar
	
	#	Operaciones

	Ph = Modelo.traslada(Ph, -30,-5, -10)
	#Ph = Modelo.escala(Ph, 100,100,100)
	Ph = Modelo.RotaZ(Ph, 45)
	#Ph = Modelo.RotaY(Ph, 30)
	#Ph = Modelo.RotaX(Ph, 30)
		
	Po = Modelo.proyecta_vista(Ph,20)
	Datos.imprimeMatriz("Coordenadas vista", Po)
		
	Pn = Modelo.repone_coordenadas(Po, DOS_D)		# Convierte coordenadas a Homogenea y traspone paraoperar
	Datos.imprimeMatriz("Coordenadas normalizadas", Pn)
	
	Pc = Modelo.mapea_en_ventana(Pn,[LIMAXIS,LIMAXIS],[-LIMAXIS,-LIMAXIS],[dimensiones[1],dimensiones[1]])
	Datos.imprimeMatriz("Coordenadas dispositivo", Pc)
	

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

		Modelo.grafica(pantalla, ROJO, Pc, sec)

		# --- Avanzamos y actualizamos la pantalla con lo que hemos dibujado.

		pygame.display.flip()

		# --- Limitamos a 60 fotogramas por segundo (frames per second)

		reloj.tick(60)

	# -------------------------------------------------------------   
	# Cerramos la ventana y salimos.
	# Si te olvidas de esta última línea, el programa se 'colgará'
	# al salir si lo hemos estado ejecutando desde el IDLE.

	pygame.quit()
	

