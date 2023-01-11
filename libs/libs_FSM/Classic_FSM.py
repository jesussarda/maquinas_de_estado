
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
        Todas la etiquetas deben estar en letra minúscula. Si alguna etiqueta contiene mayúsculas se convierte
        internamente a minúsculas.

==================================================================================================================

    Ejemplo:
                                                              s
        Para Los estados definidos con los identificadores 'inicio', 'edo_1', 'fin',

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

    ID ='FSM'
                                                     
    # -------------------------------------------------------------------------------------------

    def __init__(self, inicial_state, state_table = None, event_id_dict = None):
        """
           Establece las condiciones iniciales de la Máquina de Estado.

        :param inicial_state:   Estado inicial para la secuencia de transiciones de estados.
        :param state_table:     Diccionario con la secuencia de transiciones de estados
        :param action_dict:     Diccionario con la colección de rutinas de acción que cumple un evento.
        """

        self.event_dict= self.validate_event_id_dict(event_id_dict)

        if state_table:
            self.state_table = self.validate_table(state_table)
        else:
            self.state_table = {}                       # tabla de estados vacía.
                                                        # Se debe crear usando <add_state>
        self.inicial_state =    inicial_state.lower()   # estado de comienzo
        self.actual_state =     self.inicial_state      # estado actual (varía según la tabla de estados

    # -------------------------------------------------------------------------------------------

    def validate_event_id_dict(self, event_id_dict):

        event_dict = {}
        if event_id_dict:
            input_event_list = event_id_dict['inputs']
            if input_event_list:
                event_dict['inputs'] ={}
                for input in input_event_list:
                    event_dict['inputs'][str(input)] = False
            else:
                print(
                    f'\n\tERROR: <create_event_dict> La lista de id de eventos de entrada está vacía.')
                exit()

            output_event_list = event_id_dict['outputs']
            if output_event_list:
                event_dict['outputs'] ={}
                for output in output_event_list:
                    event_dict['outputs'][str(output)] = False  # crea evento y lo inicia en False
            else:
                print(
                    f'\n\tERROR: <create_event_dict> La lista de id de eventos de salida está vacía.')
                exit()
        else:
            print(
                f'\n\tERROR: <create_event_dict> El diccionario de id de eventos está vacío>')
            exit()

        return event_dict

    # -------------------------------------------------------------------------------------------

    def validate_table(self,state_table):
        """
            Valida que las etiquetas de estado sea la misma que en el estado siguiente, independientemente
            de el case.

        :param state_table:    Diccionario de estados.
        :return:               Diccionario de estados validado.
        """

        if state_table:                         # si no está vacio

            state_table = {key.lower(): value for key, value in state_table.items()}    # pone los id de estado en minusculas
            state_list = state_table.keys()
            for num, state in enumerate(state_list):
                event_list = state_table[state]
                if event_list:
                     for idx, event_dict  in enumerate(event_list):
                        if isinstance(event_dict['key'], str) and event_dict['key'].isnumeric():
                            value_list = list(event_dict['key'])
                            for value in value_list:
                                if int(value) > 1:
                                    print(
                                        f'\n\tERROR: <validate_consistency> El dígito <{value}> del identificador de evento <{event_dict["key"]}> de La condición <{idx+1}> del estado <{state}> debe ser binario')
                                    exit()
                        else:
                            print(
                                f'\n\tERROR: <validate_consistency> El identificador de evento <{event_dict["key"]}> de la condición <{idx+1}> del estado <{state}> no es un string o no es numérico')
                            exit()
                        # -----------------------------------------------------------------------------------

                        if  event_dict['next_st'].lower() not in state_list:
                            print(
                                f'\n\tERROR: <validate_consistency> El identificador de estado de transición <{event_dict["next_st"]}> no corresponde con ningún estado de la tabla')
                            exit()
                        else:
                            event_dict['next_st'] = event_dict['next_st'].lower()

                        # -----------------------------------------------------------------------------------

                        if event_dict['action'].isnumeric():
                            value_list = list(event_dict['action'])
                            for value in value_list:
                                if int(value) > 1:
                                    print(
                                        f'\n\tERROR: <validate_consistency> El dígito <{value}> del identificador de acción <{event_dict["action"]}> de La condición <{idx+1}> del estado <{state}> debe ser binario')
                                    exit()
                        else:
                            print(
                                f'\n\tERROR: <validate_consistency> El identificador de acción <{event_dict["action"]}> de la condición <{idx+1}> del estado <{state}> no es numérico')
                            exit()

                else:
                    print(f'\n\tERROR: <validate_consistency> El estado <{state}> no contiene condiciones o eventos')
                    exit()
        else:
            print(
                f'\n\tERROR: <validate_consistency> El diccionario de estados no existe')
            exit()

        return state_table


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
                        self.event_dict = self.update_action(self.event_key['action'])
                    self.actual_state = self.event_key['next_st']
        else:
            print(
                f'\n\tERROR: <step> La tabla de transición de estados no existe. Debe crearla antes.')
            exit()

        return self.event_dict

    # -------------------------------------------------------------------------------------------

    def update_action(self, action_key):
        """

        :param action_key:
        :return:
        """

        if action_key and isinstance(action_key, str):
            output_key_dict = self.event_dict['outputs']
            for idx, key in enumerate(output_key_dict.keys()):
                temp = action_key[idx]
                self.event_dict['outputs'][key] = bool(int(action_key[idx]))
        else:
            print(
                f'\n\tERROR: <update_action> El identificador de acción no existe o no es alfanumérico.')
            exit()

        return self.event_dict

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
        else:
            state = state.lower()

        # El id de condición debe ser un un string. Otro tipo no es válido.

        if not isinstance(key, str):
            print(f'\n\tERROR: El identificador en condición o evento <{key}> del estado <{state}> debe ser alfanumérico.')
            exit()
        else:
            if not key.isnumeric():
                print(
                    f'\n\tERROR: El identificador en condición o evento <{key}> del estado <{state}> debe ser un nomero binario.')
                exit()
            else:
                digit_lst = list(key)
                for digit in digit_lst:
                    if int(digit) > 2:
                        print(
                            f'\n\tERROR: El digito <{digit}> del identificador en condición o evento <{key}> del estado <{state}> debe ser  binario.')
                        exit()

        # El id de condición debe ser un un string. Otro tipo no es .

        if not isinstance(next_state, str):
            print(f'\n\tERROR: El identificador de estado siguente <{next_state}> para la condicion <{key}> del estado <{state}> debe ser alfanumérico.')
            exit()

        # El id de accion debe ser un un string. Otro tipo no es .

        if not isinstance(action, str):
            print(f'\n\tERROR: El identificador de accion <{action}> para la condicion <{key}> del estado <{state}> debe ser alfanumérico.')
            exit()
        else:
            if not action.isnumeric():
                print(
                    f'\n\tERROR: El identificador de accion <{action}> del estado <{state}> debe ser un nomero binario.')
                exit()
            else:
                digit_lst = list(action)
                for digit in digit_lst:
                    if int(digit) > 2:
                        print(
                            f'\n\tERROR: El digito <{digit}> del identificador de acción <{action}> del estado <{state}> debe ser  binario.')
                        exit()

        # -------------------------------------------------------------------------------------------------------
        # Si el id de estado ya ha sido creado y está en el diccionario de estados, se crea y añade el
        # diccionario de esa nueva condición a la lista de condiciones de ese estado

        event_item = {
            'key': key,
            'next_st': next_state.lower(),
            'action': action
        }

        if state in self.state_table.keys():
            self.state_table[state].append(event_item)

        # Si el estado es nuevo se crea la nueva clave de identificador de estado, y una nueva lista con
        # un único item (diccionario) para la presente condición.

        else:
            self.state_table[state] = [event_item]

    # -------------------------------------------------------------------------------------------

    def get_state_table(self):
        """
            Obtiene el diccionario de estados creado

        :return:
        """
        if self.state_table:
            return self.state_table
        else:
            print(
                f'\n\tERROR: <get_state_table> la tabla de estados no ha sido creada aún.')
            exit()

    # -------------------------------------------------------------------------------------------

    def get_event_dict(self):
        """
            Obtiene el diccionario de estados creado

        :return:
        """
        if self.event_dict:
            return self.event_dict
        else:
            print(
                f'\n\tERROR: <get_event_dict> El diccionario de eventos no ha sido creado aún.')
            exit()

    # -------------------------------------------------------------------------------------------

    def get_inputs_event_dict(self):
        """
            Obtiene los eventos de entrada del diccionario de eventos creado

        :return:
        """
        if self.event_dict:
            return self.event_dict['inputs']
        else:
            print(
                f'\n\tERROR: <get_event_dict> El diccionario de eventos no ha sido creado aún.')
            exit()

    # -------------------------------------------------------------------------------------------

    def get_outputs_event_dict(self):
        """
            Obtiene los eventos de salida del diccionario de eventos creado

        :return:
        """
        if self.event_dict:
            return self.event_dict['outputs']
        else:
            print(
                f'\n\tERROR: <get_event_dict> El diccionario de eventos no ha sido creado aún.')
            exit()

    # -------------------------------------------------------------------------------------------

    def set_event_dict(self, event_dict):
        self.event_dict = event_dict

    # -------------------------------------------------------------------------------------------

    def gets_coded_events(self, in_event_dict=None):
        """

        :param event_dict:
        :return:
        """
        if in_event_dict:
             self.event_dict['inputs'] = in_event_dict

        code = ''
        for key, value in in_event_dict.items():
            code += str(int(value))
        return code

    # -------------------------------------------------------------------------------------------

    def print_state_table(self):
        """
            Imprime el contenido de la lista de estados creada

        :return:    None
        """

        if self.state_table:

            print('\n')
            print('=' * 80)
            print('\t\tTABLA DE ESTADOS')
            print('=' * 80)
            print(f'INSTANCIA:\t\t{self.ID}\t\tESTADO INICIAL: {self.inicial_state}')
            for state in self.state_table.keys():
                print('-' * 80)
                print('ESTADO: ',state)
                print('-' * 80)
                for event_dict in self.state_table[state]:
                    print(f'\t{event_dict}')
            print('-'*80)
        else:
            print('\n\tERROR: <print_state_table> La tabla de estados está vacía')
            exit()

    # -------------------------------------------------------------------------------------------

    def print_event_dict(self):
        """
            Imprime estructura y el contenido del diccionario de eventos

        :return:    None
        """

        if self.event_dict:
            print('\n')
            print('=' * 80)
            print('\t\tDICCIONARIO DE EVENTOS')
            print('=' * 80)
            print(f'INSTANCIA:\t\t{self.ID}\t\tESTADO INICIAL: {self.inicial_state}')
            for key, list in self.event_dict.items():
                print('-' * 80)
                print(f'{key.upper()}: ')
                print('-' * 80)
                for item, value in list.items():
                    print(f'\t{item}:\t{int(value)}')
            print('-'*80)

        else:
            print('\n\tERROR: <print_event_dict> El diccionario de eventos np ha sido creado')
            exit()


