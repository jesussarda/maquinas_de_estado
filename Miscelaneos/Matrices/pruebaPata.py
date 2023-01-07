
'''
Created on 25/6/2019

@author: Jesús Enrique Sardá
'''

from math import *
import pygame
from  numpy import *
# from  ClaseModeloNumpy import *
from PatasRobot import *
import sys

#----------------------------------------------------------------
#	Par�metros geomn�tricos del problema


ESCALA =   			100
LIMAXIS =			20
NUMERO_LADOS = 		12
NUMERO_VERTICES = 	8

#----------------------------------------------------------------
#	Par�metros geomn�tricos del problema

def grafica_ejes(pantalla, largo, grueso):
	"""
		Grafica lineas de ejes dd referncias 
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
	pygame.display.set_caption("Prueba clase matrices de transformaciones ")

	# -------------------------------------------------------------   
	#   El bucle se ejecuta hasta que el usuario hace click sobre el bot�n de cierre.

	hecho = False

	reloj = pygame.time.Clock() # Se usa para establecer cuan r�pido se actualiza la pantalla
		
		
	#-----------------------------------------------------
	
	#Modelo= Modela()
		
	Lambda = 	30			# Distancia focal
	D= 			50			# Distancia del modelo al plano de proyeccion
	P= 			5			# Distancia entre las patas

	L=			4.24		# Largo de los lados
	Lc=			5
	Lx=			3			# Largo de los lados
	Ly=			3			# Largo de los lados

	PATAS	= 	6
	
	#-----------------------------------------------------
	#	Coordenadas del Modelo:	cubo
	#-----------------------------------------------------
	#	Coordenadas de los vertices de un cubo de lado 2L en el espacio
	#	a una distancia D del plano de proyeccion, usanso lente con distancia
	#	focal L
		
	#	Modelo pata derecha abajo

	p01= [   0,    0,    D]
	p11= [ -Lx,  -Ly,    D]
	p21= [ -Lx, -(Ly+L), D]

	Lista1 = matrix([p01, p11, p21])		# Lista de coordenadas  de los vertices
		
	#	Modelo pata izquierda abajo

	p02= [   0,    0,    D]
	p12= [  Lx,  -Ly,    D]
	p22= [  Lx, -(Ly+L), D]

	Lista2 = matrix([p02, p12, p22])		# Lista de coordenadas  de los vertices

	#	Modelo pata derecha arriba
	
	p03= [   0,    0,    D+P]
	p13= [ -Lx,  -Ly,    D+P]
	p23= [ -Lx, -(Ly+L), D+P]

	Lista3 = matrix([p03, p13, p23])		# Lista de coordenadas  de los vertices
		
	#	Modelo pata izquierda arriba

	p04= [   0,    0,    D+P]
	p14= [  Lx,  -Ly,    D+P]
	p24= [  Lx, -(Ly+L), D+P]

	Lista4 = matrix([p04, p14, p24])		# Lista de coordenadas  de los vertices

	#	Modelo pata derecha arriba
	
	p05= [   0,    0,    D+2*P]
	p15= [ -Lx,  -Ly,    D+2*P]
	p25= [ -Lx, -(Ly+L), D+2*P]

	Lista5 = matrix([p05, p15, p25])		# Lista de coordenadas  de los vertices
		
	#	Modelo pata izquierda arriba

	p06= [   0,    0,    D+2*P]
	p16= [  Lx,  -Ly,    D+2*P]
	p26= [  Lx, -(Ly+L), D+2*P]

	Lista6 = matrix([p06, p16, p26])		# Lista de coordenadas  de los vertices

	Lista = [Lista1, Lista2, Lista3, Lista4, Lista5, Lista6]
	cuerpo = [p01, p02, p03, p04, p05, p06]
	
	#-----------------------------------------------------
	#	Modelo:	cubo, Secuencia de pares de puntos para la generacion de
	# 	lineas -los lados del cubo-
	
	verticesPata = matrix([[0, 1], [1, 2]])	
	
	seccuerpo = matrix([[0, 1], [2, 3], [4, 5], [0, 2],  [1, 3], [2, 4], [2, 4], [3, 5]])	

	angulo = random.randint(0,90,size=6)
	signo = [1, -1, 1 , -1 , 1, -1]
	
	PosicionPatas = [[-5, 2, 0 ],[ 5, 2, 0 ],[-5, 2, 0 ],[ 5, 2, 0 ],[-5, 2, 0 ],[ 5, 2, 0 ]]
	
	colores = [VIOLETA,VERDE,VIOLETA,VERDE,VIOLETA,VERDE]
	
	if D  <= Lambda:
		sys.exit("La distancia del punto en Z no puede ser inferior a la distancia focal")
			
	pata= []
	for i in range(PATAS):
		pata.append( ModeloPata(Lista[i], verticesPata, PosicionPatas[i], Lambda, signo[i])) 

	#-----------------------------------------------------
	
	while not hecho:

		# --- Bucle principal de eventos

		for evento in pygame.event.get():
			if evento.type == pygame.QUIT: 
				hecho = True
	
		pantalla.fill(BLANCO)

		# ***** grafica aqui ***

		for i in range(PATAS):
			
			if( angulo[i] > 90):
				angulo[i] = 0
				
			pata[i].mueve_pata_arriba(angulo[i])
			pata[i].grafica(pantalla, colores[i], LIMAXIS, 7)
							
		grafica_ejes(pantalla,100, 1)
		
		# --- Aanzamos y actualizamos la pantalla con lo que hemos dibujado.

		pygame.display.flip()

		# --- Limitamos a 60 fotogramas por segundo (frames per second)

		reloj.tick(5)
		
		for i in range(PATAS):
			angulo[i] += 10
			
	
	# ------------------------------------------------------------   
	# Cerramos la ventana y salimos.
	# Si te olvidas de esta �ltima l�nea, el programa se 'colgar�'
	# al salir si lo hemos estado ejecutando desde el IDLE.

	pygame.quit()
	

