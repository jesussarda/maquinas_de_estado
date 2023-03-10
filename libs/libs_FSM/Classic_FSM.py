from libs.utils.class_utilities import  EndMsg, replace_at
from time import sleep
import re
from copy import copy

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

    ID ='FSM'   # Finite State Machine
                                                     
    # -------------------------------------------------------------------------------------------

    def __init__(self, fsm_config_dict = None):

        """


           Establece las condiciones iniciales de la Máquina de Estado.

        :param inicial_state:   Estado inicial para la secuencia de transiciones de estados.
        :param state_table:     Diccionario con la secuencia de transiciones de estados
        :param action_dict:     Diccionario con la colección de rutinas de acción que cumple un evento.
        """

        self.msg = EndMsg()

        if fsm_config_dict:
            fsm_config_dict = self.validate_config_dict(fsm_config_dict)

            self.ID = fsm_config_dict['ID']
            inicial_state = fsm_config_dict['init_st']
            event_id_dict = fsm_config_dict['events']
            state_table = fsm_config_dict['rules']

            if event_id_dict:
                self.event_dict = self.validate_event_dict(event_id_dict)
            else:
                self.event_dict = {}

            if state_table:
                self.state_table = self.validate_table(state_table)
                self.state_table = self.check_dont_care_keys(self.state_table)
            else:
                self.state_table = {}                       # tabla de estados vacía.
                                                        # Se debe crear usando <add_state>
            self.inicial_state =    inicial_state.lower()   # estado de comienzo
            self.actual_state =     self.inicial_state      # estado actual (varía según la tabla de estados
        else:
            self.msg.error_msg('__init__', 'No se ha introducido el diccionario de configuración de la máquina')

    # -------------------------------------------------------------------------------------------

    def check_dont_care_keys(self, state_table):
        """
            Verifica si  en la definición de eventos existe la condición 'dont care' (simbilo 'x').
            si existe se crea una nueva tabla de estados con los identificadores de eventos expandidos
            (cada dont care implica dos estados 0 y 1. dependiendo de la posicion y la cantidad de 'x'
            hallada los identificadores de evento se multiplican binariamente.

        :param state_table:
        :return:
        """
        if state_table:
            new_state_table = {}
            for state_id in state_table:
                new_state_table[state_id] = []
                for idx, key_item in enumerate(state_table[state_id]):
                    new_key_lst = self.split_dont_care_event(key_item['key'])   # crea lista de nuevos códigos de ventos que substituyen a los dont care
                    for new_key in new_key_lst:                     # crea nuevos eventos con el desglose de dont care
                        event_item = {
                            'key': new_key,
                            'next_st': key_item['next_st'].lower(),
                            'action': key_item['action'].lower()
                        }
                        new_state_table[state_id].append(event_item)    # los añade a la tabla de estados, para estado actual
        else:
            self.msg.error_msg('check_dont_care_keys', 'No se ha introducido el diseño de la tabla de estados')

        return new_state_table

    # -------------------------------------------------------------------------------------------

    def validate_config_dict(self,config_dict):
        """

        :param config_dict:
        :return:
        """
        key_names = ('ID', 'init_st', 'rules', 'events')
        if config_dict:
            for key in key_names:
                if key not in config_dict.keys():
                    self.msg.error_msg('validate_config_dict', f'La clave <{key}> del diccionario no es correcta')
                else:
                    if not config_dict['init_st']:
                        self.msg.error_msg('validate_config_dict',
                            f'Identificador del estado inicial <{config_dict["init_st"]}> en clave <init_st> del diccionario de configuración no existe. Es obligatorio',
                            exit = False)
                        self.msg.error_msg('validate_config_dict',f'{config_dict}')

        else:
            self.msg.error_msg('validate_config_dict',
                'El diccionario de configuración de la máquina de estado no fue creado')

        return config_dict

    # -------------------------------------------------------------------------------------------

    def validate_event_dict(self, event_id_dict):

        if event_id_dict:

            input_event_dict = event_id_dict['inputs']
            if input_event_dict:
                for input_id in input_event_dict.keys():
                    if not isinstance(input_id, str):
                        self.msg.error_msg('validate_event_dict',
                        f'El identificador de evento de entrada <{input_id}> debe ser alfanumérico')
            else:
                self.msg.error_msg('validate_event_dict',
                    'La lista de identificadores de eventos de entrada está vacía')

            output_event_list = event_id_dict['outputs']
            if output_event_list:
                for output_id in output_event_list.keys():
                    if not isinstance(output_id, str):
                        self.msg.error_msg('validate_event_dict',
                            f'El identificador de evento de salida <{output_id}> debe ser alfanumérico')
            else:
                self.msg.error_msg('validate_event_dict', 'La lista de id de eventos de salida está vacía')
        else:
            self.msg.error_msg('validate_event_dict', 'El diccionario de id de eventos está vacío')

        return event_id_dict

    # -------------------------------------------------------------------------------------------

    def validate_table(self,state_table):
        """
            Valida que las etiquetas de estado sea la misma que en el estado siguiente, independientemente
            de el case.

        :param state_table:    Diccionario de estados.
        :return:               Diccionario de estados validado.
        """

        if state_table:                         # si no está vacio

            state_table = {key.lower(): value for key, value in state_table.items()}    # pone los id de estado en minúsculas
            state_list = state_table.keys()
            for num, state in enumerate(state_list):
                event_list = state_table[state]
                if event_list:
                     for idx, event_dict  in enumerate(event_list):

                        # ------------------------------------------------------
                        event_id = event_dict['key']
                        if not isinstance(event_id, str):
                            self.msg.error_msg('validate_table',
                                f'El identificador en condición o evento <{event_id}> del estado <{state}> debe ser alfanumérico')

                        else:
                            if not event_id.isnumeric():
                                if not self.valid_chars_in_key(event_id.lower()):
                                    self.msg.error_msg('validate_table',
                                        f'El identificador de condición o evento <{event_id}> del estado <{state}> no debe contener caracteres distintos de 0, 1, o x')
                                else:
                                    digit_lst = list(event_id)
                                    for digit in digit_lst:
                                        if digit.lower() != 'x':
                                            if int(digit) >= 2:
                                                self.msg.error_msg('validate_table',
                                                    f'El digito <{digit}> del identificador en condición o evento <{event_id}> del estado <{state}> debe ser binario')

                        if  event_dict['next_st'].lower() not in state_list:
                            self.msg.error_msg('validate_table',
                                f'El identificador de estado de transición <{event_dict["next_st"]}> no corresponde con ningún estado de la tabla')
                        else:
                            event_dict['next_st'] = event_dict['next_st'].lower()

                        # -----------------------------------------------------------------------------------

                        if event_dict['action'] is not None:        # NOTA: None es una accion válida
                            if event_dict['action'].isnumeric():
                                value_list = list(event_dict['action'])
                                for value in value_list:
                                    if int(value) > 1:
                                        self.msg.error_msg('validate_table',
                                            f'El dígito <{value}> del identificador de acción <{event_dict["action"]}> de La condición <{idx+1}> del estado <{state}> debe ser binario')
                            else:
                                self.msg.error_msg('validate_table',
                                    f'El identificador de acción <{event_dict["action"]}> de la condición <{idx+1}> del estado <{state}> no es numérico')

                        # ------------------------------------------------------------------------------------
                else:
                    self.msg.error_msg('validate_table', f'El estado <{state}> no contiene condiciones o eventos')
        else:
            self.msg.error_msg('validate_table', f'El diccionario de estados no existe')

        return state_table


    # -------------------------------------------------------------------------------------------

    def step(self, key, delay= None):
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
                    if delay:
                        sleep(delay)
                    break
            self.actual_state = self.event_key['next_st']
        else:
            self.msg.error_msg('step',
                ' La tabla de transición de estados no existe. Debe crearla antes.')

        return self.event_dict['outputs']

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
            self.msg.error_msg('update_action',
                f'El identificador de acción no existe o no es alfanumérico.')
            exit()

        return self.event_dict

    # -------------------------------------------------------------------------------------------

    def valid_chars_in_key(self, event_key):
        """
            Valida el los caracteres del identificador de eventos. Deben ser solo de tres tipos:
            0, 1 y x. Cualquier otro caracter no es válido.
        :param event_key:
        :return:
        """
        if re.search('[^10x]+', event_key):     # Busca por caracteres extraños diferentes de 0,1,x
            return False                        # Encontró al menos uno distinto
        else:
            return True                         # està en regla

    # -------------------------------------------------------------------------------------------

    def _split_item(self, event_lst):
        """
        Crea una lista de identificadores de eventos a partir de laa informaciòn
        de 'dont care' o letra 'x', en los items de la lista <event_lst>
        :param tmp_lst:
        :return:
        """

        group_lst = []
        for item in event_lst:
            idx = item.rfind('x')
            new_item = item
            group_lst.append(replace_at(new_item, idx, '0'))
            new_item = item
            group_lst.append(replace_at(new_item, idx, '1'))
        return group_lst

    # -------------------------------------------------------------------------------------------

    def split_dont_care_event(self,event):
        """
            Procesa los marcadores 'x' ('dont care') y los convierte en
            nuevos identificadores de evento con sus equivalentes en 0 y 1
            respetando la posición. Se creará un lista de identificadores
            de evento equivalentes.

        :return:
        """
        new_event = event.lower()       # IMPORTANTE: asegura que x siempre sea minuscula
        num_x = new_event.count('x')

        event_list = [new_event]
        for i in range(num_x):
            event_list = self._split_item(event_list)
        return event_list

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
            self.msg.error_msg('add_state', f'El identificador de estado <{state}> debe ser alfanumérico')
        else:
            state = state.lower()

        # El id de condición debe ser un un string. Otro tipo no es válido.

        if not isinstance(key, str):
            self.msg.error_msg('add_state',
            f'El identificador en condición o evento <{key}> del estado <{state}> debe ser alfanumérico')
        else:
            # -------------------------------------------------------------
            if not key.isnumeric():
                if not self.valid_chars_in_key(key.lower()):
                    self.msg.error_msg('add_state',
                        f'El identificador de condición o evento <{key}> del estado <{state}> no debe contener caracteres distintos de 0, 1, o x')

                # self.msg.error_msg('add_state',
                #     f'El identificador de condición o evento <{key}> del estado <{state}> debe ser un número binario o contener x')
            else:
                digit_lst = list(key)
                for digit in digit_lst:
                    if digit != 'x':
                        if int(digit) >= 2:
                            self.msg.error_msg('add_state',
                                f'El digito <{digit}> del identificador en condición o evento <{key}> del estado <{state}> debe ser  binario')

        # El id de condición debe ser un un string. Otro tipo no es .

        if not isinstance(next_state, str):
            self.msg.error_msg('add_state',
                f'El identificador de estado siguente <{next_state}> para la condicion <{key}> del estado <{state}> debe ser alfanumérico.')

        # El id de acción debe ser un un string. Otro tipo no es .

        if not isinstance(action, str):
            if action is not None:
                self.msg.error_msg('add_state',
                f'El identificador de acción <{action}> para la condición <{key}> del estado <{state}> debe ser alfanumérico.')
        else:
            if not action.isnumeric():
                self.msg.error_msg('add_state',
                    f'El identificador de acción <{action}> del estado <{state}> debe ser un nomero binario.')
            else:
                digit_lst = list(action)
                for digit in digit_lst:
                    if int(digit) > 2:
                        self.msg.error_msg('add_state',
                            f'El dígito <{digit}> del identificador de acción <{action}> del estado <{state}> debe ser  binario.')

        # -------------------------------------------------------------------------------------------------------
        # Si el id de estado ya ha sido creado y está en el diccionario de estados, se crea y añade el
        # diccionario de esa nueva condición a la lista de condiciones de ese estado


        key_lst =  self.split_dont_care_event(key)

        for key_item in key_lst:

            event_item = {
                'key': key_item,
                'next_st': next_state.lower(),
                'action': action
            }

            # si el identificador del estado ya existe, se añade a la lista de ese ese estado

            if state in self.state_table.keys():
                self.state_table[state].append(event_item)

            # Si el estado es nuevo se crea la nueva clave de identificador de estado, y una nueva lista con
            # un único item (diccionario) para la presente condición.

            else:
                self.state_table[state] = [event_item]

    # -------------------------------------------------------------------------------------------

    def add_event(self, name_event, type = 'input'):
        """

        :param name_event: Identificador del evento
        :param type:        si es de tipo entrada (input) o salida (output)
        :return:
        """

        if not isinstance(name_event, str):
            self.msg.error_msg('add_event',
                f'El identificador de evento <{name_event}> debe ser alfanumérico')
        else:
            if isinstance(self.event_dict, dict):
                if 'input' in type.lower():
                    if 'inputs' in self.event_dict.keys():
                        self.event_dict['inputs'][name_event.lower()] = False
                    else:
                        self.event_dict['inputs'] = {}
                        self.event_dict['inputs'][name_event.lower()] = False

                elif 'output' in type.lower():
                    if 'outputs' in self.event_dict.keys():
                        self.event_dict['outputs'][name_event.lower()] = False
                    else:
                        self.event_dict['outputs'] = {}
                        self.event_dict['outputs'][name_event.lower()] = False
                else:
                    self.msg.error_msg('add_event',
                        f'El tipo de evento <{type}> no es válido. Debe ser <inputs> o <outputs>')

    # -------------------------------------------------------------------------------------------

    def get_state_table(self):
        """
            Obtiene el diccionario de estados creado

        :return:
        """
        if self.state_table:
            return self.state_table
        else:
            self.msg.error_msg('get_state_table', 'la tabla de estados no ha sido creada aún')
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
            self.msg.error_msg('get_event_dict', 'El diccionario de eventos no ha sido creado aún')

    # -------------------------------------------------------------------------------------------

    def get_inputs_event_dict(self):
        """
            Obtiene los eventos de entrada del diccionario de eventos creado

        :return:
        """
        if self.event_dict:
            return self.event_dict['inputs']
        else:
            self.msg.error_msg('get_inputs_event_dict', 'El diccionario de eventos no ha sido creado aún.')
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
            self.msg.error_msg('get_outputs_event_dict', 'El diccionario de eventos no ha sido creado aún')
            exit()

    # -------------------------------------------------------------------------------------------

    def set_event_dict(self, event_dict):
        self.event_dict = event_dict

    # -------------------------------------------------------------------------------------------

    def reset_event_dict(self, event_dict, type= None):
        if type:
            if type.lower() == 'inputs':
                for key in event_dict.keys():
                    event_dict[key] = False

            elif type.lower() == 'outputs':
                for key in event_dict.keys():
                    event_dict[key] = False

            else:
                self.msg.error_msg('reset_event_dict', f'El tipo <{type}> no es correcto')
        else:
            for key in event_dict['inputs'].keys():
                event_dict[key] = False
            for key in event_dict['outputs'].keys():
                event_dict[key] = False

        return event_dict

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
            self.msg.error_msg('print_state_table', 'La tabla de estados está vacía')

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
            self.msg.error_msg('print_event_dict', 'El diccionario de eventos np ha sido creado')


