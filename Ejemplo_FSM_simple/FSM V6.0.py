""" -------------------------------------------------------------
  	Máquina de Estado Finita

   	Version 5 (20-may-2018)

    -   Se define la tabla transisiones de estad para el problema
       	    imaginario -pero operativo- planteado
       	    
"""

from libs.libs_FSM.classMEF import MEF    # Se lee la clase para la Máquina de Estado

#-------------------------------------------------------------
#   Parámetros del problama

NUMERO_ESTADOS =7   #   Número de estados que requiere el problema
NUMERO_EVENTOS =4   #   Número de eventos que evalúa el estado

ESTADO_0 =      0
ESTADO_1 =      1
ESTADO_2 =      2
ESTADO_3 =      3
ESTADO_4 =      4
ESTADO_5 =      5
ESTADO_6 =      6

EVENTO_0 =      0
EVENTO_1 =      1
EVENTO_2 =      2
EVENTO_3 =      3


#-------------------------------------------------------------
#   Lista de funciones a través de una librería, tantas como se 
#   necesiten en el problema. Puede haber una acción distinta en cada
#   transición de estado

def Accion1():
    print("0",end='')

def Accion2():
    print("1",end='')

def Accion3():
    print("2",end='')
    
def Accion4():
    print("3",end='')

    
ListaAcc = {                #   Se crea la librería
    0: Accion1,
    1: Accion2,
    2: Accion3,
    3: Accion4
    }
   	
#-------------------------------------------------------------
#   M A I N
#-------------------------------------------------------------
#   Se definen los eventos de la máguina de estados
#   Para el problema de ejemplo

if __name__ == "__main__":
    
    maquina = MEF(NUMERO_ESTADOS,NUMERO_EVENTOS,ListaAcc)
    #maquina.imprime_tabla()

    maquina.incluye(ESTADO_0,EVENTO_0,'0',0,0)
    maquina.incluye(ESTADO_0,EVENTO_1,'1',1,0)
    maquina.incluye(ESTADO_0,EVENTO_2,'2',2,0)

    maquina.incluye(ESTADO_1,EVENTO_0,'0',0,0)
    maquina.incluye(ESTADO_1,EVENTO_1,'1',1,1)
    maquina.incluye(ESTADO_1,EVENTO_2,'2',1,1)

    maquina.incluye(ESTADO_2,EVENTO_0,'0',1,1)
    maquina.incluye(ESTADO_2,EVENTO_1,'1',0,0)
    maquina.incluye(ESTADO_2,EVENTO_2,'2',2,1)
    maquina.imprime_tabla()
        
    #-------------------------------------------------------------
    #   Lista de Entradas a evaluar


    entrada= "0102221110110111110"

    print()
    print("entrada =",entrada)
    #print()

    #	Procesamiento de la entrada
    #   NOTA:
    #       aunque la entrada son números la variable <char> pasa caracteres
    #       sin convertir a número (La condición de la máquina es textual)

    print("salida  =",end=' ')
    for char in entrada:
        maquina.procesa(char)
    print()
        
