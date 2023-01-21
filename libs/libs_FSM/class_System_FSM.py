from libs.libs_FSM.Classic_FSM import FSM
from libs.utils.class_utilities import EndMsg

key_list = ('ID', 'init_st', 'rules', 'events')


class SystemFSM():
    """
        System Scheduler: Planificador de máquinas de estado interconectadas
    """

    # ----------------------------------------------------------------------------------------

    def __init__(self, fsm_def_tables):
        """

        :param fsm_def_tables:
        """

        self.msg = EndMsg()

        self.fsm_list = []
        fsm_data_tables = self.validate_daf_data(fsm_def_tables)
        if fsm_data_tables:
            for id_name, fsm_def_dict in fsm_def_tables.items():
                machine = FSM(fsm_def_dict)
                self.fsm_list.append(machine)
        else:
            self.msg.put_error_msg('__init__', 'Diccionario de configuración de la máquina está vacía')

    # ------------------------------------------------------------------------------------------

    def get_sys_event_dict(self):
        """

        :return:
        """
        self.sys_events_dic = {}
        for machine in self.fsm_list:
            evant_dict = machine.get_event_dict()
            for id, event in evant_dict['inputs'].items():
                self.sys_events_dic[id] = event
            for id, event in evant_dict['outputs'].items():
                self.sys_events_dic[id] = event

        return self.sys_events_dic

# ----------------------------------------------------------------------------------------------

    def validate_daf_data(self, fsm_def_data):
        """

        :param fsm_def_data:
        :return:
        """

        if fsm_def_data:
            for fsm_key, fsm_dict in fsm_def_data.items():
                for key in key_list:
                    if key not in fsm_dict.keys():
                        self.msg.put_error_msg( 'validate_daf_data',
                            f'Clave <{key}> no está en la configuración de la máquin <{fsm_key}>')

                if not isinstance( fsm_dict['ID'], str):
                    self.msg.put_error_msg( 'validate_daf_data',
                        f'Identificador de máqina <{fsm_dict["ID"]}> debe ser alfanumérico>')

                if not isinstance( fsm_dict['init_st'], str):
                    self.msg.put_error_msg( 'validate_daf_data',
                        f'Identificador de estado inicial <{fsm_dict["init_st"]}> en máquina <{fsm_key}> debe ser alfanumérico')
                else:
                    if not fsm_dict['init_st']:
                        self.msg.put_error_msg( 'validate_daf_data',
                            f'Identificador de estado inicial <{fsm_dict["init_st"]}> en máquina <{fsm_key}> está vacio. Debe existir obligatoriamente'   )

                if  not fsm_dict['rules']:
                    self.msg.put_error_msg( 'validate_daf_data',
                        f'Tabla de estado  <rules> en máquina <{fsm_key}> está vacia. Debe existir obligatoriamente'  )

                if  not fsm_dict['events']:
                    self.msg.put_error_msg( 'validate_daf_data',
                        f'Tabla de eventos  <events> en máquina <{fsm_key}> está vacio. Debe existir obligatoriamente')

        else:
            self.msg.put_error_msg( 'validate_daf_data',
                f'Diccionario de configuración del sistema está vacío')

        return fsm_def_data