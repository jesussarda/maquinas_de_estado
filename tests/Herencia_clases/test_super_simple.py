#!/usr/bin/env python
# -*- coding: utf-8 -*-
#https://pythones.net
"""
Created on Fri Aug 13 19:15:17 2021

@author: Jesus
"""

class Padre(object):                        # Creamos la clase Padre
    # --------------------------------------------------------------------------------------------------
    # Variable de clase y métodoas
    # Son púbicas a nivel de instancia: distintas instancias pueden hacer uso de la misma variable
    # --------------------------------------------------------------------------------------------------

    texto = 'este es el texto'

    @classmethod            # metodo del clase: distintas instancias se ven afectadas por el métoso
    def get_text(cls):
        return cls.texto

    # --------------------------------------------------------------------------------------------------
    # Métodos de instancia
    # --------------------------------------------------------------------------------------------------

    def __init__(self, ojos, cejas):        # Definimos los Atributos en el constructor de la clase
        # Variables de instancia.
        # Son privadas dentro de la instancia

        self.ojos = ojos
        self.cejas = cejas


    def test(self):
        print(self.texto)


    # --------------------------------------------------------------------------------------------------
    # Métodos estáticos. No está ligada a la clase Nota que no se usa self en la declaración.
    # No puede hacer uso de los atributos de la clase
    # --------------------------------------------------------------------------------------------------

    @staticmethod
    def get_test():
        print('es estático')
        
#  ------------------------------------------------------------------------
#   Forma básica

# class Hijo(Padre):                          # Creamos clase hija que hereda de Padre
#     def __init__(self, ojos, cejas, cara):  # Definimos los atributos en el constructor
#         self.ojos = ojos                    # Sobreescribimos cada atributo
#         self.cejas = cejas
#         self.cara = cara                    # Especificamos el nuevo atributo para Hijo
     
        
     
#  ------------------------------------------------------------------------
#   Forma elemental usando atributos del padre

# class Hijo(Padre):                          # Creamos clase hija que hereda de Padre
#     def __init__(self, ojos, cejas, cara):  # Definimos los atributos en el constructor
#         Padre.__init__(self, ojos, cejas)
#         self.cara = cara                    # Especificamos el nuevo atributo para Hijo

#  ------------------------------------------------------------------------
#   Forma avanzada usando super 

class Hijo(Padre):                          # Creamos clase hija que hereda de Padre
    def __init__(self, ojos, cejas, cara):  # Definimos los atributos en el constructor
        super().__init__(ojos, cejas)
        self.cara = cara                    # Especificamos el nuevo atributo para Hijo


texto = Hijo.get_text()                     # ojo el método es de la clase Padre, heredada por la clase HIjo
print(texto)
Hijo.texto = 'texto cambiado'               # se cambia la propiedad para ver que ocurre con varias instancias

Hijo.get_test()

Tomas = Hijo('Marrones', 'Negras', 'Larga') # Instancia 1
print (Tomas.ojos, Tomas.cejas, Tomas.cara) # Imprimimos los atributos del objeto

Pedro = Hijo('verdes', 'Verdes', 'Cortas')  # Instancia 1
print (Pedro.ojos, Pedro.cejas, Pedro.cara) # Imprimimos los atributos del objeto

Tomas.test()                                # NOTA: corre método del padre
Pedro.test()                                # NOTA: corre método del padre