from libs.libs_FSM.class_System_FSM import SystemFSM

state_table_fsm_1 = {'estado': {}}
key_id_dict_fsm_1 = {'inputs': {}}


state_table_fsm_2 = {'estado': {}}
key_id_dict_fsm_2 = {'inputs': {}}

system_dict = {
    'fsm_1': {
        'ID': 'Máquina 1',
        'init_st': 'test',
        'rules': state_table_fsm_1,
        'events':key_id_dict_fsm_1
    },
    'fsm_2': {
        'ID': 'Máquina 2',
        'init_st': 'test',
        'rules': state_table_fsm_2,
        'events': key_id_dict_fsm_2
    },

}

#system_dict ={}

if __name__ == '__main__':

    ejemplo = SystemFSM(system_dict)
    sys_events= ejemplo.get_sys_event_dict()
    print(sys_events)