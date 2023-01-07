""" -------------------------------------------------------------
  	Máquina de Estado Finita

   	Version 5 (20-may-2018)

    -   Patas para robot hexpodo con dos grados de libertad.

	-   Los comandos de entrada provienen de máquinas
	    de estado superiores
	
	    Son cuatro comandos: 
	       dec cod  comentario
	       ------------------------------------
	    -   0  PAR  pata arriba, 
	    -   1  PAB  pata abajo, 
	    -   2  MAD  secuencia de movimiento adelante
	    -   3  MAT  secuencia de movimiento atras
		
	-   Las salidas son los comandos para dos actuadores
	        bin dec cod  comentario
	        ------------------------------------
	    -   00   0  ARR  mueve pata hacia arriba
	    -   01   1  ABA  mueve pata hacia abajo
	    -   10   2  DER  mueve pata a la derecha
	    -   11   3  IZQ  mueve pata a la izquierda


"""

#------------------------------------------------------------
#   Importar librerías

import pygame
from pygame.locals import *   # Importa timer
from libs.libs_FSM.classMEF_2 import MEF    # Importa la clase para la Máquina de Estado

#-------------------------------------------------------------
#   Parámetros del problama

NUMERO_MAQUINAS = 6  #	 Es un hexapodo (6 patas)
NUMERO_ESTADOS =  8  #   Número de estados que requiere el problema
NUMERO_EVENTOS =  4  #   Número de eventos que evalúa el estado

TABLA_VACIA= False  #   Se incdica a la máquina al crearse que debe crear una tabla
                    #   de transiciones de estado vacia (se creará externamente) 

#	comandos de entrada 
	  
PAR = 0     # pata arriba, 
PAB = 1     # pata abajo, 
MAD = 2     # secuencia de movimiento adelante
MAT = 3     # secuencia de movimiento atras 

#	comandos de salida 

ARR = 0	    # mueve pata hacia arriba
ABA = 1     # mueve pata hacia abajo
DER = 2     # mueve pata a la derecha
IZQ = 3     # mueve pata a la izquierda

#-----------------------------------------------
#   Constantes

ED0 =   0
ED1 =   1
ED2 =   2
ED3 =   3
ED4 =   4
ED5 =   5
ED6 =   6
ED7 =   7

TIEMPO_TADAS = 1000     #   Para todas las màqinas 1 seg
TIEMPO_ID_0 = 1000      #   Màqinas 1, 1 seg

#-----------------------------------------------
# Definimos algunos colores

NEGRO =     (0, 0 ,0)
BLANCO =    (255, 255, 255)
VERDE =     (0, 255, 0)
ROJO =      (255, 0, 0)
AZUL =      (0, 0, 255)
VIOLETA =   (98, 0, 255)

#-------------------------------------------------------------
#   librería de funciones a través de una librería, tantas como se 
#   necesiten en el problema. Puede haber una acción distinta en cada
#   transición de estado
        
def Arriba():
    print("AR",end='  ')

def Abajo():
    print("AB",end='  ')

def Derecha():
    print("DE",end='  ')
    
def Izquierda():
    print("IZ",end='  ')
    
#-------------------------------------------------------------
#   Se crea la librería

Lista_Acciones = {
    ARR: Arriba,
    ABA: Abajo,
    DER: Derecha,
    IZQ: Izquierda
    }

#-------------------------------------------------------------
#   Rutina de simulación

def simula(Lista,entrada):
    for id in range(NUMERO_MAQUINAS):           # Para todas las máquinas..
        Lista[id].procesa(entrada[id])       # Procesa toda la entrada
    print()

#-------------------------------------------------------------
#   M A I N
#-------------------------------------------------------------
#	Se crean una máquina por pata del robot, con a misma tabla de
#	transiciones de estado, y se colocan en una lista

if __name__ == "__main__":

    pygame.init()

    id= 0                                                        		# Identificador de la máquina
    ListaMAQ =[]                                                        # Crea Lista de màquias de estado
    ListaMAQ.append( MEF(id, NUMERO_ESTADOS, NUMERO_EVENTOS, Lista_Acciones))

    #-------------------------------------------------------------
    #   Definición de la tabla de transiciones de estado para el problama 

    #	Estado 0
    ListaMAQ[id].incluye(ED0,'PAR',ED0,ARR)
    ListaMAQ[id].incluye(ED0,'PAB',ED1,ABA)
    ListaMAQ[id].incluye(ED0,'MAD',ED2,ARR)
    ListaMAQ[id].incluye(ED0,'MAT',ED5,ARR)
    
    #	Estado 1
    ListaMAQ[id].incluye(ED1,'PAR',ED0,ARR)
    ListaMAQ[id].incluye(ED1,'PAB',ED1,ABA)
    ListaMAQ[id].incluye(ED1,'MAD',ED2,ARR)
    ListaMAQ[id].incluye(ED1,'MAT',ED5,ARR)

    #	Estado 2
    ListaMAQ[id].incluye(ED2,'PAR',ED0,ARR)
    ListaMAQ[id].incluye(ED2,'PAB',ED1,ABA)
    ListaMAQ[id].incluye(ED2,'MAD',ED3,DER)
    ListaMAQ[id].incluye(ED2,'MAT',ED5,ARR)
    
    #	Estado 3
    ListaMAQ[id].incluye(ED3,'PAR',ED0,ARR)
    ListaMAQ[id].incluye(ED3,'PAB',ED1,ABA)
    ListaMAQ[id].incluye(ED3,'MAD',ED4,ABA)
    ListaMAQ[id].incluye(ED3,'MAT',ED5,ARR)
    
    #	Estado 4
    ListaMAQ[id].incluye(ED4,'PAR',ED0,ARR)
    ListaMAQ[id].incluye(ED4,'PAB',ED1,ABA)
    ListaMAQ[id].incluye(ED4,'MAD',ED0,IZQ)
    ListaMAQ[id].incluye(ED4,'MAT',ED5,ARR)

    #	Estado 5
    ListaMAQ[id].incluye(ED5,'PAR',ED0,ARR)
    ListaMAQ[id].incluye(ED5,'PAB',ED1,ABA)
    ListaMAQ[id].incluye(ED5,'MAD',ED2,ARR)
    ListaMAQ[id].incluye(ED5,'MAT',ED6,IZQ)
    
    #	Estado 6
    ListaMAQ[id].incluye(ED6,'PAR',ED0,ARR)
    ListaMAQ[id].incluye(ED6,'PAB',ED1,ABA)
    ListaMAQ[id].incluye(ED6,'MAD',ED2,ARR)
    ListaMAQ[id].incluye(ED6,'MAT',ED7,ABA)
    
    #	Estado 7
    ListaMAQ[id].incluye(ED7,'PAR',ED0,ARR)
    ListaMAQ[id].incluye(ED7,'PAB',ED1,ABA)
    ListaMAQ[id].incluye(ED7,'MAD',ED2,ARR)
    ListaMAQ[id].incluye(ED7,'MAT',ED0,DER)
    
    #-------------------------------------------------------------
    #   Se copa la tabla creada en esta máquina para ser usada 
    #   como referencia por la siguentes tablas

    TablaTransisiones = ListaMAQ[id].lee_tabla()    # Se lee y copia  la tabla

    ListaMAQ[id].imprime_tabla()                    # *** temporal +++       

        
    #-------------------------------------------------------------
    #   Crea y añade a la lista varias máquinas con  tablas de transición vacias, y copia la
    #   tabla previamente definida


    for id in range(1, NUMERO_MAQUINAS):
        ListaMAQ.append( MEF(id, NUMERO_ESTADOS, NUMERO_EVENTOS, Lista_Acciones, TABLA_VACIA))
        ListaMAQ[id].copia_tabla(TablaTransisiones)      #


    #-------------------------------------------------------------
    #   Lista de Entradas a evaluar (se actualiza en otras máquinas de estado)

    Comando= ['PAR','PAB','MAD','MAT','MAD','MAT']


    #-------------------------------------------------------------
    #   Encabezado

    for id in range(NUMERO_MAQUINAS):               # Para todas las máquinas..
        print(Comando[id],end=' ')
        
    print()    
    print(" 1   2   3   4   5   6")
    print("----------------------")
    
    #-------------------------------------------------------------
    #   Simulación
    #-------------------------------------------------------------
    # -------------------------------------------------------------   
    # Establecemos las dimensiones de la pantalla [largo,altura]

    dimensiones = [700,500]                         # width, Hight
    pantalla = pygame.display.set_mode(dimensiones) 
    pygame.display.set_caption("Prueba MEF Hexapodo")
    
    #pygame.time.set_timer(USEREVENT,1000)     # Establece cadencia de simulación en 1 segundo
    reloj = pygame.time.Clock()                 # Se usa para establecer cuan rápido se refresca la pantalla

    #-------------------------------------------------------------------
    #   Inicailiza los temporizadores de todas las máquinas

    for id in range(NUMERO_MAQUINAS):           #   Para todas las máquinas..
        ListaMAQ[id].Inicia_cadencia(1000)      #   Inicia los temporizadores de cada máquina

    #-------------------------------------------------------------------
    #   Lazo de simulación
    #-------------------------------------------------------------------

    hecho = False
    while not hecho:
        #--------------------------------------------------------------
        #   Captura de eventos

        for event in pygame.event.get():
            if event.type == QUIT:
                hecho = True

            for id in range(NUMERO_MAQUINAS):               # Para todas las máquinas..
                if event.type == USEREVENT + id:
                    #print("paso {}".format(id))
                    ListaMAQ[id].procesa(Comando[id])

            #if event.type == USEREVENT+1:
#            for id in range(NUMERO_MAQUINAS):               # Para todas las máquinas..
                #ID = event.type - USEREVENT
                #if event.type == USEREVENT:
                #    print("paso")
                    #ListaMAQ[0].procesa(Comando[0])
                    #print(str(event.type) +" "+ str(id))

        #--------------------------------------------------------------
        #   visulización en pantalla
                
        pantalla.fill(BLANCO)

        # --- EL CÓDIGO DE DIBUJO DEBERÍA IR AQUÍ
	
 	
        pygame.display.flip()   # --- Avanzamos y actualizamos la pantalla con lo que hemos dibujado.
        reloj.tick(60)          # --- Limitamos a 60 fotogramas por segundo (frames per second)

    pygame.quit()
           
