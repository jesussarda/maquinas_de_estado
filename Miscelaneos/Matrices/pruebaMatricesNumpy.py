from math import *
import pygame
from  numpy import *
#from  ClaseMatrices import *
from  ClaseModeloNumpy import *

# Definimos algunos colores

#NEGRO = 	(0, 0 ,0)
#BLANCO = 	(255, 255, 255)
#VERDE = 	(0, 255, 0)
#ROJO = 		(255, 0, 0)
#AZUL = 		(0, 0, 255)
#VIOLETA = 	(98, 0, 255)

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

def main():

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
	#Modelo.imprime_Matriz("Lista - Coordenadas delodelo", Lista, 2)
		
	#-----------------------------------------------------
	#	Modelo:	cubo, Secuencia de pares de puntos para la generacion de
	# 	lineas -los lados del cubo-
	
	sec = matrix([[0, 1], [0, 2], [2, 3], [1, 3], [4, 5], [4, 6], [6, 7], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]])

	Ph = Modelo.convierte_a_homogenea(Lista)		# Convierte coordenadas a Homogenea y traspone para poder operar
	#Modelo.imprime_Matriz("Ph - Coordenadas homogeneas", Ph, 2)
	
	#	Operaciones

	Ph = Modelo.traslada(Ph, -20, 0, 0)	
	Ph = Modelo.RotaZ(Ph, 15)
	#Ph = Modelo.RotaY(Ph, 30)
	#Ph = Modelo.RotaX(Ph, 30)		
	
	Ph = Modelo.proyecta_vista(Ph,20)
	#Modelo.imprime_Matriz("Ph - Coordenadas de vista", Ph, 2)
		
	Pn = Modelo.convierte_a_normal(Ph, DOS_D)		# Convierte coordenadas a Homogenea y traspone paraoperar
	#Modelo.imprime_Matriz("Po - Coordenadas normales", Pn, 2)
	
	Pc = Modelo.mapea_en_pantalla(Pn,[LIMAXIS,LIMAXIS],[-LIMAXIS,-LIMAXIS],[dimensiones[0],dimensiones[1]])
	#Modelo.imprime_Matriz("Pc - Coordenadas dispositivo", Pc, 2)
	
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

		Modelo.grafica(pantalla, NEGRO, Pc, sec)
		Modelo.grafica_ejes(pantalla,100,1)
		
		# --- Aanzamos y actualizamos la pantalla con lo que hemos dibujado.

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
	
if __name__ == "__main__":
		
	main()
