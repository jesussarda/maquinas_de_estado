'''
Created on 25/6/2019

@author: Administrador
'''
from math import *
import pygame
from  numpy import *
from  ClaseModeloNumpy import *
import sys

#------------------------------------------------------------------------------ 

class ModeloCuerpo(object):
    '''
    classdocs
    '''


    #------------------------------------------------------------------------------ 
    #    Constructor
    
    def __init__(self, vertices, lados, Posicion, focal):
        '''
        Constructor
        '''
        self.modelo= Modela()
        
        self.DisFocal =     focal
        self.coordenadas =  vertices
        self.sec=           lados
        self.posicion =     Posicion
        self.Pn= []
        self.Pc= []
     
  #------------------------------------------------------------------------------ 

    def grafica(self, pantalla, Color, LimAxis, grosor):
        """
            
        """
        self.modelo.convierte_a_homogenea(self.coordenadas)                         # Convierte coordenadas a Homogenea (el resuktado queda acumulado) 
        self.modelo.traslada(self.posicion[0], self.posicion[1], self.posicion[2])  # Traslada eje de coordenadas aaun lado 
        self.modelo.perspectiva(self.DisFocal)
        self.Pn= self.modelo.convierte_a_normal(DOS_D)                              # Convierte coordenadas a Homogenea y traspone paraoperar

        Dim= pygame.display.Info()
        dimVert=  Dim.current_h
        dimHori=  Dim.current_w
        self.Pc = self.modelo.mapea_en_pantalla(self.Pn, [LimAxis,LimAxis],[-LimAxis,-LimAxis],[dimHori,dimVert])
        self.modelo.grafica(pantalla, Color, self.Pc, self.sec, grosor)
        
