# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 19:15:17 2021

@author: Jesus
"""

class Agregarelemento(list):                    # Creamos una clase Agregarelemento heredando atributos de clase list (clase incorporada)

    def append(self, alumno):                   # Definimos que el método append (de listas) añadirá el elemento alumno
        print (("Añadido el alumno"), (alumno)) # Imprimimos el resultado del método
        super().append(alumno)                  # Incorporamos la función super SIN INDICAR LA CLASE ACTUAL, seguida
                                                # del método append para la variable alumno (append es un metodo de la clase list

Lista1 = Agregarelemento()  # Definimos la clase de nuestra lista llamada "Lista1"
Lista1.append ('Matias')    # Añadimos un elemento a la lista como lo haríamos normalmente
Lista1.append ('Juan')      # Añadimos un elemento a la lista como lo haríamos normalmente

print (Lista1)              # Imprimimos la lista para corroborar que se añadió el alumno