from libs.utils.class_utilities import EndMsg
from libs.libs_FSM.Classic_FSM import FSM

"""
    ---------------------------------------------------------------------------------
      Problema: Control de semáforo y paso peatonal en una encrucijada (un semáforo 
        en cada cruce.
    --------------------------------------------------------------------------------


        transisiones:

       T / V1.A1.R1.P1.S1.V2.A2.R2.P2.S2
       
       donde:
       
    Entradas:
        T =     evento de tiempo
    Salidas:
        V1 =    Color verde del semaforo 1
        A1 =    Color amarillo del semaforo 1
        R1 =    Color rojo del semaforo 1
        P1 =    Color verde de avance del paso 1
        S1 =    Color rojo de stop del paso 1
        
        V2 =    Color verde del semaforo 2
        A2 =    Color amarillo del semaforo 2
        R2 =    Color rojo del semaforo 2
        P2 =    Color verde de avance del paso 2
        S2 =    Color rojo de stop del paso 2
"""

# ---------------------------------------------------------------------------------------------
# Integración de los datos para la máquina de estados

fsm_config_dict = {
    'ID': 'Proyecto semáforo encrucijada',
    'init_st': 's0',
    'rules': None,
    'events': None
}


# -------------------------------------------------------------------------------------------
#   A C C I O N E S

def set_action(out_event_dict):
    """
        activa o para giro del motor, prende o apaga luz de alarma

    :param event_dict:
    :return:
    """

    for key, value in out_event_dict.items():
        if value:
            print(f'\n\tevento: {key} = {bool(value)}')


# =============================================================================================
#       M A I N
# =============================================================================================


if __name__ == '__main__':

    # ------------------------------------------------------------------------------------------

    expende = FSM(fsm_config_dict)

    # T / V1.A1.R1.P1.S1.V2.A2.R2.P2.S2

    #   Definición de identificadores

    expende.add_event('T', 'input')

    expende.add_event('V1', 'output')
    expende.add_event('A1', 'output')
    expende.add_event('R1', 'output')
    expende.add_event('P1', 'output')
    expende.add_event('S1', 'output')

    expende.add_event('V2', 'output')
    expende.add_event('A2', 'output')
    expende.add_event('R2', 'output')
    expende.add_event('P2', 'output')
    expende.add_event('S2', 'output')

    #   Definición de tabla de transiciones de estado
    #   T / V1.A1.R1.P1.S1.V2.A2.R2.P2.S2

    expende.add_state('S0', '0', 'S0', '1001000101')  #
    expende.add_state('S0', '1', 'S1', '0101000101')  #  Tiempo  15s

    expende.add_state('S1', '0', 'S1', '0101000101')  #
    expende.add_state('S1', '1', 'S2', '0010100110')  #  Tiempo  5s

    expende.add_state('S2', '0', 'S2', None)  # Estado de espera
    expende.add_state('S2', '1', 'S3', None)  # Estado de espera

    expende.add_state('S3', '0', 'S3', None)  # Estado de espera
    expende.add_state('S3', '1', 'S4', None)  # Estado de espera

    expende.add_state('S4', '0', 'S4', None)  # Estado de espera
    expende.add_state('S4', '1', 'S5', None)  # Estado de espera

    expende.add_state('S5', '0', 'S5', None)  # Estado de espera
    expende.add_state('S5', '1', 'S0', None)  # Estado de espera

    state_table = expende.get_state_table()
    expende.validate_table(state_table)

#    for lista in secuencia_eventos:
#        in_event_dict = expende.get_inputs_event_dict()
#        in_event_dict = expende.reset_event_dict(in_event_dict, 'inputs')
#
#        for key, value in lista.items():
#            in_event_dict[key] = int(value)
#
#        codigo_entrada = expende.gets_coded_events(in_event_dict)
#        print(f'state = {expende.actual_state} code= {codigo_entrada}')
#        out_event_dict = expende.step(codigo_entrada)
#        set_action(out_event_dict)
#


