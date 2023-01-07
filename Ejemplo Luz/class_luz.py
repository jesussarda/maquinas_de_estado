import pygame as pg
from libs.libs_FSM.Classic_FSM import FSM
from libs.utils.draw_text import Text

# -------------------------------------------------------------------------------------------

SCREEN_DIM =        400,400

DIS_LUZ_PULS_X =    50
DIS_LUZ_PULS_Y =    150

POS_LUZ =       200,50
POS_LED_P1 =    DIS_LUZ_PULS_X, POS_LUZ[1] + DIS_LUZ_PULS_Y
POS_LED_P2 =    SCREEN_DIM[0] - DIS_LUZ_PULS_X, POS_LUZ[1] +DIS_LUZ_PULS_Y

POS_TEXT_P1 =    POS_LED_P1[0], POS_LED_P1[1] - 30
POS_TEXT_P2 =    POS_LED_P2[0], POS_LED_P2[1] - 30

DIM_PULS    = 10,20
RECT_P1 =     POS_LED_P1[0],POS_LED_P1[1],DIM_PULS[0], DIM_PULS[1]
RECT_P2 =     POS_LED_P2[0],POS_LED_P2[1],DIM_PULS[0], DIM_PULS[1]

RADIO_LUZ =     30
RADIO_PULS =    5

TEXT_PULS =     (255,255,0)

LED_LUZ_ON =    (255,255,255)
LED_LUZ_OFF =   (64,64,64)

LED_P1_ON =     (0,255,0)
LED_P1_OFF =    (0,64,0)
LED_P2_ON =     (0,255,0)
LED_P2_OFF =    (0,64,0)


# -------------------------------------------------------------------------------------------

class Luz(FSM):
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

    name = 'clt_luz'

    # -------------------------------------------------------------------------------------------

    def __init__(self, screen, state_table = None):
        """

        :param screen:
        """

        # ===================================================================================
        # Diccionario de funciones o métodos de acción

        self.accion_dict = {
            'prende': self.prende,
            'apaga':   self.apaga
            }

        # ===================================================================================


        if state_table:
            super().__init__('S0', state_table, self.accion_dict)
        else:
            super().__init__('S0')

        self.screen =       screen

        self.txt_P1 = Text( FontSize= 20)
        self.txt_P2 = Text( FontSize= 20)

        self.sw_luz = False
        self.sw_P1 =  False
        self.sw_P2 =  False

    # -------------------------------------------------------------------------------------------

    def new_state(self, id_st, id_event, id_next_st, id_action):
        """
           Añade un estado y una condición (evento) para ese estado

        :param id_st:       Identificador del estado
        :param id_event:    Identificador del evento
        :param id_next_st:  Identificador del estado siguiente si se da el evento
        :param id_action:   identificdor o apuntador a la función de accion si se d el evento
        :return:    None

        """
        if isinstance(id_action, str):
            self.add_state(id_st, id_event, id_next_st, self.accion_dict[id_action])
#            self.machine.add_state(id_st, id_event, id_next_st, self.accion_dict[id_action])
        else:
            self.add_state(id_st, id_event, id_next_st, id_action)
#            self.machine.add_state(id_st, id_event, id_next_st, id_action)
        pass

    # -------------------------------------------------------------------------------------------

    def get_action_dict(self):
        """
            Se obtiene la lista de funciones definidas
        :return:
        """
        return self.accion_dict

    # -------------------------------------------------------------------------------------------
    #   A C C I O N E S

    def prende(self):
        """
            Prende la luz.
         :return:
        """
        self.sw_luz = True

    def apaga(self):
        """
            Apaga la luz
        :return:
        """
        self.sw_luz = False

    # ----------------------------------------------------------------------------------------------
    #   D I B U J O S

    def draw_light(self):
        """
            Dibuja simulación gráfica de la  luz con los leds de los pulsadores P1 y P2

        :return: ninguno
        """

        self.txt_P1.render(self.screen,'P1 (Tecla s)',POS_TEXT_P1, TEXT_PULS)
        self.txt_P2.render(self.screen,'P2 (Tecla d)',POS_TEXT_P2, TEXT_PULS)

        if self.sw_luz:
            pg.draw.circle(self.screen,LED_LUZ_ON, POS_LUZ, RADIO_LUZ)      # luz
        else:
            pg.draw.circle(self.screen,LED_LUZ_OFF, POS_LUZ, RADIO_LUZ)

        if self.sw_P1:
            pg.draw.rect(self.screen, LED_P1_ON, RECT_P1)
            # pg.draw.circle(self.screen,LED_P1_ON, POS_LED_P1, RADIO_PULS)      # mPulsador P1
        else:
            pg.draw.rect(self.screen, LED_P1_OFF, RECT_P1)
            # pg.draw.circle(self.screen,LED_P1_OFF, POS_LED_P1, RADIO_PULS)

        if self.sw_P2:
            pg.draw.rect(self.screen, LED_P2_ON, RECT_P2)
            # pg.draw.circle(self.screen,LED_P2_ON, POS_LED_P2, RADIO_PULS)      # mPulsador P2
        else:
            pg.draw.rect(self.screen, LED_P2_OFF, RECT_P2)
            # pg.draw.circle(self.screen,LED_P2_OFF, POS_LED_P2, RADIO_PULS)

    # ----------------------------------------------------------------------------------------------

    def get_coded_events(self):
        """
            Obtiene el código numérico del estado de los eventos start y sensor

        :return: Texto con Código numérico correspondiente al estado de los eventos
        """
        code ='{0}{1}'.format(int(self.sw_P1), int(self.sw_P2))
        return code

    # ----------------------------------------------------------------------------------------------

    def get_push_button_state(self, event):
        """
            Detecta actividad del botón de start del motor (tecla <s> del teclado)

        :param event:
        :return:
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                self.sw_P1 = True
            if event.key == pg.K_d:
                self.sw_P2 = True

        elif event.type == pg.KEYUP:
            if event.key == pg.K_s:
                self.sw_P1 = False
            if event.key == pg.K_d:
                self.sw_P2 = False

    # ----------------------------------------------------------------------------------------------

    def simulation_step(self):
        """
            Ejecuta un paso de la máquina de estados adquiriendo el código
            de evento co condición.

        :return: ninguno
        """

        self.step(self.get_coded_events())


