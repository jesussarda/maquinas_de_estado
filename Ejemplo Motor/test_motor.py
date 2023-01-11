from class_motor import Motor
import pygame as pg

"""
    -------------------------------------------------------------------------------------------------
     Problema: Tenemos un sistema con un motor que queremos que se comporte de la forma siguiente :
    -------------------------------------------------------------------------------------------------

    - En estado inicial o de reposo, estará detenido en la posición en la
    que el sensor <pos> detecta la posición de reposo.
    
    - Si no está inicialmente en esa posición se activará una luz de <alarma> pero
    automáticamente se ajustará la posición: arranca <activa> el motor para alcanzar la posición
    de reposo y para.
    
    - Cuando se pulse arranque <sw,tecla s>, el motor dará dos vueltas completas,
    deteniéndose en la posición de reposo inicial.
    
    - Durante el recorrido, si se pulsa arranque <sw,tecla s>, el motor seguirá
    rotando hasta alcanzar el final de las dos vueltas.
    
    - Si al completar las dos vueltas, el pulsador arranque <sw,tecla s> está pulsado
    por cualquier causa, no se comenzará un ciclo nuevo hasta que deje de estar pulsado.
       
    ---------
     
    NOTA:
        La transiciones de estado está condicionada por dos eventos de entrada y se genera dos
        eventos de salida:
        
            entradas/salidas ->    <pos><arranque>/<alarma><motor> -> '00'/'00'
                  
    
"""

BG_COLOR = (64,128,128)

# ---------------------------------------------------------------------------------------------
#   Tabla de estados. Reglas de transición de estados:

#   NOTA:
#       El identificador de acción con clave 'action' es el nombre de una función o método que
#       ya ha sido creado y se ha añadido a un diccionario.

#   VENTAJA:
#       Al crear la tabla de estado completa, se tienen todos los identificadores de estado
#       ya creados, y por tanto se puede verificar la consistencia, es decir que todos los
#       identificadores de estados siguientes correspondan con los identificadores de estado
#       existentes.

# ---------------------------------------------------------------------------------------------

state_table = {
    'iNicio':  [
        {'key': '00', 'next_st': 'falla',   'action': '10' },
        {'key': '01', 'next_st': 'falla',   'action': '10' },
        {'key': '10', 'next_st': 'inicio',  'action': '00' },
        {'key': '11', 'next_st': 'ciclo_1a','action': '10' }],

    'ciclo_1a': [
        {'key': '00', 'next_st': 'ciClo_1B', 'action': '10'},
        {'key': '01', 'next_st': 'ciclo_1b', 'action': '10'},
        {'key': '10', 'next_st': 'ciclo_1a', 'action': '10'},
        {'key': '11', 'next_st': 'CICLO_1a', 'action': '10'}],

    'ciclo_1b': [
        {'key': '00', 'next_st': 'falla',    'action': '11'},
        {'key': '01', 'next_st': 'ciclo_1b', 'action': '10'},
        {'key': '10', 'next_st': 'ciclo_2a', 'action': '10'},
        {'key': '11', 'next_st': 'ciclo_2a', 'action': '10'}],

    'ciclo_2a': [
        {'key': '00', 'next_st': 'ciclo_2b', 'action': '10'},
        {'key': '01', 'next_st': 'ciclo_2b', 'action': '10'},
        {'key': '10', 'next_st': 'ciclo_2a', 'action': '10'},
        {'key': '11', 'next_st': 'ciclo_2a', 'action': '10'}],

    'ciclo_2b': [
        {'key': '00', 'next_st': 'Ciclo_2b','action': '10'},
        {'key': '01', 'next_st': 'ciclo_2b','action': '10'},
        {'key': '10', 'next_st': 'inicio',  'action': '00'},
        {'key': '11', 'next_st': 'espera',  'action': '00'}],

    'espera': [
        { 'key': '00', 'next_st': 'falla',  'action': '11' },
        { 'key': '01', 'next_st': 'falla',  'action': '11' },
        { 'key': '10', 'next_st': 'inicio', 'action': '00' },
        { 'key': '11', 'next_st': 'espera', 'action': '00' }],

    'falla': [
        { 'key': '00', 'next_st': 'falla',  'action':'11' },
        { 'key': '01', 'next_st': 'falla',  'action':'11' },
        { 'key': '10', 'next_st': 'inicio', 'action':'00' },
        { 'key': '11', 'next_st': 'inicio', 'action':'00' }]
}

# ---------------------------------------------------------------------------------------------
# Identificadores de eventos de entrada y salida:

#   NOTA:
#       El orden de los identificadores en las listaa son importantes. Debe corresponder con
#       cada dígito binario la clave <key> de la tabla de estados

key_id_dict = {
    'inputs': ['pos_motor','sw_start'],
    'outputs': ['acttiva_motor', 'luz_alarma']
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
        motor = Motor(screen, state_table, key_id_dict)
        print('\n\tPrueba con tabla de estados externa.')

        motor.ID = 'Proyecto Motor'
    else:
        motor = Motor(screen, event_id_dict = key_id_dict)
        print('\n\tPrueba con tabla de estados añadida.')

        motor.ID = 'Proyecto Motor'

        # Tabla de estados.
        #   DESVENTAJA: a medida que se an creando los estados, se van validando uno a uno. Como
        #               no se tiene un vision global de la tabla, no es posible verificar la consistencia:
        #               que todas los estados siguentes de transición correspondan con los estados, por lo que
        #               hay que hacer una validacion expresa al final.

        motor.add_state('iNicio', '00', 'faLLa', '10')  # Prende el motor para re posicionar
        motor.add_state('inicio', '01', 'falla', '10')  # Prende el motor para re posicionar
        motor.add_state('inicio', '10', 'inicio', '00')  # Apaga el motor para para o mantener parado
        motor.add_state('inicio', '11', 'ciclo_1a', '10')  # Prende el motor para primer giro

        motor.add_state('ciclo_1a', '00', 'ciclo_1b', '10')  # Mantiene el motor prendido para primer giro
        motor.add_state('ciclo_1a', '01', 'ciclo_1b', '10')  # Mantiene el motor prendido para primer giro
        motor.add_state('ciclo_1a', '10', 'ciclo_1a', '10')  # Mantiene el motor prendido hasta que sensor desactive
        motor.add_state('ciclo_1a', '11', 'ciclo_1a', '10')  # Mantiene el motor prendido hasta que sensor desactive

        motor.add_state('ciclo_1b', '00', 'falla',    '11')  # Mantiene el motor prendido durante primer giro
        motor.add_state('ciclo_1b', '01', 'ciclo_1b', '10')  # Mantiene el motor prendido durante primer giro
        motor.add_state('ciclo_1b', '10', 'ciclo_2a', '10')  # Mantiene el motor prendido para segundo giro
        motor.add_state('ciclo_1b', '11', 'ciclo_2a', '10')  # Mantiene el motor prendido para segundo giro

        motor.add_state('ciclo_2a', '00', 'ciclo_2b', '10')  # Mantiene el motor prendido para segundo giro
        motor.add_state('ciclo_2a', '01', 'ciclo_2b', '10')  # Mantiene el motor prendido para segundo giro
        motor.add_state('ciclo_2a', '10', 'ciclo_2a', '10')  # Mantiene el motor prendido hasta que sensor desactive
        motor.add_state('ciclo_2a', '11', 'ciclo_2a', '10')  # Mantiene el motor prendido hasta que sensor desactive

        motor.add_state('ciclo_2b', '00', 'ciclo_2b', '10')  # Mantiene el motor prendido hasta que sensor active
        motor.add_state('ciclo_2b', '01', 'ciclo_2b', '10')  # Mantiene el motor prendido hasta que sensor active
        motor.add_state('ciclo_2b', '10', 'inicio', '00')  # Apaga el motor para para
        motor.add_state('ciclo_2b', '11', 'espera', '00')  # Apaga el motor para para

        motor.add_state('espera', '00', 'falla',  '11')  # Prende el motor
        motor.add_state('espera', '01', 'falla',  '11')  # Prende el motor
        motor.add_state('espera', '10', 'inicio', '00')  # Apaga el motor
        motor.add_state('espera', '11', 'espera', '00')  # Apaga el motor

        motor.add_state('falla', '00', 'falla',  '11')  # Prende el motor
        motor.add_state('falla', '01', 'falla',  '11')  # Prende el motor
        motor.add_state('falla', '10', 'inicio', '00')  # Apaga el motor
        motor.add_state('falla', '11', 'inicio', '00')  # Apaga el motor

        state_table = motor.get_state_table()
        motor.validate_table(state_table)

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


    motor.print_state_table()   # *** Test ***
    motor.print_event_dict()    # *** Test ***
    print(motor.get_inputs_event_dict())
    print(motor.get_outputs_event_dict())
    pg.quit()