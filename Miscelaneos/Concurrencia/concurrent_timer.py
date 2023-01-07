from threading import Timer
import time

class Temporizador(Timer):
    """
    Implementación propia de timer para hacerlo concurrente
 
    Timer (basado en threading._Timer)
    que invoca un método a un determinado intervalo en segundos

    """

    # --------------------------------------------------------------------

    def __init__ (self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """

        Timer.__init__ (self, *args, **kwargs)
        self.setDaemon (True)
        self._running = 0
        self._destroy = 0
        self.start()

    # --------------------------------------------------------------------

    def run (self):
        """

        :return:
        """
        while True:
            self.finished.wait(self.interval)
            if self._destroy:
                return
            if self._running:
                self.function (*self.args, **self.kwargs)

    # --------------------------------------------------------------------

    def start_timer (self):
        """

        :return:
        """
        self._running = 1

    # --------------------------------------------------------------------

    def stop_timer (self):
        """

        :return:
        """
        self._running = 0

    # --------------------------------------------------------------------

    def is_running (self):
        """

        :return:
        """
        return self._running
 
    # --------------------------------------------------------------------

    def destroy_timer (self):
        """

        :return:
        """
        self._destroy = 1

#------------------------------------------------------------
#       M A I N
#------------------------------------------------------------

if __name__ == "__main__":

    #----------------------------------------------------
    #   Función a ejecutar concurrentemente al que se le
    #   pasa un parámetro

    def Funcion_Prueba (name):
        print ('tiempo  %s' % name)
 
    #----------------------------------------------------
    #   prueba

    tiempo = Temporizador(1.0, Funcion_Prueba, ['1 seg'])
    tiempo.start_timer()

    while 1:
        time.sleep(10)       #  Se libera el procesdador un tiempo
        print("-> 10 seg")
        #tiempo.stop_timer()  #  Al termiaar el tiempo se para  eo ciclo de recurrencia

