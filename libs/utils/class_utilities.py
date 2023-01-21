import threading
import time

# ===============================================================================================
#      Counter
# ===============================================================================================

class Counter():

    # --------------------------------------------------------------

    def __init__(self, id_name,  callback= None):
        """
            Crea un evento de conteo. El identificador del evento es <id_name>. una cuenta se
            realiza invocando el método <step> y se puede monitorear el estado con el método
            <has_ended>. El diccionario para esa instancia se obtiene con <get_count_event_dict>.

        :param id:
        :param callback:
        """

        self.id_name = id_name
        self._function = callback

    # --------------------------------------------------------------

    def set_counter(self, count_limit= 1, up= True):
        """
            Inicia las condiciones de operación del contador
        :param count_limit: Número de pasos de conteo
        :param up:          Sentido del conteo True: creciente, False decreciente
        :return:
        """

        if count_limit <= 0:
            count_limit = 1
            print(f'Limite no puede ser menor a uno')

        self._limit = count_limit - 1

        if up:
            self._count = 0
        else:
            self._count = count_limit - 1
        self._stop = False
        self._up = up

    # --------------------------------------------------------------

    def reset(self):
        """
            Reinicia condiciones de operación del contador
        :return:
        """
        if self._up:
            self._count = 0
        else:
            self._count = self._limit-1
        self._stop= False

    # --------------------------------------------------------------

    def step(self, *args, **kwargs):
        """
            Un paso de conteo (creciente o decreciente). Si llega al limite
            se ejecuta la función de callback (si la hay)
        :param args:    Argumentos para la función callback (opcional)
        :param kwargs:
        :return:    Resultado de la funcion (opcional)
        """
        info= None

        if self._stop:
            self._stop = False

        # ---------------------------------------------------
        #  incremental

        if self._up:
            if self._count >= self._limit:
                if self._function:
                    info = self._function(*args, **kwargs)
                self._stop= True
                self._count = 0
            else:
                self._count += 1

        # ---------------------------------------------------
        #  decremental

        else:
            if self._count <= 0:
                if self._function:
                    info = self._function(*args, **kwargs)
                self._stop= True
                self._count = self._limit
            else:
                self._count -= 1

        return info

    # --------------------------------------------------------------

    def has_ended(self):
        """
            Se verifica si el conteo ha finalizado, en cualquiera
            de los sentidos

        :return:
        """
        return self._stop

    # --------------------------------------------------------------

    def get_count(self):
        """

        :return:
        """
        return self._count

    # --------------------------------------------------------------

    def get_count_event_dict(self):
        """
            Obtiene el estado de la instancia en el formato de
            un diccionario.

        :return:    Diccionario con el id de la instancia y el estado
                    de finalización del conteo
        """
        return {self.id_name: self.stop}


# ===============================================================================================
#       EbdMsg
# ===============================================================================================


class EndMsg():

    # -------------------------------------------------------------------------------------------

    def __init__(self):
        """
            presenta un mensaje con el origen del error y termina la ejecución.
        """
        msg = 'None'

    # -------------------------------------------------------------------------------------------

    def put_msg(self, msg):
        """
            Presenta en terminal un mensaje.

        :param msg:
        :return:
        """
        print(f'\n\t{msg}.')

    # -------------------------------------------------------------------------------------------

    def put_error_msg(self, method_name, msg, end = True):
        """
            Presenta en terminal un mensaje, con el nombre de de el método o función donde se
            origino el error, y termina la ejecución del script.

        :param method_name:     Nombre del método o función que genera el error
        :param msg:             Mensaje anttes de terminar.
        :return:
        """

        print(f'\n\tERROR: <{method_name}> {msg}.')
        if end:
            exit()


# ===============================================================================================
#       TimeEvent
# ===============================================================================================

class TimeEvent(threading.Timer):
    """

        implementación de evento timer concurrente
    """

    def __init__(self,interval, callback, *args, **kwargs):
        """

            Timer (basado en threading._Timer)
            que invoca un método a un determinado intervalo en segundos
        :param interval:
        :param callback:
        :param args:
        :param kwargs:
        """

        threading.Timer.__init__(self,interval, callback, *args, **kwargs)
        self.setDaemon(True)
        self._running = 0
        self._destroy = 0
        self.start()

        self.dato = "0"

    # -------------------------------------

    def run(self):
        """
            Ejecuta el temporizador recursivamente
        :return:
        """

        while True:
            self.finished.wait(self.interval)
            if self._destroy:
                return
            if self._running:
                self.args = (self.dato,)  # parámetro debe estar en una lista o tupla
                self.function(*self.args, **self.kwargs)

    # -------------------------------------

    def start_timer(self):
        """
            Inicia la temporización
        :return:
        """
        self._running = True

    # -------------------------------------

    def stop_timer(self):
        """
            Para el temporizador
        :return:
        """
        self._running = False

    # -------------------------------------

    def is_running(self):
        """
            Verifica si el proceso está corriendo
        :return:    estdo de
        """
        return self._running

    # -------------------------------------

    def destroy_timer(self):
        """
            Elimina timer

        :return:
        """
        self._destroy = True

    # -------------------------------------

    def update_data(self, dato):
        """
            Actualiza parámetro de la función
                *** Añadido ***

        :param dato:
        :return:
        """
        self.dato = dato
