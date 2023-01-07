#-------------------------------------------------------------
#   Máquina de Estado Finita
#	Version 1
#	-	Se crea la funcion <inicia_tabla>. La tabla de estados no se crea directamente, ni
#		en forma clásica. Se usa el modo compacto para
#		crear la matriz - que es menos obvia -
#	-	Se crea la funcion <incluir>
#	-	se crea la funcion <imprime_tabla>
#	-	se crea la funcion <Maquina>
#	-	Se crea una librería de funciones y la funcion
#		<Ejecuta> para escoger la función a partir de un índice
#-------------------------------------------------------------
#	NOTA: 
#		Hay conflictos con la variable <tablaEstados> porque deja
#	de ser global al ser creada en una subrutina. Pyhton no maneja bien
#       el ámbito de las variables, y loa parámetros por referencias a un función

#   Cada estado contiene una lista de eventos.
#   Cada evento tiene información de:
#   <código del evento>     o condición a evaluar,
#   <estado siguiente>      si se cumple el evento
#   <acción a realizar>     o indice a la acción para ese evento de la librería de acciones 
#                           a realizar

NUMERO_ESTADOS =3       #	Número de estados que requiere el problema
NUMERO_EVENTOS =3       #	Número de eventos que evalúa el estado
NUMERO_ITEMS =  3       #	Tripleta de atributos: código de evento o condición, 
                #	estado siguiente e índice de acción que tiene cada evento

ESTADO_0 =      0
ESTADO_1 =      1
ESTADO_2 =      2

EVENTO_0 =      0
EVENTO_1 =      1
EVENTO_2 =      2

CONDICION =     0
EDOSIGUIENTE=   1
ACCION =        2


#----------------------------------------------------
# crea una tabla de estados (Modo compacto)

def inicia_tabla(estados,eventos):
    
    if estados < NUMERO_ESTADOS and eventos < NUMERO_EVENTOS:	    # Si los vlores estan dentro de los rangos
        tablaEstados = [0]*NUMERO_ESTADOS                           # Crea lista de ceros
        for estado in range(NUMERO_ESTADOS):
            tablaEstados[estado]= [0]*NUMERO_EVENTOS                # Crea lista de ceros dentro de la lista
            for condicion in range(NUMERO_EVENTOS):
                tablaEstados[estado][condicion]= [0]*NUMERO_ITEMS   # Crea lista de ceros dentro de la lista
                tablaEstados[estado][condicion][0]="NO"             # Acttualiza solo el primer item de la nueva lista
"""
tablaEstados = [0]*NUMERO_ESTADOS                           # Crea lista de ceros
for estado in range(NUMERO_ESTADOS):
    tablaEstados[estado]= [0]*NUMERO_EVENTOS                # Crea lista de ceros dentro de la lista
    for condicion in range(NUMERO_EVENTOS):
        tablaEstados[estado][condicion]= [0]*NUMERO_ITEMS   # Crea lista de ceros dentro de la lista
        tablaEstados[estado][condicion][0]="NO"             # Acttualiza solo el primer item de la nueva lista
"""
#----------------------------------------------------
# Se añade la definición del <evento> de un <estado>
# definido en la tripleta 
#	<condicion>, <siguiente> y <accion>

def incluye(estado,evento,condicion,siguiente,accion):
    if estado < NUMERO_ESTADOS and evento  < NUMERO_EVENTOS:
        tablaEstados[estado][evento][CONDICION]= condicion
        tablaEstados[estado][evento][EDOSIGUIENTE]= siguiente
        tablaEstados[estado][evento][ACCION]= accion
 
#-------------------------------------------------------------
# Imprime el contenido de la table de estados

def imprime_tabla():
    print()
    print("------------------- Tabla de estados --------------------- ")
    for estado in range(NUMERO_ESTADOS):
        print("estado ",estado,end= '  ')
        print(tablaEstados[estado])
    print("----------------------------------------------------------")
    print()

#-------------------------------------------------------------
#   Lista de funciones a través de una librería

def Accion1():
    print("Evento 1",end='->')

def Accion2():
    print("Evento 2",end='->')

def Accion3():
    print("Evento 3",end='->')

    
ListaAcciones ={                            #   Se crea la librería
    0: Accion1,
    1: Accion2,
    2: Accion3
    }

#-------------------------------------------------------------
#   Se ejecuta la rutina de acción indicada por
#	el <indice> obtenida de la librería

def Ejecuta(indice):
        func= ListaAcciones.get(indice)     # Se obtiene una función de la librerìa
        return func()                              # y se ejecuta
   
#-------------------------------------------------------------
#   Máquina de estados

def Maquina(entrada, estadoActual):
    estado = tablaEstados[estadoActual]     #   Lee registro de estado
    for evento in estado:                   #   Evalua todos los eventos en el registro
        if entrada == evento[0]:            #   La entrada es un evento registrado?
            Ejecuta(evento[2])              #   Se ejecuta la accion para ese evento
            print(" Entrada= ",evento[0]," Estado Siguiente= ",evento[1]," Accion= ",evento[2])
            return evento[1]                #   retorna le estado siguiente
            
#-------------------------------------------------------------
#   Principal
#-------------------------------------------------------------
#   Lista de Entradas a evaluar

entrada= "0102221110110111110"
print()
print("entrada =",entrada)

#-------------------------------------------------------------
#   Se crea una tabla de estados según el problema

#inicia_tabla(NUMERO_ESTADOS,NUMERO_EVENTOS)
#imprime_tabla()

#-------------------------------------------------------------
#   Se definen los eventos de la máguina de estados

incluye(ESTADO_0,EVENTO_0,'0',0,0)
incluye(ESTADO_0,EVENTO_1,'1',1,0)
incluye(ESTADO_0,EVENTO_2,'2',2,0)

incluye(ESTADO_1,EVENTO_0,'0',0,0)
incluye(ESTADO_1,EVENTO_1,'1',1,1)
incluye(ESTADO_1,EVENTO_2,'2',1,0)

incluye(ESTADO_2,EVENTO_0,'0',2,1)
incluye(ESTADO_2,EVENTO_1,'1',0,0)
incluye(ESTADO_2,EVENTO_2,'2',1,0)

imprime_tabla()

#-------------------------------------------------------------
#   Se evalúa con la máquina la lista o secuencia de entradas

i=1
estadoActual = 0
for char in entrada:
    estadoActual= Maquina(char,estadoActual)
    i+=1

