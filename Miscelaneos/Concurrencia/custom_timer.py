from threading import Thread
from time import sleep
 
TIMER_ON_TIME = 1
 

""" 
    --------------------------------------------------------------------------
        
    La clase <ResettableTimer> es un temporizador cuyo bucle de conteo puede ser
    reiniciado arbitrariamente. Su duración es configurable. Se pueden especificar
    comandos tanto para la expiración como para la actualización.
    Su resolución de actualización también se puede especificarse. El temporizador
    reiniciable sigue contando hasta que el método <run> es explícitamente parado
    con el método <kill>.
    
    --------------------------------------------------------------------------
"""

class ResettableTimer(Thread):

    def __init__(self, maxtime, FunExpire, inc=None, FunUpdate=None):
        """

        :param maxtime:     time in seconds before expiration after resetting
                            in seconds
        :param FunExpire:   function called when timer expires
        :param inc:         amount by which timer increments before
                            updating in seconds, default is maxtime/2
        :param FunUpdate:   function called when timer updates
        """
        
        self.maxtime =  maxtime
        self.expire =   FunExpire

        if inc:
            self.inc =    inc
        else:
            self.inc =    maxtime/2

        if FunUpdate:
            self.update = FunUpdate
        else:
            self.update = lambda c : None

        self.counter =  0
        self.active =   True
        self.stop =     False

        Thread.__init__(self)
        self.setDaemon(True)

    #--------------------------------------------------------------------------

    def set_counter(self, t):
        """
        Set self.counter to t.

        :param t:   new counter value
        :return:    None
        """
        self.counter = t

    #--------------------------------------------------------------------------

    def deactivate(self):
        """
        Set self.active to False.

        :return:    None
        """
        self.active = False

    #--------------------------------------------------------------------------

    def kill(self):
        """
        Will stop the counting loop before next update.

        :return:    Noone
        """
        self.stop = True

    #--------------------------------------------------------------------------

    def reset(self):
        """
        Fully rewinds the timer and makes the timer active, such that
        the expire and update commands will be called when appropriate.

        :return: NOne
        """
        self.counter = 0
        self.active = True
     
    #--------------------------------------------------------------------------

    def run(self):
        """
        Run the timer loop.

        :return:
        """

        #print("activo")
        while True:
            self.counter = 0
            while self.counter < self.maxtime:
                self.counter += self.inc

                sleep(self.inc)

                if self.stop:
                    return

                if self.active:
                    self.update(self.counter)

            if self.active:
                self.active = False
                self.expire()
 
#--------------------------------------------------------------------------

class Relay:

    #--------------------------------------------------------------------------

    def __init__(self, id):
        """
        Constructor
        :param id:
        """
        self.id = id
     
        #print ("** Starting " + str(id) + " ON for " + str(TIMER_ON_TIME) + " seconds")
     
        self.timer = ResettableTimer(TIMER_ON_TIME, self.process_event)
        self.timer.start()
 
    #--------------------------------------------------------------------------

    def process_event(self):
        """
        handle the relay switching on timer event
        :return:
        """
 
        # execute some logic
        # ...
        # ...
     
        print('Evento para Relay: ',  str(self.id))
        self.timer.maxtime = TIMER_ON_TIME              # resetea el timer

        print ('Reiniciando timer: ', str(self.id))
        self.timer.reset()                              # restart el timer

#------------------------------------------------------------------------ 
#    M A I N
#------------------------------------------------------------------------ 

if __name__ == "__main__":

    # Crea lista de temporizadores

    relays = []
    for i in range(10):
        relays.append(Relay(i))     #  Añade temprizador a la lista

    #------------------------------------------------------------------------
    # Main loop

    while True:
      sleep(10)           # sleep until it's time to do something in this loop
      print("-> 10 seg")
      #print(">> active threads: ", activeCount(), "\n")  # this might need to be active_count()
         