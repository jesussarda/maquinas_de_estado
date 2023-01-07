""" -------------------------------------------------------------
  	Máquina de Estado Finita

   	Version 2 (17-may-2018
   	-   	Se crea la clase MEF que resuelve los problemas de la version V1
   		con los atributos
   		
   		<tablaEstados> 
   			que es la tabla de estados. La tabla de estados no 
   			se crea directamente, ni en forma clásica. Se usa el modo compacto para
       		crear la matriz - que es menos obvia -
        <estadoActual>
        	el estado en el paso actual
 		<cuenta>
 			que  cuenta le número de pasos
 			
 		y los métodos
 		
 		<incluye>
 			para añadir eventos a la tabla
 		<imprime_tabla>
 			para imprimir oa tabla de estados
 		<procesa>
 			que procesa un paso o cambio de estado de la máquina

   	-   Se crea una librería de funciones que procesan acciones de
   		la máquina y la función  <Ejecuta> para escoger una función
   		a partir de un índice
       
	-	Al contrasio de la versión V1 se crea la función <main> que 
		encierra todo, al estilo de main de C/C++, para mejorar el
		estilo de la programación (el interprete pyhton es dependiente de la 
		indentación)
		
	-------------------------------------------------------------
	NOTA:
   		Cada estado contiene una lista de eventos.
   		Cada evento tiene información de:
   		<código del evento>     o condición a evaluar,
   		<estado siguiente>      si se cumple el evento
   		<acción a realizar>     o indice a la acción para ese evento de la librería de acciones 
                           		a realizar
"""
NUMERO_ESTADOS =3   #   Número de estados que requiere el problema
NUMERO_EVENTOS =3   #   Número de eventos que evalúa el estado
NUMERO_ITEMS =  3   #   Tripleta de atributos: código de evento o condición, 
                    #   estado siguiente e índice de acción que tiene cada evento

ESTADO_0 =      0
ESTADO_1 =      1
ESTADO_2 =      2

EVENTO_0 =      0
EVENTO_1 =      1
EVENTO_2 =      2

CONDICION =     0
EDOSIGUIENTE=   1
ACCION =        2

#-------------------------------------------------------------
#   Lista de funciones a través de una librería, tantas como se 
#	necesiten en el problema

def Accion1():
    print("0",end='')

def Accion2():
    print("1",end='')

def Accion3():
    print("2",end='')

    
ListaAcciones = {                #   Se crea la librería
    0: Accion1,
    1: Accion2,
    2: Accion3
    }

#-------------------------------------------------------------
#   Se ejecuta la rutina de acción indicada por
#   el <indice> obtenida de la librería

def Ejecuta(indice):
        func= ListaAcciones.get(indice)     # Se obtiene una función de la librerìa
        return func()                       # y se ejecuta
   
   
#-------------------------------------------------------------
#   Clase Máquina de Estado Finita (MEF) 
#-------------------------------------------------------------

class MEF:
    
    #--------------------------------------------------------
    #   Constructor
    # 	Crea e inicia una tabla de estados (Modo compacto)
    
    def __init__(self, estados, eventos):
        self.tablaEstados = [0]*NUMERO_ESTADOS                          # Crea lista de ceros
        for estado in range(NUMERO_ESTADOS):
            self.tablaEstados[estado]= [0]*NUMERO_EVENTOS               # Crea lista de ceros dentro de la lista
            for condicion in range(NUMERO_EVENTOS):
                self.tablaEstados[estado][condicion]= [0]*NUMERO_ITEMS  # Crea lista de ceros dentro de la lista
                self.tablaEstados[estado][condicion][0]="#"             # Acttualiza solo el primer item de la nueva lista

        self.estadoActual= 0                                            # Estado en un paso de ejecución
        self.cuenta = 0                                                 # Contador de pasos de ejecución
	
    #--------------------------------------------------------
    #   incluye 
    # 	Se añade la definición del <evento> de un <estado>
    # 	definido en la tripleta 
    #	<condicion>, <siguiente> y <accion>

    def incluye(self,estado,evento,condicion,siguiente,accion):
        if estado < NUMERO_ESTADOS and evento  < NUMERO_EVENTOS:
            self.tablaEstados[estado][evento][CONDICION]= condicion
            self.tablaEstados[estado][evento][EDOSIGUIENTE]= siguiente
            self.tablaEstados[estado][evento][ACCION]= accion
        else:
            print("** ERROR: Parámetro estado o evento muy alto ***")
            
    #-------------------------------------------------------------
    # Imprime el contenido de la table de estados

    def imprime_tabla(self):
        print()
        print("------------------- Tabla de estados --------------------- ")
        for estado in range(NUMERO_ESTADOS):
            print("estado ", estado, end= '  ')
            print(self.tablaEstados[estado])
        print("----------------------------------------------------------")
        print()
     
    #-------------------------------------------------------------
    # Procesa un paso de la maqiona de estados

    def procesa(self, entrada):
        estado = self.tablaEstados[self.estadoActual]       #   Lee registro de estado
        for evento in estado:                               #   Evalua todos los eventos en el registro
            if entrada == evento[CONDICION]:                #   La entrada es un evento registrado?
                Ejecuta(evento[ACCION])                     #   Se ejecuta la accion para ese evento
                self.estadoActual = evento[EDOSIGUIENTE]    #   Actualiza el estado actual

                #print(" Entrada= ", evento[CONDICION]," Estado Siguiente= ", evento[EDOSIGUIENTE]," Accion= ", evento[ACCION])
	
#-------------------------------------------------------------
#   M A I N
#-------------------------------------------------------------
#   Se definen los eventos de la máguina de estados

def main():
    
    maquina = MEF(NUMERO_ESTADOS,NUMERO_EVENTOS)
    maquina.imprime_tabla()

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
        
#-------------------------------------------------------------
#   ejecuta main

if __name__ == "__main__":
    
    main()
