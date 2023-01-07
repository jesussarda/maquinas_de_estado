# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 19:15:17 2021

@author: Jesus
"""


class Perros(object):  # Declaramos la clase principal Perros
    def ladrar(self):
        print("""GUAAAUU GUAAAUU!""")

    def grunir(self):
        print("""GRRRRRR GRRRRR""")


class Caniche(Perros):  # La clase secundaria hereda de la clase principal perros
    def ladrar(self):
        print("""guau guau guau""")

    def grunir(self):
        print("""gññññiii gñññiiii""")


class Pastor_Aleman(Perros):  # La clase secundaria hereda de la clase principal perros
    def ladrar(self):
        print("""GuaUUU GUAAAUUU GuaUUU""")

    def grunir(self):
        print("Agrfgregreff aggrrfsgrrr")


class Shepadoodle(Caniche, Pastor_Aleman):  # La clase hereda de las clases hijas de su padre Perros
    def ladrarx(self, veces):
        for cuantas in range(veces):
            super(Shepadoodle, self).ladrar()


Tommy =     Pastor_Aleman()
Piny =      Caniche()

Cuchele =   Shepadoodle()
Cuchele.ladrarx(5)  # Imprime guau guau guau (5 veces) porque heredo el ladrido de la clase padre CANICHE
                    # Pero si eliminamos o renombramos el método ladrar de CANICHE que imprimiria?
                    # Imprimiria el ladrido del Pastor_Aleman
                    # Y  si borramos ambos? Imprimirá el ladrido de Perros!