""" -------------------------------------------------------------
    clase Máquina de Estado Finita

    Version 2 (21-may-2018)

    -   Se crea la clase MEF que resuelve los problemas de la version V1
        con los atributos

        <tablaEstados>
            que es la tabla de estados. La tabla de estados no
            se crea directamente, ni en forma clásica. Se usa el modo compacto para
                crear la matriz - que es menos obvia -
                <ListaAcciones>
                una lista que contiene todas las funciones definidas externamente para
                el problema, usadas en la tabla de estado a través de un indice
                o código único.
                <estadoActual>
                el estado de la transición actual
                <cuenta>
            que  cuenta le número de pasos

        y los métodos
 
                <ejecuta>
                    que obtiene la función de acción definida por un <indice>
                    de una lista.
                <incluye>
                    para añadir eventos a la tabla
                <imprime_tabla>
                    para imprimir oa tabla de estados
                <procesa>
                    que procesa un paso o cambio de estado de la máquina

    -------------------------------------------------------------
    NOTA:
        Cada estado contiene una lista de eventos.
        Cada evento tiene información de:
        <código del evento>     o condición a evaluar,
        <estado siguiente>      transición si se cumple el evento
        <acción a realizar>     o indice a la acción para ese evento de la librería de acciones
                                a realizar
"""   

import pygame
from pygame.locals import *   # Importa timer
from threading import Timer

#-------------------------------------------------------------
#   Constantes

CONDICION =     0
EDOSIGUIENTE=   1
ACCION =        2
NUMEROITEMS =   3

#-------------------------------------------------------------
#   Clase Máquina de Estado Finita (MEF) 
#-------------------------------------------------------------

class MEF:

    #--------------------------------------------------------
    #   Constructor
    # 	Crea e inicia una tabla de estados (Modo compacto)
    
    def __init__(self, identificacion,Numero_estados, Numero_eventos, acciones, Sw= True):

        if Sw:
            self.tablaEstados = [0]*Numero_estados                                 # Crea lista de ceros
            for estado in range(Numero_estados):
                self.tablaEstados[estado]= [0]*Numero_eventos                      # Crea lista de ceros dentro de la lista
                for condicion in range(Numero_eventos):
                    self.tablaEstados[estado][condicion]= [0]*NUMEROITEMS  		# Crea lista de ceros dentro de la lista
                    self.tablaEstados[estado][condicion][0]="#"             # Acttualiza solo el primer item de la nueva lista
                    self.creado = True
        else:
            self.tablaEstados = []
            self.creado = False

        self.Nestados = Numero_estados
        self.Neventos = Numero_eventos
        self.ListaAcciones = acciones                                   # Lista de funciones de acción del problema
        self.estadoActual= 0                                            # Estado en un paso de ejecución
        self.cuenta = 0                                                 # Contador de pasos de ejecución
        self.ID = identificacion                                        # Identificador de esta máquin

    #-------------------------------------------------------------
    #   Se ejecuta la rutina de acción indicada por
    #   el <indice> obtenida de la librería

    def ejecuta(self,indice):
        func= self.ListaAcciones.get(indice)    # Se obtiene una función de la librerìa
        #print("paso",end="")
        return func()                           # y se ejecuta

    #-------------------------------------------------------------
    # Retorna el ñindice en la lista de eventos de un estado
    # de la siguente condicion libre (marcada por '#')

    def indice(self, estado):
        eventos = self.tablaEstados[estado]
        ind=0
        for cond in eventos:
            if cond[CONDICION] == "#":
                 break 
            ind += 1
        return ind
    
    #--------------------------------------------------------
    #   incluye 
    # 	Se añade la definición del <evento> de un <estado>
    # 	definido en la tripleta 
    #	<condicion>, <siguiente> y <accion>

    def incluye(self,estado,condicion,siguiente,accion):
        if self.creado:
            if estado < self.Nestados and siguiente < self.Nestados:
                evento = self.indice(estado)
                if evento < self.Neventos:
                    self.tablaEstados[estado][evento][CONDICION]= condicion
                    self.tablaEstados[estado][evento][EDOSIGUIENTE]= siguiente
                    self.tablaEstados[estado][evento][ACCION]= accion
                else:
                    print("** ERROR: Parámetro evento excede el límite ***")
            else:
                print("** ERROR: Parámetro estado muy alto ***")
        else:
            print("Tabla no ha sido creada")
            
    #-------------------------------------------------------------
    # Imprime el contenido de la table de estados

    def imprime_tabla(self):
        if self.creado:
            print()
            print('------------------- Tabla {0:2d} de estados------------------- '.format(self.ID))
            for estado in range(self.Nestados):
                print("estado ", estado, end= '  ')
                print(self.tablaEstados[estado])
            print("----------------------------------------------------------")
            print()
        else:
            print("Tabla no ha sido creada")
     
    #-------------------------------------------------------------
    # Procesa un paso de la máquina de estados

    def procesa(self, entrada):
        if self.creado:
            estado = self.tablaEstados[self.estadoActual]       #   Lee registro de estado
            for evento in estado:                               #   Evalua todos los eventos en el registro
                if entrada == evento[CONDICION]:                #   La entrada es un evento registrado?
                    self.ejecuta(evento[ACCION])                #   Se ejecuta la accion para ese evento
                    self.estadoActual = evento[EDOSIGUIENTE]    #   Actualiza el estado actual               	
                    #print(" ",end='')
        else:
            print("Tabla de máqina {} no ha sido creada".format(self.ID))

            #print(" Entrada= ", evento[CONDICION]," Estado Siguiente= ", evento[EDOSIGUIENTE]," Accion= ", evento[ACCION])

    #-------------------------------------------------------------
    # Retorna tabla se transiciones de estado
    
    def	lee_tabla(self):
        if self.creado:
            return self.tablaEstados
        else:
            print("Tabla no ha sido creada")
            return []

    #-------------------------------------------------------------
    # Retorna tabla se transiciones de estado
    
    def	copia_tabla(self,tabla):
        self.tablaEstados = tabla
        self.creado = True

    #-------------------------------------------------------------
    # Lee el identificador único del objeto
    
    def	lee_ID(self):
        clave = self.ID 
        return clave

    #-------------------------------------------------------------
    # Escribe externamente el identificador del objeto
    
    def Escribe_ID(self, clave):
        self.ID = clave

    #-------------------------------------------------------------
    # rstablece la cadencia de simulación para esta máqiona
    
    def Inicia_cadencia(self, tiempo):
        pygame.time.set_timer(USEREVENT + self.ID, tiempo)     # Establece cadencia de simulación en 1 segundo
        #print("MAQ " + str(self.ID))
    #-------------------------------------------------------------
    # rstablece la cadencia de simulación para esta máqiona
    
    def Inicia_Timer(self, tiempo, evento):
        timer = Timer(tiempo, evento)
        timer.start()
        #print("MAQ " + str(self.ID))

