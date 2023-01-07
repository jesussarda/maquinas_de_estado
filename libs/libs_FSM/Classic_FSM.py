
"""
    MÁQUINA DE ESTADO FINITO (Finite State Machine).
    
    Implementación de símil electrónico basada en una tabla o lista de estados y condiciones similar a como se crea
    en una memoria ROM en el diseño de circuitos secuenciales. El algoritmo es menos eficiente en tiempo de 
    proesamiento pero mas intuitivo de crear y  diseñar para el usuario. La transición de estados se genera en forma
    natural a partir del diagrama de estados. Para ello se ha  creado un método <add_state> para transferir el diseño
    del diagrama al diseño del algiritmo, estado a estado, con sus condiciones o eventos, y sus transiciones y acciones
    dependiendo de si se cumple  la condición.
    

    Sigue las ruta de cambios de estado definida en un diccionario con la secuencia clave-valor:
    <Id_estado>: <Lista Condiciones>. Donde:

        'Id_estado' (clave):            Es una etiqueta que identifica al estado creado o por crear.
                                        El valor para esta clave es siempre una lista, de condiciones.

    Cada estado del diccionario está caracterizado por una lista de diccionarios de pares clave-valor
    con todas las condiciones posibles para ese estado. Cada item está declarado así.

        'key' (Condición):              Es un código de identificación que define la condición para
                                        que haya un cambio de estado.

        'next_st' (Estado Siguiente):   Es un identificador del estado de cambio si se cumple la condición.
                                        Generalmente lo crea una función que evalúa cualquier
                                        evento a monitorizar: estado de switches, eventos del sistema operativo,
                                        concurrencias temporales, etc. como retorno.

        'action'(Acción):               Es una función en donde se ejecuta la acción a realizar si se
                                        cumple la condición. Pueden ser nuevos eventos a evaluar.

    NOta:
        El diccionario es case insensitive para las  etiquetas
        Todas la etiquetas deben estar en letra minúscula. Si alguna etiqueta contiene mayusculas se convierte
        internamente a minúsculas.

==================================================================================================================

    Ejemplo:
                                                              s
        Para Los estados definidos con los identificadores 'inicio', 'edo_1', 'fin'
                                                                      }
        dic_Estados = { 'inicio': [

                                {'key':     '0102',
                                 'next_st': 'edo_1',
                                 'action':  <func accion1>},

                                {'key': '0111',
                                 'next_st': 'inicio',
                                 'action': <func accion2>}
                          ],
                        'edo_1': [

                                {'key': '0102',
                                 'next_st': 'fin',
                                 'action': <func accion1>}
                          ],
                        'fin': [

                                {'key': '103',
                                 'next_st': 'inicio',
                                 'action': <func accion3>}
                          ]
                    }

    NOTA:
        En  teoría no hay límite en la cantidad de estados o cantidad de condiciones (eventos) por estado. El limite
        lo establece los recursos.
"""


# -------------------------------------------------------------------------------------------

class FSM():

    name ='Finite State Machine'
                                                     
    # -------------------------------------------------------------------------------------------

    def __init__(self, Inicial_state, state_table = None, action_dict = None):
        """
           Establece las condiciones iniciales de la Máquina de Estado.

        :param Inicial_state:   Estado inicial para la secuencia de transiciones de estados.
        :param state_table:     Diccionario con la secuencia de transiciones de estados
        :param action_dict:     Diccionario con la colección de rutinas de acción que cumple un evento.
        """

        if state_table and action_dict:
            valid_state_dict = self.validate_table(state_table, action_dict)
            self.state_table = valid_state_dict # tabla de estados prediseñada validada
        else:
            self.state_table = {}               # tabla de estados vacía.
                                                # Se debe crear usando <add_state>

        self.inicial_state =    Inicial_state   # estado de comienzo
        self.actual_state =     Inicial_state   # estado actual (varía según la tabla de estados
        self.sw_stop =          False

    # -------------------------------------------------------------------------------------------

    def validate_table(self, state_table, action_dict):
        """
            Válida la consistencia de la estructura de la tabla de estados y convierte los identificadores
            de acción en la función o el método, que debe haber sido creado previamente.

        :param state_table:
        :return:    None Si hay inconsistencias, o, La tabla con el ajuste de las acciones
        """

        state_table = self.validate_consistency(state_table, action_dict)
        if state_table:
            for state in state_table.keys():
                event_list = state_table[state]
                if event_list:
                    for idx, event_dict in enumerate(event_list):
                        function = self.validate_event_dict(state, event_dict, action_dict)
                        if function:
                            state_table[state][idx]['action'] = function
                        else:
                            print(
                                f'\n\tERROR: <validate_table> No existe una función de acción válida para el evento <{event_dict["key"]}> del estado <{state}>')
                            exit()
                else:
                    print(f'\n\tERROR: <validate_table> El estado <{state}> no contiene condiciones o eventos')
                    exit()
        else:
            print(f'\n\tERROR: <validate_table> La tabla no ha sido creada')
            exit()

        return state_table

    # -------------------------------------------------------------------------------------------

    def validate_consistency(self,state_table, action_dict):
        """
            Valida que las etiquetas de estado sea la misma que en el estado siguiente, independientemente
            de el case.

        :param state_table:    Diccionario de estados.
        :return:               Diccionario de estados validado.
        """

        if state_table:                         # si no está vacio
            state_list = state_table.keys()
            action_list = action_dict.keys()
            for state in state_list:
                event_list = state_table[state]
                if event_list:
                    for idx, event_dict in enumerate(event_list):
                        if state.lower() == event_dict['next_st'].lower():
                            state_table[state][idx]['next_st'] = state
                        for action in action_list:
                            if event_dict['action'].lower() == action.lower():
                                state_table[state][idx]['action'] = action
                else:
                    print(f'\n\tERROR: <validate_consistency> El estado <{state}> no contiene condiciones o eventos')
                    exit()
        else:
            print(
                f'\n\tERROR: <validate_consistency> El diccionario de estados no existe')
            exit()

        return state_table

    # -------------------------------------------------------------------------------------------

    def validate_event_dict(self, state, event_dict, action_dict):
        """
            Valida estructura de u diccionario de evento <event_dict> de un estado <state> específico.

        :param state:       Id de estado ql que pertenec el evento.
        :param event_dict:  Diccionario de un evento del estado <state> a validar.
                            Claves: 'key', 'next_st' y 'action'
        :param action_dict: Diccionario con el grupo de funciones o métodos de acción para la
                            condición o evento, si se da la condición en <key>

        :return: action_method  Función correspondiente (ejecutable)

        """

        action_method = None
        if event_dict and action_dict:

            # -------------------------------------------------------------------------------------------------------
            # se validan las entradas:
            # El id de estado debe ser un un string. Otro tipo no es valido.

            if not isinstance(state, str):
                print(
                    f'\n\tERROR: El identificador de estado <{state}> debe ser alfanumérico.')
                exit()

            # El id de condición debe ser un un string. Otro tipo no es válido.

            if not isinstance(event_dict['key'], str):
                print(
                    f'\n\tERROR: El identificador en condición o evento <{event_dict["key"]}> del estado <{state}> debe ser alfanumérico.')
                exit()

            # El id de condición debe ser un un strsing. Otro tipo no es válido.

            if not isinstance(event_dict['next_st'], str):
                print(
                    f'\n\tERROR: El identificador de estado siguente <{event_dict["next_st"]}> para la condición <{event_dict["key"]}> del estado <{state}> debe ser alfanumérico.')
                exit()

            # El id de accion deb esr un string.

            if not isinstance(event_dict['action'], str):
                print(
                    f'\n\tERROR: El identificador de acción <{event_dict["action"]}> para la condición <{event_dict["key"]}> del estado <{state}> debe ser alfanumérico.')
                exit()
            else:
                action = event_dict["action"]
                if action in action_dict.keys():
                    action_method = action_dict[action]
                else:
                    print(
                        f'\n\tERROR: El método <{event_dict["action"]}> para la condición <{event_dict["key"]}> del estado <{state}> no ha sido creado.')
                    exit()
        else:
            print(
                f'\n\tERROR: <validate_event_dict> El diccionario de eventos y/o de acciones no existe.')
            exit()

        return action_method

    # -------------------------------------------------------------------------------------------

    def step(self, key):
        """
            Busca en el diccionario de estados la lista de eventos o condiciones a evaluar para
            el estado actual.
            Recorre la lista para encontrar el código del evento en <key>, si existe, se ejecuta
            la acción correspondiente y se cambia de estado

            NOTA:
                El código <key> generalmente se crea a partir de una función <get_coded_events>
                que evalúa el estado de dispositivos, códigos de eventos, etc. que cambian
                concurrentemente.

        :param  key:    Código de evento a evaluar.
        :return: None
        """

        # Verifica que el id de evento (key) existe en la lista de eventos del estado actual.
        # Si está y se cumple la condición, se cambia en estado actual por el estado indicado en
        # la condición y se ejecuta la acción asociada.

        if self.state_table:
            for self.event_key in self.state_table[self.actual_state]:
                if self.event_key['key'] == key:
                    if self.event_key['action'] != None:
                        self.event_key['action']()
                    self.actual_state = self.event_key['next_st']
        else:
            print(
                f'\n\tERROR: <step> La tabla de transición de estados no existe. Debe crearla antes.')
            exit()


    # -------------------------------------------------------------------------------------------

    def add_state(self, state, key, next_state, action = None):
        """
            Añade uh nuevo estado a la lista de estados, o añade una nueva condición al estado
            ya creado.

        :param state:       Estado a crear o ya creado
        :param key:         Condición: código de identificación de la condición a evaluar
        :param next_state:  Estado siguiente si se cumple la condición, es decir se pulsó la tecla
        :param action:      Acción a realizar si se cumple la condición
        :return:            None

        ------------------------------------------------------------------------------------------------
            NOTA:
                No hay límite teórico para la cantidad de estados o condiciones en la lista
        ------------------------------------------------------------------------------------------------
        """

        # -------------------------------------------------------------------------------------------------------
        # se validan las entradas:
        # El id de estado debe ser un un string. Otro tipo no es valido.

        if not isinstance(state, str):
            print(f'\n\tERROR: El identificador de estado <{state}> debe ser alfanumérico.')
            exit()

        # El id de condición debe ser un un string. Otro tipo no es válido.

        if not isinstance(key, str):
            print(f'\n\tERROR: El identificador en condición o evento <{key}> del estado <{state}> debe ser alfanumérico.')
            exit()

        # El id de condición debe ser un un string. Otro tipo no es .

        if not isinstance(next_state, str):
            print(f'\n\tERROR: El identificador de estado siguente <{next_state}> para la condicion <{key}> del estado <{state}> debe ser alfanumérico.')
            exit()

        # -------------------------------------------------------------------------------------------------------
        # Si el id de estado ya ha sido creado y está en el diccionario de estados, se crea y añade el
        # diccionario de esa nueva condición a la lista de condiciones de ese estado

        event_item = {
            'key': key,
            'next_st': next_state,
            'action': action
        }

        if state in self.state_table.keys():
            self.state_table[state].append(event_item)

        # Si el estado es nuevo se crea la nueva clave de identificador de estado, y una nueva lista con
        # un único item (diccionario) para la presente condición.

        else:
            self.state_table[state] = [event_item]

    # -------------------------------------------------------------------------------------------

    def execute_action(self, state, key):
        """
            Se ejecuta la rutina asociada a una acción de la lista de estados.

        :param state:   estado a la que corresponde la acción
        :param key:     Condición (tecla) asociado a este estado
        :return:
        """

        key_lst = list(self.state_table.keys())
        if state in key_lst:
            for event_key in self.state_table[state]:
                if event_key['key']  ==  key:
                    if event_key['action'] != None:
                        event_key['action']()
                else:
                    print(f'\n\tERROR: El identificador de condición o evento <{key}> no es válido.')
                    exit()

    # -------------------------------------------------------------------------------------------

    def get_state_dict(self):
        """
            Obtiene el diccionario de estados creado

        :return:
        """
        if self.state_table:
            return self.state_table

    # -------------------------------------------------------------------------------------------

    def print_state_dict(self):
        """
            Imprime el contenido de la lista de estados creda
        :return:
        """

        if self.state_table:
            for state in self.state_table.keys():
                print('-' * 80)
                print('ESTADO: ',state)
                print('-' * 80)
                for event_dict in self.state_table[state]:
                    print(f'\t{event_dict}')
            print('-'*80)
        else:
            print('\n\tERROR: La tabla de estados está vacía')
            exit()

