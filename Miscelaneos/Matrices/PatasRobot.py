'''
Created on 25/6/2019

@author: Jesùs Enrique Sardá
'''
from math import *
import pygame
from  numpy import *
from  ClaseModeloNumpy import Modela, DOS_D
import sys

#------------------------------------------------------------------------------ 

class ModeloPata(object):
    '''
    classdocs
    '''

    #------------------------------------------------------------------------------ 
    #    Constructor
    
    def __init__(self, vertices, lados, Posicion, focal, opuesto):
        '''
        Constructor
        '''
        if opuesto == True:
            self.signo= 1
        else:
            self.signo= -1
            
        self.modelo= Modela()
        
        self.DisFocal =     focal
        self.sec=           lados
        self.coordenadas =  vertices
        self.posicion =     Posicion
        self.Pn= []
        self.Pc= []

#------------------------------------------------------------------------------ 

    def mueve_pata_arriba(self, angulo):
        """
        Las coordenadas del modelo de la pata está posicionada respecto al
        centro del eje de coodrenadas,de esa manera se puede transformar girando
        respecto ael eje z y respecto al eje y, que es como se desea como
        comportamiento. Luego se traslada e junto en el espacio que conecta
        con el cuerpo.

        """
        self.modelo.convierte_a_homogenea(self.coordenadas)                         # Convierte coordenadas a Homogenea (el resuktado queda acumulado) 
        self.modelo.RotaZ(self.signo*angulo)                                        # Rota pata respecto al centro del eje
        self.modelo.traslada(self.posicion[0], self.posicion[1], self.posicion[2])  # Traslada eje de coordenadas a un lado
        self.modelo.perspectiva(self.DisFocal)
        self.Pn= self.modelo.convierte_a_normal(DOS_D)                              # Convierte coordenadas a Homogenea y traspone para operar

#------------------------------------------------------------------------------ 

    def grafica(self, pantalla, Color, LimAxis, grosor):
        """
        """
        Dim= pygame.display.Info()
        dimVert=  Dim.current_h
        dimHori=  Dim.current_w
        self.Pc = self.modelo.mapea_en_pantalla(self.Pn, [LimAxis,LimAxis],[-LimAxis,-LimAxis],[dimHori,dimVert])
        self.modelo.grafica(pantalla, Color, self.Pc, self.sec, grosor)
           
#------------------------------------------------------------------------------ 

#     def mueve_pata_arriba(self):
#         pass   
     
    def mueve_pata_abajo(self): 
        pass     
    
    def mueve_pata_adelante(self): 
        pass 
    
    def mueve_pata_atras(self): 
        pass