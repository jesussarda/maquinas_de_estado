'''
Created on 25/6/2019

@author: Jesùs Enrique Sardá
'''

import pygame
from  numpy import  matrix, random
from  ClaseModeloNumpy import Modela, VIOLETA, VERDE, BLANCO, DOS_D
import sys


#----------------------------------------------------------------
#	Parámetros geomnétricos del problema


ESCALA =   			100
LIMAXIS =			20
NUMERO_LADOS = 		12
NUMERO_VERTICES = 	8
PASO =				10



#-------------------------------------------------------------


def Procesa_rot(Modelo, Lista, angulo, focal, Tra):
	"""
		Para la instancia <Modelo> se rota punto de una figura en <lista> un cierto <angulo>,
	:param Modelo:
	:param Lista:
	:param angulo:
	:param focal:
	:param Tra:
	:return:
	"""
	acumula = Modelo.convierte_a_homogenea(Lista)			# Convierte coordenadas a Homogénea (la matriz resuttado queda acumulada)
	Modelo.RotaZ(angulo)						# Rota pata respecto al centro del eje
	Modelo.traslada(Tra[0], Tra[1], Tra[2])		# Traslada eje de coordenadas a un lado
	Modelo.perspectiva(focal)					# Convierte a para vista en perspectiva
	return Modelo.convierte_a_normal(DOS_D)		# Convierte coordenadas a Homogénea y traspone para operar

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
	#   El bucle se ejecuta hasta que el usuario hace click sobre el botón de cierre.

	hecho = False

	reloj = pygame.time.Clock() # Se usa para establecer cuan rápido se actualiza la pantalla
		
		
	#-----------------------------------------------------
	
	#Datos= Matriz()		# Instancia de clase matriz
	Modelo1= Modela()		# Instancia de clase modelo
	Modelo2= Modela()		# Instancia de clase modelo
	Modelo3= Modela()		# Instancia de clase modelo
	Modelo4= Modela()		# Instancia de clase modelo
	Modelo5= Modela()		# Instancia de clase modelo
	Modelo6= Modela()		# Instancia de clase modelo
	
	Modelo = [Modelo1, Modelo2, Modelo3, Modelo4, Modelo5, Modelo6]
	
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
	
	sec = matrix([[0, 1], [1, 2]])	
	
	seccuerpo = matrix([[0, 1], [2, 3], [4, 5], [0, 2],  [1, 3], [2, 4], [2, 4], [3, 5]])	

	angulo1 = 0

	"""
	angulo2 = 15
	angulo3 = 25
	"""
	angulo = 90*random.rand(90)
	signo = [1, -1, 1 , -1 , 1, -1]
	
	angulo[1] *= -1
	angulo[3] *= -1
	angulo[5] *= -1
	
	Traslacion = [[-5, 2, 0 ],[ 5, 2, 0 ],[-5, 2, 0 ],[ 5, 2, 0 ],[-5, 2, 0 ],[ 5, 2, 0 ]]
	
	colores = [VIOLETA,VERDE,VIOLETA,VERDE,VIOLETA,VERDE]
	
	if D  <= Lambda:
		sys.exit("La distancia del punto en Z no puede ser inferior a la distancia focal")
		
	#Pn = Procesa_rot(Modelo, Lista,  angulo, Lambda)
	#Pc = Modelo.mapea_en_pantalla(Pn,[LIMAXIS,LIMAXIS],[-LIMAXIS,-LIMAXIS],[dimensiones[0],dimensiones[1]])
	#Modelo.imprime_Matriz(" pata", Pn, 2)	

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

		if angulo1 > 90:
			angulo1= 0
		
		for i in range(PATAS):			
			if( angulo[i] > 90):
				angulo[i]= 0

		for i in range(PATAS):			
			Pn = Procesa_rot(Modelo[i], Lista[i],  signo[i]*angulo[i], Lambda, Traslacion[i])
			Pc = Modelo[i].mapea_en_pantalla(Pn,[LIMAXIS,LIMAXIS],[-LIMAXIS,-LIMAXIS],[dimensiones[0],dimensiones[1]])
			Modelo1.grafica(pantalla, colores[i], Pc, sec, 7)
		
#		Modelo1.grafica_ejes(pantalla, 100,  3)
		Modelo1.grafica_ejes(pantalla, grueso = 3)
#		Modelo1.grafica_ejes(pantalla)

		# --- Aanzamos y actualizamos la pantalla con lo que hemos dibujado.

		pygame.display.flip()

		# --- Limitamos a 60 fotogramas por segundo (frames per second)

		reloj.tick(5)
		
		for i in range(PATAS):
			angulo[i] += PASO
			
	
		angulo1 += PASO
		"""	
		angulo2 += 10
		angulo3 += 5s
		"""
	# ------------------------------------------------------------   
	# Cerramos la ventana y salimos.
	# Si te olvidas de esta última línea, el programa se 'colgará'
	# al salir si lo hemos estado ejecutando desde el IDLE.

	pygame.quit()
	
