from math import *
import pygame
from  numpy import *
#from  ClaseMatrices import *
from  ClaseModeloNumpy import *

#----------------------------------------------------------------
#	Parametros geomnetricos del problema

DOS_D =		2
TRES_D =	3

ESCALA =   			100
LIMAXIS =			30
NUMERO_LADOS = 		12
NUMERO_VERTICES = 	8


#-------------------------------------------------------------

def Procesa_tra_rot(Modelo, Lista, Tra, angulo, foco):
#	Modelo.convierte_a_homogenea(Lista)		# Convierte coordenadas a Homogenea (el resuktado queda acumulado)
	Modelo.convierte_a_homogenea_acu(Lista)		# Convierte coordenadas a Homogenea (el resuktado queda acumulado)
	Modelo.traslada_acu(Tra[0], Tra[1], Tra[2])
	Modelo.RotaZ_acu(angulo)
	Modelo.proyecta_vista_acu(foco)
	return Modelo.convierte_a_normal_acu(DOS_D)		# Convierte coordenadas a Homogenea y traspone paraoperar
#	return Modelo.convierte_a_normal(DOS_D)		# Convierte coordenadas a Homogenea y traspone paraoperar

#-------------------------------------------------------------
#   M A I N
#-------------------------------------------------------------

if __name__ == "__main__":

	# -------------------------------------------------------------   
	# Inicia motor gráfico

	pygame.init()

	# -------------------------------------------------------------   
	# Establecemos las dimensiones de la pantalla [largo,altura]

	dimensiones = [500,700]     # width, Hight
	pantalla = pygame.display.set_mode(dimensiones) 
	pygame.display.set_caption("Prueba clase matrices de transformaciones ")

	# -------------------------------------------------------------   
	#   El bucle se ejecuta hasta que el usuario hace click sobre el botón de cierre.

	hecho = False

	reloj = pygame.time.Clock() # Se usa para establecer cuan rápido se actualiza la pantalla
		
		

	#imprimeMatriz("Perspectiva",Per)

	#-----------------------------------------------------
	
	#Datos= Matriz()			# Instancia de clase matriz
	Modelo= Modela()		# Instancia de clase modelo
	
	D= 			50			# Distancia del modelo al plano de proyeccion
	L=			10			# Largo de los lados
	Lambda = 	50			# Distancia focal

	#-----------------------------------------------------
	#	Coordenadas del Modelo:	cubo
	#-----------------------------------------------------
	#	Coordenadas de los vertices de un cubo de lado 2L en el espacio
	#	a una distancia D del plano de proyeccion, usanso lente con distancia
	#	focal L
		
	p1= [-L, -L, D]
	p2= [-L,  L, D]
	p3= [ L, -L, D]
	p4= [ L,  L, D]
	p5= [-L, -L, D + 2*L]
	p6= [-L,  L, D + 2*L]
	p7= [ L, -L, D + 2*L]
	p8= [ L,  L, D + 2*L]

	Lista = matrix([p1, p2, p3, p4, p5, p6, p7, p8])		# Lista de coordenadas  de los vertices
		
	#-----------------------------------------------------
	#	Modelo:	cubo, Secuencia de pares de puntos para la generacion de
	# 	lineas -los lados del cubo-
	
	sec = matrix([[0, 1], [0, 2], [2, 3], [1, 3], [4, 5], [4, 6], [6, 7], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]])
	
	#Pn = Procesa_tra_rot(Modelo, Lista, [-20, 0, 0], 15, 20)
	#Pc = Modelo.mapea_en_ventana(Pn,[LIMAXIS,LIMAXIS],[-LIMAXIS,-LIMAXIS],[dimensiones[0],dimensiones[1]])

	#-----------------------------------------------------
	angulo = 0
	while not hecho:

		# --- Bucle principal de eventos

		for evento in pygame.event.get():
			if evento.type == pygame.QUIT: 
				hecho = True
	
		# Primero, limpia la pantalla con blanco. No vayas a poner otros comandos de dibujo encima 
		# de esto, de otra forma serán borrados por este comando:

		pantalla.fill(BLANCO)

		# ***** grafica aqui ***

		Pn = Procesa_tra_rot(Modelo, Lista, [-30, 0, 0], angulo, 20)
		Pc = Modelo.mapea_en_pantalla(Pn,[LIMAXIS,LIMAXIS],[-LIMAXIS,-LIMAXIS],[dimensiones[0],dimensiones[1]])
		Modelo.grafica(pantalla, NEGRO, Pc, sec,2)
		Modelo.grafica_ejes(pantalla,100,2)
		
		# --- Aanzamos y actualizamos la pantalla con lo que hemos dibujado.

		pygame.display.flip()

		# --- Limitamos a 60 fotogramas por segundo (frames per second)

		reloj.tick(10)
		angulo += 5
	# -------------------------------------------------------------   
	# Cerramos la ventana y salimos.
	# Si te olvidas de esta última línea, el programa se 'colgará'
	# al salir si lo hemos estado ejecutando desde el IDLE.

	pygame.quit()
	
