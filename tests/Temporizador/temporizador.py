import threading

class Temporizador(threading.Timer):
    """ implemntacion propia de timer para hacerlo recurrente
 
        Timer (basado en threading._Timer)
        que invoca un método a un determinado intervalo en segundos
 
    """
     
    def __init__ (self, *args, **kwargs):
        threading.Timer.__init__ (self, *args, **kwargs) 
        self.setDaemon (True)
        self._running = 0
        self._destroy = 0
        self.start()
        self.dato = "0"

    #-------------------------------------
    #    Ejecuta el temporizador recursivamente

    def run (self):

        while True:
            self.finished.wait (self.interval)
            if self._destroy:
                return;
            if self._running:
                self.args = [self.dato]         # parámetro debe estar en una lista
                self.function(*self.args, **self.kwargs)
                #print(self.args)
 
    #-------------------------------------
    #    Inicia la temporizción

    def start_timer (self):
        self._running = 1
 
    #-------------------------------------
    #    Para el temporizador

    def stop_timer (self):
        self._running = 0
 
    #-------------------------------------
    #    Verifica si el proceso está corriendo

    def is_running (self):
        return self._running
 
    #-------------------------------------
    #    Elimina timer

    def destroy_timer (self):
        self._destroy = 1;

    #-------------------------------------
    #    Actualiza parámetro de la función
    #   *** Añadido ***

    def update_data(self,dato):
        self.dato = dato

