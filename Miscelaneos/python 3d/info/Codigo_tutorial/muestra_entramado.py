"""
"""
import entramado as ent
import pygame
import numpy as np

#-----------------------------------------------

diccionarioFunciones = {    
    pygame.K_LEFT: (lambda x: x.trasladaTodo([-10,   0, 0])),
    pygame.K_RIGHT:(lambda x: x.trasladaTodo([ 10,   0, 0])),
    pygame.K_DOWN: (lambda x: x.trasladaTodo([  0,  10, 0])),
    pygame.K_UP:   (lambda x: x.trasladaTodo([  0, -10, 0])),

    pygame.K_EQUALS: (lambda x: x.escalaTodo(1.25)),
    pygame.K_MINUS:  (lambda x: x.escalaTodo( 0.8)),

    pygame.K_q: (lambda x: x.rotaTodo('X',  0.1)),
    pygame.K_w: (lambda x: x.rotaTodo('X', -0.1)),
    pygame.K_a: (lambda x: x.rotaTodo('Y',  0.1)),
    pygame.K_s: (lambda x: x.rotaTodo('Y', -0.1)),
    pygame.K_z: (lambda x: x.rotaTodo('Z',  0.1)),
    pygame.K_x: (lambda x: x.rotaTodo('Z', -0.1))}
    
#-----------------------------------------------

class Proyector:
    """ 
    Dibuja un objeto 3D en una pantalla pygame
    """

    #-----------------------------------------------
    
    def __init__(self, ancho, alto):
        """
        Crea una pantalla de dimensiones indicadas y le coloca título
        """

        self.ancho =    ancho                                     # Ancho de la ventana
        self.alto =     alto                                      # Alto de la ventana
        self.pantalla = pygame.display.set_mode((ancho, alto))    # Crea la ventana
        pygame.display.set_caption('Dibujo de un cubo')           # Titula la ventana
        
        self.modelos = {}                       # Diccionario de modelos vacio
        
        self.muestraNodos =  True               # indica si hay vértices 
        self.muestraBordes = True               # indica si hay lados 
        
        self.colorFondo =   (10,10,50)          # fondo Azul marino
        self.colorBorde =   (200,200,200)       # lineas Gris claro 
        self.colorNodo =    (255,255,255)       # punto Blanco
        self.radioPunto =   4                   # El vértice se represnta como un circulo de radio indicado
        
    #-----------------------------------------------

    
    def trasladaTodo(self, vectorTraslado):
        """ 
        Traslada todos los modelos a lo largo de un vector dx,dy,dz
        """
        
        matriz = ent.matrizTraslacion(*vectorTraslado)
        for trama in self.modelos.values():
            trama.transforma(matriz)
        
    #-----------------------------------------------

    def escalaTodo(self, vectorEscala):
        """
        Escala todos los modelos por una factor dado, cintrado en el centro de la pantalla
        """
        
        centro_x = self.ancho/2
        centro_y = self.alto/2
        matriz = ent.matrizEscala(*vectorEscala)
        for trama in self.modelos.values():              # Para cada modelo de la librería
            trama.transforma(matriz)
#            trama.scale((centro_x, centro_y), escala)        # escala
                      
    #-----------------------------------------------

    def rotaTodo(self, eje, angulo):
        """ 
        Rota todo el entramado desde el centro, alrededor del <eje> en un angulo <theta> dado
        """
        
        #Function = 'rota' + eje                     # Nombre del metodo a invocar
        matriz = matrizRotacion(eje, angulo)
        for trama in self.modelos.values():         # para todoas os  objetos wireframe de la libreria
            centro = trama.encuentraCentro()        # obtiene el centro de coordenadas del modelo
            trama.transforma(matriz)
            #getattr(trama, Function)(centro, angulo) # Invoca el Metodo    
                
    #-----------------------------------------------
    
    def ejecuta(self):
        """ 
        Create a pygame pantalla until it is closed. 
        """

        running = True
        while running:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in diccionarioFunciones:
                        diccionarioFunciones[event.key](self)
	                
            self.pantalla.fill(self.colorFondo)     # Colorea fondo de poantalla
            self.display()                          # dibuja el modelo
            pygame.display.flip()                   # Presenta la pantalla
            
#        pygame.quit()

    #-----------------------------------------------
    
    def anadeEntramado(self, name, wireframe):
        """ 
            Add a named wireframe object. 
        """
        
        self.modelos[name] = wireframe
		

    #-----------------------------------------------
    
    def display(self):
        """ 
            Dibuja el modelo en la panalla 
        """
        
        self.pantalla.fill(self.colorFondo)

        for trama in self.modelos.values():
            if self.muestraBordes:
                for n1, n2 in trama.bordes:
                    pygame.draw.aaline(self.pantalla, self.colorBorde, trama.nodos[n1][:2], trama.nodos[n2][:2], 1) #  for edge in wireframe.edges:

            if self.muestraNodos:
                for nodo in trama.nodos:
                    pygame.draw.circle(self.pantalla, self.colorNodo, (int(nodo[0]), int(nodo[1])), self.radioPunto, 0)

#-----------------------------------------------
#    MAIN
#-----------------------------------------------

def main():
    
     # Crea modelo cubo
    
    cubo = ent.Entramado()
    cubo.anadeNodo([(x ,y, z) for x in (50, 250) for y in (50, 250) for z in (50, 250)])
    cubo.anadeBorde([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
    
    # Desarrolla modelo y presenta
    
    pv = Proyector(400, 300)
    pv.anadeEntramado('cubo', cubo)
    pv.ejecuta()
   
if __name__ == '__main__':
    
    main()