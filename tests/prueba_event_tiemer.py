from libs.utils.class_utilities import TimeEvent
import time
from random import randint


# ----------------------------------------------------
#   Función a ejecutar recurrentemente al que se pasa un parámetro

def FuncionPrueba(name):
    print(f'Comando {name}')


# =======================================================
#       C L A S E
# =======================================================

class TimeEventSchduller():
    """

    """

    def __init__(self, id, interval, function):
        """

        :param id:
        :param intervalo:
        :param funcion:
        """

        self.id = id
        self.function = function
        self.input = ""
        self.interval = interval


    def init(self):
        """

        :return:
        """

        self.tiempo = TimeEvent(self.interval, self.function, (self.input,))  # Crea una instancia del temporizador
        self.tiempo.start_timer()  # Inicia ciclo


    def run(self, dato):
        """

        :param dato:
        :return:
        """
        self.tiempo.update_data(dato)


# ------------------------------------------------------------
#   M A I N
# ------------------------------------------------------------

intervalo= 1
periodo =       10
cant_ciclos =   5

if __name__ == "__main__":

    comando = ["PAR", "PAB", "MAD", "MAT", ]

    # ----------------------------------------------------
    #   Crea temporizador

    item = TimeEventSchduller(0, 1, FuncionPrueba)   # ID = 0, tiempo = 1 seg
    item.init()                               # Inicia temporización

    i = 0
    ciclo = True
    while ciclo:

        idx = randint(0, len(comando) - 1)  # Genera un indice aleatorio, para simular un comando cambiante
        dato = comando[idx]
        print(f" -> Periodo {i:2d}, {periodo} seg. Llega comando {dato}")
        item.run(dato)                  # Cambia dato de la función

        time.sleep(periodo)                 # Se libera el procesador durante un  tiempo
        # tiempo.stop_timer()               # Al terminar el tiempo se para lo ciclo de recurrencia
        if i < cant_ciclos:
            i += 1
        else:
            ciclo= False

