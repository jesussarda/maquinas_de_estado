from libs.utils.class_utilities import TimeEvent
from  time import time

# ----------------------------------------------------
#   Función a ejecutar recurrentemente al que se pasa un parámetro

def funcion_evento(name):
    print(f'Comando {name}')


# ------------------------------------------------------------
#   M A I N
# ------------------------------------------------------------

intervalo =     1
cant_ciclos =   5

if __name__ == "__main__":

    evento = TimeEvent(intervalo, funcion_evento)
    evento.start_timer()
    evento.update_data('tiempo')
    evento.run()    # lazo del temporizador
