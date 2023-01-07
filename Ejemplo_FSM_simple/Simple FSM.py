#-------------------------------------------------------------
#   Máquina de Estado Finita
#-------------------------------------------------------------

#   Cada estado contiene una lista de eventos.
#   Cada evento tiene información de:
#   <código del evento>     o condición a evaluar,
#   <estado siguiente>      si se cumple el evento
#   <acción a realizar>     o indice a la acción para ese evento de la librería de acciones 
#                           a realizar

tablaEstados= (
    (("0", 0, 0),("1", 1, 0),("2", 2, 0)), # estado 0
    (("0", 0, 0),("1", 1, 1),("2", 1, 0)), # estado 1
    (("0", 2, 1),("1", 0, 0),("2", 1, 0)), # estado 2
    )

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
#   Lista de Entradas a evaluar

entrada= "0102221110110111110"
print()
print("entrada =",entrada)
print()

#-------------------------------------------------------------
#   Se evalúa con la máquina la lista o secuencia de entradas

i=1
estadoActual = 0
for char in entrada:
    estadoActual= Maquina(char,estadoActual)
    i+=1

