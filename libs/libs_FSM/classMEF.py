""" -------------------------------------------------------------
    clase Máquina de Estado Finita

    Version 4 (20-may-2018)

    -   Se crea la clase MEF que resuelve los problemas de la version V1
        con los atributos

        <tablaEstados>
            que es la tabla de estados. La tabla de estados no
            se crea directamente, ni en forma clásica. Se usa el modo compacto para
                crear la matriz - que es menos obvia -
                <ListaAcciones>
                una lista que contiene todas las funciones definidas externamente para
                el problema, usadas en la tabla de estado a través de un indice
                o código único.
                <estadoActual>
                el estado de la transición actual
                <cuenta>
            que  cuenta le número de pasos

        y los métodos

                <ejecuta>
                    que obtiene la función de acción definida por un <indice>
                    de una lista.
                <incluye>
                    para añadir eventos a la tabla
                <imprime_tabla>
                    para imprimir oa tabla de estados
                <procesa>
                    que procesa un paso o cambio de estado de la máquina

    -------------------------------------------------------------
    NOTA:
        Cada estado contiene una lista de eventos.
        Cada evento tiene información de:
        <código del evento>     o condición a evaluar,
        <estado siguiente>      transición si se cumple el evento
        <acción a realizar>     o indice a la acción para ese evento de la librería de acciones
                                a realizar
"""

#-------------------------------------------------------------
#   Constantes

CONDICION =     0
EDOSIGUIENTE=   1
ACCION =        2
NUMEROITEMS =   3

#-------------------------------------------------------------

class MEF:
    """
        Clase Máquina de Estado Finita (MEF)
    """

    #--------------------------------------------------------

    def __init__(self, Numero_estados, Numero_eventos,acciones):
        """
            Crea e inicia una tabla de estados (Modo compacto)

        :param Numero_estados:
        :param Numero_eventos:
        :param acciones:
        """
        self.tablaEstados = [0]*Numero_estados                                 # Crea lista de ceros
        for estado in range(Numero_estados):
            self.tablaEstados[estado]= [0]*Numero_eventos                      # Crea lista de ceros dentro de la lista
            for condicion in range(Numero_eventos):
                self.tablaEstados[estado][condicion]= [0]*NUMEROITEMS  		# Crea lista de ceros dentro de la lista
                self.tablaEstados[estado][condicion][0]="#"             # Acttualiza solo el primer item de la nueva lista

        self.Nestados = Numero_estados
        self.Neventos = Numero_eventos
        self.ListaAcciones = acciones                                   # Lista de funciones de acción del problema
        self.estadoActual= 0                                            # Estado en un paso de ejecución
        self.cuenta = 0                                                 # Contador de pasos de ejecución

    #-------------------------------------------------------------

    def ejecuta(self,indice):
        """
            Se ejecuta la rutina de acción indicada por
            el <indice> obtenida de la librería

        :param indice:
        :return:
        """
        func= self.ListaAcciones.get(indice)    # Se obtiene una función de la librerìa
        return func()                           # y se ejecuta

    #--------------------------------------------------------

    def incluye(self,estado,evento,condicion,siguiente,accion):
        """
         	Se añade la definición del <evento> de un <estado>
         	definido en la tripleta
        	<condicion>, <siguiente> y <accion>

        :param self:
        :param estado:
        :param evento:
        :param condicion:
        :param siguiente:
        :param accion:
        :return:
        """
        if estado < self.Nestados and evento  < self.Neventos and siguiente < self.Nestados:
            self.tablaEstados[estado][evento][CONDICION]= condicion
            self.tablaEstados[estado][evento][EDOSIGUIENTE]= siguiente
            self.tablaEstados[estado][evento][ACCION]= accion
        else:
            print("** ERROR: Parámetro estado o evento muy alto ***")
            
    #-------------------------------------------------------------

    def imprime_tabla(self):
        """
            Imprime el contenido de la table de estados.

        :param self:
        :return:    None
        """

        print()
        print("------------------- Tabla de estados --------------------- ")
        for estado in range(self.Nestados):
            print("estado ", estado, end= '  ')
            print(self.tablaEstados[estado])
        print("----------------------------------------------------------")
        print()
     
    #-------------------------------------------------------------

    def procesa(self, entrada):
        """
            Procesa un paso de la máquina de estados

        :param self:
        :param entrada:
        :return:
        """

        estado = self.tablaEstados[self.estadoActual]       #   Lee registro de estado
        for evento in estado:                               #   Evalua todos los eventos en el registro
            if entrada == evento[CONDICION]:                #   La entrada es un evento registrado?
                self.ejecuta(evento[ACCION])                     #   Se ejecuta la accion para ese evento
                self.estadoActual = evento[EDOSIGUIENTE]    #   Actualiza el estado actual


