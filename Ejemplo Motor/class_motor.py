import pygame as pg
import math

from libs.libs_FSM.Classic_FSM import FSM
from libs.utils.draw_text import Text


# -------------------------------------------------------------------------------------------

SCREEN_DIM =        400,400

POS_MOTOR =         200,200
DIS_MARC_MOTOR =    90
POS_LED_START =     180,0

POS_TXT_START =     POS_MOTOR[0] + POS_LED_START[0] - 20, POS_MOTOR[1] + POS_LED_START[1] - 30

RADIO_LED =         10
RADIO_MARC =        5
RADIO_MOTOR =       100

POS_LED_SENSOR =    130,0

TEXT_COLOR =        (200,200,200)
COLOR_MOTOR =       (200,200,200)
COLOR_MARC =        (255, 0, 0)
LED_SENSOR_ON =     (255,0,0)
LED_SENSOR_OFF =    (64,0,0)
LED_START_ON =      (0,255,0)
LED_START_OFF =     (0,64,0)

# ===================================================================================================

class Motor(FSM):
    """
     -------------------------------------------------------------------------------------------------
     Problema: Tenemos un sistema con un motor que queremos que se comporte de la forma siguiente :
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

    name = 'ctl_motor'

    # -------------------------------------------------------------------------------------------

    def __init__(self, screen, state_table = None, event_id_dict= None):
        """
            Crea la máquina de estados para el problema del control del motor y
            la presentación gráfica de la simulación.
            Usa la librería genérica para una máquina de estados finita <Clasic_FSM>
            Simula el giro de un motor, el sensor de movimiento del motor y la pulsación del arranque
            (tecla <s> de start)

        :param screen:      Token 8identificador) de la ventana de simulación
        :param state_table: Tabla de estados con las reglas de transición (opcional)
        """
        """
            
        :param screen:
        """

        # ===================================================================================

        if state_table:
            super().__init__('inicio', state_table,  event_id_dict)
        else:
            super().__init__('inicio',  event_id_dict = event_id_dict)


        self.screen =       screen

        self.giro_motor =   0
        self.angulo =       0
        self.radian =       0

        self.sensor =       False   # entrada
        self.start_btn =    False   # entrada

        self.sw_start =     True    # salida
        self.alarm =        False   # salida

        self.txt_start = Text( FontSize= 20)

    # -------------------------------------------------------------------------------------------

    def motor_rotation(self):
        """
            Simula el giro del motor
            (incremento de un contador, dependiente de las acciones de la máquina de estado)

        :return: ninguno
        """
        if self.sw_start:
            self.giro_motor += 1

    # ----------------------------------------------------------------------------------------------

    def get_sensor_state(self):
        """
            Obtiene el estado del sensor en la posición de reposo del motor.

        :return: estado del sensor (True: Giro del motor cuando pasa por el estado de reposo.
                                    False: lo contrario
        """
        self.angulo = self.giro_motor* 30
        self.sensor = self.angulo % 360
        return self.sensor == 0

    # ----------------------------------------------------------------------------------------------

    def get_buttons_state(self):
        """
            Obtiene el estado del boton de arranque del motor.
            NOTA:
                es un función auxiliar creada para legibilidad del código
        :return:
        """
        return self.start_btn

    # ----------------------------------------------------------------------------------------------

    def get_start_button_state(self, event):
        """
            Detecta actividad del botón de start del motor (tecla <s> del teclado)
        :param event:
        :return:
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                self.start_btn = True

        elif event.type == pg.KEYUP:
            if event.key == pg.K_s:
                self.start_btn = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.start_btn = True

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.start_btn = False

    # ----------------------------------------------------------------------------------------------

    def simulation_step(self):
        """
            Ejecuta un paso de la máquina de estados adquiriendo el código
            de evento co condición.

        :return: ninguno
        """

        event_dict= self.get_event_dict()
        in_event_dict = event_dict['inputs']
        in_event_dict['pos_motor'] =  int(self.get_sensor_state())
        in_event_dict['sw_start'] =  int(self.get_buttons_state())

        self.event_dict = self.step(self.gets_coded_events(in_event_dict))
        self.set_action(self.event_dict['outputs'])


    # -------------------------------------------------------------------------------------------
    #   A C C I O N E S

    def set_action(self, out_event_dict):
        """
            activa o para giro del motor, prende o apaga luz de alarma

        :param event_dict:
        :return:
        """

        self.sw_start = out_event_dict['acttiva_motor']
        self.sw_alarm = out_event_dict['luz_alarma']

    # ----------------------------------------------------------------------------------------------
    #   D I B U J O S

    def draw_motor(self):
        """
            Dibuja simulación gráfica del motor y los leds de actividad

        :return: ninguno
        """

        self.txt_start.render(self.screen,'START (Tecla S)',POS_TXT_START, TEXT_COLOR)

        pg.draw.circle(self.screen,COLOR_MOTOR, POS_MOTOR, RADIO_MOTOR)                  # motor

        if self.sw_alarm:
                pg.draw.circle(self.screen, LED_SENSOR_ON, (POS_MOTOR[0] + POS_LED_SENSOR[0], POS_MOTOR[1] + POS_LED_SENSOR[1]), RADIO_LED)  # marcador del motor
        else:
            pg.draw.circle(self.screen, LED_SENSOR_OFF, (POS_MOTOR[0] + POS_LED_SENSOR[0], POS_MOTOR[1] + POS_LED_SENSOR[1]), RADIO_LED)  # marcador del motor

        self.radian = (math.pi/180)*self.angulo
        x= DIS_MARC_MOTOR * math.cos(self.radian)
        y= DIS_MARC_MOTOR * math.sin(self.radian)
        pg.draw.circle(self.screen, (255, 0, 0), (POS_MOTOR[0] + x, POS_MOTOR[1] + y), RADIO_MARC)

        if self.get_buttons_state():
            pg.draw.circle(self.screen, LED_START_ON, (POS_MOTOR[0] + POS_LED_START[0], POS_MOTOR[1] + POS_LED_START[1]), RADIO_LED)  # marcador del motor
        else:
            pg.draw.circle(self.screen, LED_START_OFF, (POS_MOTOR[0] + POS_LED_START[0], POS_MOTOR[1] + POS_LED_START[1]), RADIO_LED)  # marcador del motor
