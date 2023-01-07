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
        {'key': '00', 'next_st': 'S0',  'action': 'apaga' },
        {'key': '01', 'next_st': 'S1',  'action': 'apaga' },
        {'key': '10', 'next_st': 'S1',  'action': 'apaga' },
        {'key': '11', 'next_st': 'S0',  'action': 'apaga' }],

    'S1': [
        {'key': '00', 'next_st': 'S3', 'action':'prende'},
        {'key': '01', 'next_st': 'S1', 'action':'prende'},
        {'key': '10', 'next_st': 'S1', 'action':'prende'},
        {'key': '11', 'next_st': 'S2', 'action':'prende'}],

    'S2': [
        {'key': '00', 'next_st': 'S2', 'action': 'apaga'},
        {'key': '01', 'next_st': 'S4', 'action': 'apaga'},
        {'key': '10', 'next_st': 'S4', 'action': 'apaga'},
        {'key': '11', 'next_st': 'S2', 'action': 'apaga'}],

    'S3': [
        {'key': '00', 'next_st': 'S3', 'action': 'prende'},
        {'key': '01', 'next_st': 'S4', 'action': 'prende'},
        {'key': '10', 'next_st': 'S4', 'action': 'prende'},
        {'key': '11', 'next_st': 'S3', 'action': 'prende'}],

    'S4': [
        {'key': '00', 'next_st': 'S0', 'action': 'apaga'},
        {'key': '01', 'next_st': 'S4', 'action': 'apaga'},
        {'key': '10', 'next_st': 'S4', 'action': 'apaga'},
        {'key': '11', 'next_st': 'S5', 'action': 'apaga'}],

    'S5': [
        {'key': '00', 'next_st': 'S5', 'action': 'prende'},
        {'key': '01', 'next_st': 'S1', 'action': 'prende'},
        {'key': '10', 'next_st': 'S1', 'action': 'prende'},
        {'key': '11', 'next_st': 'S5', 'action': 'prende'}]
}

# =============================================================================================
#       M A I N
# =============================================================================================

test = True

if __name__ == "__main__":

    pg.init()
    screen = pg.display.set_mode((500, 400))
    pg.display.set_caption('Simula encendido de luz desde dos pulsadores')
    reloj = pg.time.Clock()

    if test:
        light = Luz(screen,  state_table)
        print('\n\tPrueba con tabla de estados externa.')
    else:
        light = Luz(screen)     # crea máquina de estados
        print('\n\tPrueba con tabla de estados añadida.')

        action_dict = light.get_action_dict()

        light.add_state('S0', '00', 'S0', action_dict['apaga'])
        light.add_state('S0', '01', 'S1', action_dict['apaga'])
        light.add_state('S0', '10', 'S1', action_dict['apaga'])
        light.add_state('S0', '11', 'S0', action_dict['apaga'])

        light.add_state('S1', '00', 'S3', action_dict['prende'])
        light.add_state('S1', '01', 'S1', action_dict['prende'])
        light.add_state('S1', '10', 'S1', action_dict['prende'])
        light.add_state('S1', '11', 'S2', action_dict['prende'])

        light.add_state('S2', '00', 'S2', action_dict['apaga'])
        light.add_state('S2', '01', 'S4', action_dict['apaga'])
        light.add_state('S2', '10', 'S4', action_dict['apaga'])
        light.add_state('S2', '11', 'S2', action_dict['apaga'])

        light.add_state('S3', '00', 'S3', action_dict['prende'])
        light.add_state('S3', '01', 'S4', action_dict['prende'])
        light.add_state('S3', '10', 'S4', action_dict['prende'])
        light.add_state('S3', '11', 'S3', action_dict['prende'])

        light.add_state('S4', '00', 'S0', action_dict['apaga'])
        light.add_state('S4', '01', 'S4', action_dict['apaga'])
        light.add_state('S4', '10', 'S4', action_dict['apaga'])
        light.add_state('S4', '11', 'S5', action_dict['apaga'])

        light.add_state('S5', '00', 'S5', action_dict['prende'])
        light.add_state('S5', '01', 'S1', action_dict['prende'])
        light.add_state('S5', '10', 'S1', action_dict['prende'])
        light.add_state('S5', '11', 'S5', action_dict['prende'])

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

    light.print_state_dict()   # *** Test ***
    pg.quit()
