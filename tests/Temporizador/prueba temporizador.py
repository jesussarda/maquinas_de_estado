from temporizador import *
import time
from random import randint


#----------------------------------------------------
#   Función a ejecutar recurentemente al que se pasa un parámetro

def FuncionPrueba (name):
    print ('tiempo  %s' % name)

#----------------------------------------------------
#   Clase 

class Item():
    """
    """
    def __init__ (self, id, interv, funcion):
        """
        """
         
        self.ID = id
        self.FuncionPrueba = funcion
        self.entrada = ""
        self.intervalo = interv

    def inicia(self):
        """
           prueba
        """
 
        #----------------------------------------------------
 
        self.tiempo = Temporizador(self.intervalo, self.FuncionPrueba, [self.entrada])    #   Crea una instancia del temporizador
        self.tiempo.start_timer()                                    #   Inica ciclo

    def Procesa(self, dato):
        """
        """
        self.tiempo.update_data(dato)
        #print( self.entrada)


#------------------------------------------------------------
#   MAIN
#------------------------------------------------------------


def main():

    comando= ["PAR","PAB","MAD","MAT",]

    #----------------------------------------------------
    #   Crea temporizador

    item = Item(0, 1, FuncionPrueba)        # ID = 0, tiempo = 1 seg
    item.inicia()                           # Inicia temporizacio

    i= 0
    while 1:
        dato = randint(0,len(comando)-1)    # Genera un dato aleatorio, para simular un dato cambiante
        dato = comando[dato]
        print(" -> 10 seg", end= " ")
        print("{:2d} llega comando {}".format(i, dato))
        item.Procesa(dato)                  #Camia dato de la función

        time.sleep(10)                      # Se libera el procesdador dirante un  tiempo
        #tiempo.stop_timer()                # Al termiaar el tiempo se para  eo ciclo de recurrencia
        i += 1


#------------------------------------------------------------
#   EJECUTA MAIN
#------------------------------------------------------------
if __name__ == "__main__":
    
    main()
