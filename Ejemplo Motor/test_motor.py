from class_motor import Motor
import pygame as pg

"""
    -------------------------------------------------------------------------------------------------
     Problema: Tenemos un istema con unmotor que queremos que se comporte de la forma siguiente :
    -------------------------------------------------------------------------------------------------

    1 - En estado inicial o de reposo, estará detenido en la posición en la
    que el sensor <S> detecta la posición de reposo.
    
    2 - Si no está inicialmente en esa posición se activará una luz de <alarma> pero
    automáticamente se ajustará la posición: arranca el motor para alcanzar la posición
    de reposo y para.
    
    3 - Cuando se pulse Arranque <tecla s>, el motor dará dos vueltas completas,
    deteniéndose en la posición de reposo inicial.
    
    4 - Durante el recorrido, si se pulsa arranque <s> , el motor seguirá
    rotando hasta alcanzar el final de las dos vueltas.
    
    5 - Si al completar las dos vueltas, el pulsador arranque <s>  está pulsado
    por cualquier causa, no se comenzará un ciclo nuevo hasta que deje de
    estar pulsado.

"""

#BG_COLOR = (64,64,64)
BG_COLOR = (64,128,128)
#BG_COLOR = (0,128,64)

# ---------------------------------------------------------------------------------------------
#   Tabla de estados. Reglas de transición de estados:

#   NOTA:
#       El identificador de acción con clave 'action' es el nombre de una función o método que
#       ya ha sido creado y se ha añadido a un diccionario.

# ---------------------------------------------------------------------------------------------

state_table = {
    'inicio':  [
        {'key': '00', 'next_st': 'falla',   'action': 'activa' },
        {'key': '01', 'next_st': 'falla',   'action': 'activa' },
        {'key': '10', 'next_st': 'inicio',  'action': 'para' },
        {'key': '11', 'next_st': 'ciclo_1a','action': 'activa' }],

    'ciclo_1a': [
        {'key': '00', 'next_st': 'ciclo_1b', 'action': 'activa'},
        {'key': '01', 'next_st': 'ciclo_1b', 'action': 'activa'},
        {'key': '10', 'next_st': 'ciclo_1a', 'action': 'activa'},
        {'key': '11', 'next_st': 'ciclo_1a', 'action': 'activa'}],

    'ciclo_1b': [
        {'key': '00', 'next_st': 'falla',    'action': 'activa'},
        {'key': '01', 'next_st': 'ciclo_1b', 'action': 'activa'},
        {'key': '10', 'next_st': 'ciclo_2a', 'action': 'activa'},
        {'key': '11', 'next_st': 'ciclo_2a', 'action': 'activa'}],

    'ciclo_2a': [
        {'key': '00', 'next_st': 'ciclo_2b', 'action': 'activa'},
        {'key': '01', 'next_st': 'ciclo_2b', 'action': 'activa'},
        {'key': '10', 'next_st': 'ciclo_2a', 'action': 'activa'},
        {'key': '11', 'next_st': 'ciclo_2a', 'action': 'activa'}],

    'ciclo_2b': [
        {'key': '00', 'next_st': 'Ciclo_2b','action': 'activa'},
        {'key': '01', 'next_st': 'ciclo_2B','action': 'activa'},
        {'key': '10', 'next_st': 'inicio',  'action': 'para'},
        {'key': '11', 'next_st': 'espera',  'action': 'para'}],

    'espera': [
        { 'key': '00', 'next_st': 'falla',  'action': 'activa' },
        { 'key': '01', 'next_st': 'falla',  'action': 'activa' },
        { 'key': '10', 'next_st': 'inicio', 'action': 'para' },
        { 'key': '11', 'next_st': 'espera', 'action': 'para' }],

    'falla': [
        { 'key': '00', 'next_st': 'falla',  'action':'activa' },
        { 'key': '01', 'next_st': 'falla',  'action':'activa' },
        { 'key': '10', 'next_st': 'inicio', 'action':'para' },
        { 'key': '11', 'next_st': 'inicio', 'action':'para' }]
}

# =============================================================================================
#       M A I N
# =============================================================================================

test = False

if __name__ == "__main__":

    pg.init()
    screen = pg.display.set_mode((500, 400))
    pg.display.set_caption('Simula Arranque de Máquina')
    reloj = pg.time.Clock()

    if test:
        motor = Motor(screen, state_table)
        print('\n\tPrueba con tabla de estados externa.')
    else:
        motor = Motor(screen)
        print('\n\tPrueba con tabla de estados añadida.')

        action_dict = motor.get_action_dict()
    
        # Tabla de estados

        motor.add_state('inicio', '00', 'falla', action_dict['activa'])  # Prende el motor para re posicionar
        motor.add_state('inicio', '01', 'falla', action_dict['activa'])  # Prende el motor para re posicionar
        motor.add_state('inicio', '10', 'inicio', action_dict['para'])  # Apaga el motor para para o mantener parado
        motor.add_state('inicio', '11', 'ciclo_1a', action_dict['activa'])  # Prende el motor para primer giro

        motor.add_state('ciclo_1a', '00', 'ciclo_1b', action_dict['activa'])  # Mantiene el motor prendido para primer giro
        motor.add_state('ciclo_1a', '01', 'ciclo_1b', action_dict['activa'])  # Mantiene el motor prendido para primer giro
        motor.add_state('ciclo_1a', '10', 'ciclo_1a', action_dict['activa'])  # Mantiene el motor prendido hasta que sensor desactive
        motor.add_state('ciclo_1a', '11', 'ciclo_1a', action_dict['activa'])  # Mantiene el motor prendido hasta que sensor desactive

        motor.add_state('ciclo_1b', '00', 'falla', action_dict['activa'])  # Mantiene el motor prendido durante primer giro
        motor.add_state('ciclo_1b', '01', 'ciclo_1b', action_dict['activa'])  # Mantiene el motor prendido durante primer giro
        motor.add_state('ciclo_1b', '10', 'ciclo_2a', action_dict['activa'])  # Mantiene el motor prendido para segundo giro
        motor.add_state('ciclo_1b', '11', 'ciclo_2a', action_dict['activa'])  # Mantiene el motor prendido para segundo giro

        motor.add_state('ciclo_2a', '00', 'ciclo_2b', action_dict['activa'])  # Mantiene el motor prendido para segundo giro
        motor.add_state('ciclo_2a', '01', 'ciclo_2b', action_dict['activa'])  # Mantiene el motor prendido para segundo giro
        motor.add_state('ciclo_2a', '10', 'ciclo_2a', action_dict['activa'])  # Mantiene el motor prendido hasta que sensor desactive
        motor.add_state('ciclo_2a', '11', 'ciclo_2a', action_dict['activa'])  # Mantiene el motor prendido hasta que sensor desactive

        motor.add_state('ciclo_2b', '00', 'ciclo_2b', action_dict['activa'])  # Mantiene el motor prendido hasta que sensor active
        motor.add_state('ciclo_2b', '01', 'ciclo_2b', action_dict['activa'])  # Mantiene el motor prendido hasta que sensor active
        motor.add_state('ciclo_2b', '10', 'inicio', action_dict['para'])  # Apaga el motor para para
        motor.add_state('ciclo_2b', '11', 'espera', action_dict['para'])  # Apaga el motor para para

        motor.add_state('espera', '00', 'falla', action_dict['activa'])  # Prende el motor
        motor.add_state('espera', '01', 'falla', action_dict['activa'])  # Prende el motor
        motor.add_state('espera', '10', 'inicio', action_dict['para'])  # Apaga el motor
        motor.add_state('espera', '11', 'espera', action_dict['para'])  # Apaga el motor

        motor.add_state('falla', '00', 'falla', action_dict['activa'])  # Prende el motor
        motor.add_state('falla', '01', 'falla', action_dict['activa'])  # Prende el motor
        motor.add_state('falla', '10', 'inicio', action_dict['para'])  # Apaga el motor
        motor.add_state('falla', '11', 'inicio', action_dict['para'])  # Apaga el motor

    done = False
    while not done:

        # -------------------------------------
        #   Captura de eventos

        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                done = True

            motor.get_start_button_state(evento)

        # -------------------------------------
        #   Simulación del escenario

        screen.fill(BG_COLOR)

        motor.motor_rotation()
        motor.simulation_step()
        motor.draw_motor()

        pg.display.flip()
        reloj.tick(10)

    pg.quit()