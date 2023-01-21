from libs.utils.class_utilities import CountEvent, TimeEvent
from time import time, sleep, ctime, thread_time_ns


# ------------------------------------------------------------

def event_ended(data):

    print(f'\tEvent {data} ended: {ctime(time())}')

# ------------------------------------------------------------

def scheduler(counters_lst):

    print(f'Base time: {ctime(time())}')

    for counter in counters_lst:
        name = counter.id_name
        counter.step(name)

# =======================================================
#       C L A S E
# =======================================================

class TimeEventSchduller():

    # ---------------------------------------------------

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

    # ---------------------------------------------------

    def init(self):
        """

        :return:
        """

        self.tiempo = TimeEvent(self.interval, self.function, (self.input,))  # Crea una instancia del temporizador
        self.tiempo.start_timer()  # Inicia ciclo

    # ---------------------------------------------------

    def run(self, dato):
        """

        :param dato:
        :return:
        """
        self.tiempo.update_data(dato)


# ------------------------------------------------------------
#   M A I N
# ------------------------------------------------------------

interval =      1       # Base de teiempo de 1 seg.
num_counters =   5       # cantidad de contadores
conts_list = [5,10,15,20,25]

if __name__ == "__main__":

    # crea lista de contadores

    counters = []
    for i in range(num_counters):
        counter = CountEvent(f'T{i}',event_ended)
        counter.set_counter(conts_list[i], up= False)
        counters.append(counter)

    # Inicia programador de eventos temporales

    scheduler = TimeEventSchduller('TES', 1, scheduler)
    scheduler.init()

    while 1:
        scheduler.run(counters)
        sleep(5)

