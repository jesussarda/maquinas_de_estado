from class_luz import Luz
import pygame as pg

"""
    ---------------------------------------------------------------------------------
      Problema: Control de la luz en los dos extremos de un pasillo público
    --------------------------------------------------------------------------------
    
      1 - El pasillo dispone de dos pulsadores, uno al lado de cada puerta, de
      manera que se pueda encender y apagar la luz desde cada extremo. Cada
      pulsador produce un ‘1’ lógico mientras está pulsado, y un ‘0’ lógico
      cuando no lo está.
      
      2 - Se desea que, cada vez que se pulse cualquier pulsador, la luz cambie
      de estado: si está apagada se debe encender, y viceversa.
      
      3 - Se debe tener en cuenta el caso en el que, mientras se pulsa un
      interruptor, se pulse el otro. Por ejemplo, si estando apagada la luz,
      alguien pulsa P1 se enciende la luz. Pero si mientras está pulsado P1
      alguien pulsa P2, entonces se apagará nuevamente la luz.
      
      4 - Hay que considerar la simultaneidad de pulsaciones

"""

BG_COLOR = (64,128,128)

# ---------------------------------------------------------------------------------------------
#   Tabla de estados. Reglas de transición de estados:

#   NOTA:
#       El identificador de acción con clave 'action' es el nombre de una función o método que
#       ya ha sido creado y se ha añadido a un diccionario.

# ---------------------------------------------------------------------------------------------

state_table = {
    'S0':  [
        {'key': '00', 'next_st': 'S0',  'action': '0' },
        {'key': '01', 'next_st': 'S1',  'action': '0' },
        {'key': '10', 'next_st': 'S1',  'action': '0' },
        {'key': '11', 'next_st': 'S0',  'action': '0' }],

    'S1': [
        {'key': '00', 'next_st': 'S3', 'action':'1'},
        {'key': '01', 'next_st': 'S1', 'action':'1'},
        {'key': '10', 'next_st': 'S1', 'action':'1'},
        {'key': '11', 'next_st': 'S2', 'action':'1'}],

    'S2': [
        {'key': '00', 'next_st': 'S2', 'action': '0'},
        {'key': '01', 'next_st': 'S4', 'action': '0'},
        {'key': '10', 'next_st': 'S4', 'action': '0'},
        {'key': '11', 'next_st': 'S2', 'action': '0'}],

    'S3': [
        {'key': '00', 'next_st': 'S3', 'action': '1'},
        {'key': '01', 'next_st': 'S4', 'action': '1'},
        {'key': '10', 'next_st': 'S4', 'action': '1'},
        {'key': '11', 'next_st': 'S3', 'action': '1'}],

    'S4': [
        {'key': '00', 'next_st': 'S0', 'action': '0'},
        {'key': '01', 'next_st': 'S4', 'action': '0'},
        {'key': '10', 'next_st': 'S4', 'action': '0'},
        {'key': '11', 'next_st': 'S5', 'action': '0'}],

    'S5': [
        {'key': '00', 'next_st': 'S5', 'action': '1'},
        {'key': '01', 'next_st': 'S1', 'action': '1'},
        {'key': '10', 'next_st': 'S1', 'action': '1'},
        {'key': '11', 'next_st': 'S5', 'action': '1'}]
}

# ---------------------------------------------------------------------------------------------
# Identificadores de eventos de entrada y salida:

#   NOTA:
#       El orden de los identificadores en las listaa son importantes. Debe corresponder con
#       cada dígito binario la clave <key> de la tabla de estados

key_id_dict = {
    'inputs': {'sw_p1': False, 'sw_p2': False},
    'outputs': {'luz': False}
}

# ---------------------------------------------------------------------------------------------
# Integración de los datos para la máquina de estados

fsm_data_dict = {
    'ID': 'Proyecto Luces Pasillo',
    'init_st':  's0',
    'rules':    state_table,
    'events':   key_id_dict
#    'rules': None,
#    'events': None
}

# =============================================================================================
#       M A I N
# =============================================================================================

if __name__ == "__main__":

    pg.init()
    screen = pg.display.set_mode((500, 400))
    pg.display.set_caption('Simula encendido de luz desde dos pulsadores')
    reloj = pg.time.Clock()

    light = Luz(screen,  fsm_data_dict)

#        action_dict = light.get_action_dict()

    if not fsm_data_dict['events']:
        light.add_event('sw_p1', 'input')
        light.add_event('sw_p2', 'input')
        light.add_event('luz', 'output')

        # Tabla de estados.

    if not fsm_data_dict['rules']:
        light.add_state('S0', '00', 'S0', '0')
        light.add_state('S0', '01', 'S1', '0')
        light.add_state('S0', '10', 'S1', '0')
        light.add_state('S0', '11', 'S0', '0')

        light.add_state('S1', '00', 'S3', '1')
        light.add_state('S1', '01', 'S1', '1')
        light.add_state('S1', '10', 'S1', '1')
        light.add_state('S1', '11', 'S2', '1')

        light.add_state('S2', '00', 'S2', '0')
        light.add_state('S2', '01', 'S4', '0')
        light.add_state('S2', '10', 'S4', '0')
        light.add_state('S2', '11', 'S2', '0')

        light.add_state('S3', '00', 'S3', '1')
        light.add_state('S3', '01', 'S4', '1')
        light.add_state('S3', '10', 'S4', '1')
        light.add_state('S3', '11', 'S3', '1')

        light.add_state('S4', '00', 'S0', '0')
        light.add_state('S4', '01', 'S4', '0')
        light.add_state('S4', '10', 'S4', '0')
        light.add_state('S4', '11', 'S5', '0')

        light.add_state('S5', '00', 'S5', '1')
        light.add_state('S5', '01', 'S1', '1')
        light.add_state('S5', '10', 'S1', '1')
        light.add_state('S5', '11', 'S5', '1')

        state_table = light.get_state_table()
        light.validate_table(state_table)


    done = False
    while not done:

        # -------------------------------------
        #   Captura de eventos

        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                done = True

            light.get_push_button_state(evento)

        # -------------------------------------
        #   Simulación del escenario

        screen.fill(BG_COLOR)

        light.simulation_step()
        light.draw_light()

        pg.display.flip()
        reloj.tick(10)

    # ------------------------------------------
    # Fin de la simulación

#    light.print_state_table()   # *** Test ***
    pg.quit()
