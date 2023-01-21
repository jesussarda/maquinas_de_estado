from libs.utils.class_utilities import EndMsg
from libs.libs_FSM.Classic_FSM import FSM
"""
    ---------------------------------------------------------------------------------
      Problema: Control de una máquna expendedorq de jugos de naraja y de manzana.
    --------------------------------------------------------------------------------

    -   Los jugos cuestan 30. La máquina recibe monedas de 5, 10 y/0 25 en una ranura. 
    -   Al completarse al monto, se escoge el tipo de jugo (botones de selección) y la
        puerta se abre con el producto.
    -   Si la cantidad de monedas excede el monto, se entrega el vuelto por puerta de
        retorno.
        Se tienen entonces
        
    Eventos de entrada:
        1. monedas de 5                 (m5)   
        2. monedas de 10                (m10)
        3. monedas de 25                (m25)
        4. selección jugo de naranja    (sjn)
        5. selección jugo de manzana    (sjm)
        
    Eventos de salida:
        1. entrega jugo naranja         (ejn)
        2. entrega jugo omanzana        (ejm)
        3. vuelto 5                     (v5)
        4. vuelto 10                    (v10)
        5. vuelto 10                    (v20)
        6. vuelto 25                    (v25)
        
        transisiones:
        
        m5.m10.m25.jn,jm / jn.jm.v5.v10.v20.v25
"""

# ---------------------------------------------------------------------------------------------
# Integración de los datos para la máquina de estados

fsm_config_dict = {
    'ID': 'Proyecto expendedor de jugos',
    'init_st':  's0',
    'rules':    None,
    'events':   None
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

    # ----------------------------------------------------------------------------------------
    # OJO:  Todos los eventos son excluyentes, es decir, si coloco una moneda de 5, no es posible
    #       colocar simultáneamente otra de 10. Si escojo un jugo no puede ser dos simultáneos.

#    secuencia_eventos = [           # Con monedas de 5
#        {'m5': True},  #  5
#        {'m5': True},  #  10
#        {'m5': True},  #  15
#        {'m5': True},  #  20
#        {'m5': True},  #  25
#        {'m5': True},  #  30
#        {'sjn': True}
#    ]

#    secuencia_eventos = [           # Con monedas de 10
#        {'m10': True},  #  10
#        {'m10': True},  #  20
#        {'m10': True},  #  30
#        {'sjn': True}
#    ]

    secuencia_eventos = [           # Con monedas de 25 y 5
        {'m5': True},   #  5
        {'m25': True},  #  30
        {'sjm': True}
    ]

    # ------------------------------------------------------------------------------------------

    expende = FSM(fsm_config_dict)

    # m5.m10.m25.jn,jm / jn.jm.v5.v10.v25

    #   Definición de identificadores

    expende.add_event('m5', 'input')
    expende.add_event('m10', 'input')
    expende.add_event('m25', 'input')
    expende.add_event('sjn', 'input')
    expende.add_event('sjm', 'input')

    expende.add_event('ejn', 'output')
    expende.add_event('ejm', 'output')
    expende.add_event('v5', 'output')
    expende.add_event('v10', 'output')
    expende.add_event('v25', 'output')

    #   Definición de tabla de transiciones de estado
    #   m5.m10.m25.jn,jm / jn.jm.v5.v10.v25

    expende.add_state('S0', '00000', 'S0', None)    # Estado de espera

    expende.add_state('S0', '10000', 'S1', None)    # entra moneda de 5
    expende.add_state('S0', '01000', 'S2', None)    # entra moneda de 10
    expende.add_state('S0', '00100', 'S5', None)    # entra moneda de 25
    expende.add_state('S0', '00010', 'S0', None)    # entra seleción jugo nar.
    expende.add_state('S0', '00001', 'S0', None)    # entra seleción jugo manz.

    expende.add_state('S1', '10000', 'S2', None)    # entra moneda de 5
    expende.add_state('S1', '01000', 'S3', None)    # entra moneda de 10
    expende.add_state('S1', '00100', 'S6', None)    # entra moneda de 25 (se completo 30)
    expende.add_state('S1', '00010', 'S1', None)    # entra seleción jugo nar.
    expende.add_state('S1', '00001', 'S1', None)    # entra seleción jugo manz.

    expende.add_state('S2', '10000', 'S3', None)    # entra moneda de 5
    expende.add_state('S2', '01000', 'S4', None)    # entra moneda de 10
    expende.add_state('S2', '00100', 'S6', '001000')   # entra moneda de 25 (devuelve 5)
    expende.add_state('S2', '00010', 'S2', None)    # entra seleción jugo nar.
    expende.add_state('S2', '00001', 'S2', None)    # entra seleción jugo manz.

    expende.add_state('S3', '10000', 'S4', None)    # entra moneda de 5
    expende.add_state('S3', '01000', 'S5', None)    # entra moneda de 10
    expende.add_state('S3', '00100', 'S6', '000100')    # entra moneda de 25 (devuelve 10)
    expende.add_state('S3', '00010', 'S3', None)    # entra seleción jugo nar.
    expende.add_state('S3', '00001', 'S3', None)    # entra seleción jugo manz.

    expende.add_state('S4', '10000', 'S5', None)    # entra moneda de 5
    expende.add_state('S4', '01000', 'S6', None)    # entra moneda de 10
    expende.add_state('S4', '00100', 'S6', '001100')    # entra moneda de 25 (devuelve 15)
    expende.add_state('S4', '00010', 'S4', None)    # entra seleción jugo nar.
    expende.add_state('S4', '00001', 'S4', None)    # entra seleción jugo manz.

    expende.add_state('S5', '10000', 'S6', None)    # entra moneda de 5  (se completa 30 )
    expende.add_state('S5', '01000', 'S6', '001000')    # entra moneda de 10 (devuelve 5)
    expende.add_state('S5', '00100', 'S6', '000010')    # entra moneda de 25 (devuelve 20)
    expende.add_state('S5', '00010', 'S5', None)    # entra seleción jugo nar.
    expende.add_state('S5', '00001', 'S5', None)    # entra seleción jugo manz.

    expende.add_state('S6', '10000', 'S6', '001000')    # entra moneda de 5  (devuelve 5)
    expende.add_state('S6', '01000', 'S6', '000100')    # entra moneda de 10 (devuelve 10)
    expende.add_state('S6', '00100', 'S6', '000001')    # entra moneda de 25 (devuelve 25)
    expende.add_state('S6', '00010', 'S0', '100000')    # entra seleción jugo nar. y entrega
    expende.add_state('S6', '00001', 'S0', '010000')    # entra seleción jugo manz. y entrega

    state_table = expende.get_state_table()
    expende.validate_table(state_table)

    for lista  in secuencia_eventos:
        in_event_dict = expende.get_inputs_event_dict()
        in_event_dict = expende.reset_event_dict(in_event_dict, 'inputs')

        for key, value in lista.items():
            in_event_dict[key] = int(value)

        codigo_entrada = expende.gets_coded_events(in_event_dict)
        print(f'state = {expende.actual_state} code= {codigo_entrada}')
        out_event_dict = expende.step(codigo_entrada)
        set_action(out_event_dict)



