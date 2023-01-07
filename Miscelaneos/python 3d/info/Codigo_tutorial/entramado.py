"""
"""

import numpy as np

#-----------------------------------------------

def matrizTraslacion(dx=0, dy=0, dz=0):
    """ 
    Retorna matriz de traslacion punto a lo largo de un vector (dx, dy, dz).
    """
        
    return np.array([[1,  0,  0,  0],
                     [0,  1,  0,  0],
                     [0,  0,  1,  0],
                     [dx, dy, dz, 1]])
    
#-----------------------------------------------

def matrizEscala(sx=0, sy=0, sz=0):
    """ 
    Retorna matriz para escalar punto a lo largo de todos los ejes centrado en al punto (cx,cy,cz).
    """
    
    return np.array([[sx, 0,  0,  0],
                     [0,  sy, 0,  0],
                     [0,  0,  sz, 0],
                     [0,  0,  0,  1]])
    
#-----------------------------------------------

def matrizRotacionX(radians):
    """ 
    Retorrna matriz de rotación alrededor del eje X un ángulo (en radianes)
    """
    
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[ 1, 0, 0, 0],
                     [ 0, c,-s, 0],
                     [ 0, s, c, 0],
                     [ 0, 0, 0, 1]])
#-----------------------------------------------

def matrizRotacionY(radians):
    """ 
    Retorrna matriz de rotación alrededor del eje Y un ángulo (en radianes)
    """
    
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[ c, 0, s, 0],
                     [ 0, 1, 0, 0],
                     [-s, 0, c, 0],
                     [ 0, 0, 0, 1]])
    
#-----------------------------------------------

def matrizRotacion(eje, angulo):
    if eje == 'X':
        return matrizRotacionX(angulo)
    elif eje == 'Y':
        return matrizRotacionY(angulo)
    elif eje == 'Z':
        return matrizRotacionZ(angulo)
    else:
        print(" Error en la denominación del eje")
        return none
    
def matrizRotacionZ(radians):
    """ 
    Retorrna matriz de rotación alrededor del eje Z un ángulo (en radianes)
    """
    
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[ c,-s, 0, 0],
                     [ s, c, 0, 0],
                     [ 0, 0, 1, 0],
                     [ 0, 0, 0, 1]])
    
#-----------------------------------------------

def matrizProyeccion(K):
    """
    Retorna la matriz que proyecta punto de coordenada 3D del modelo a vista en 
    perspectiva en plano 2D 
    """
    return np.array([[1, 0,  0,  0],
                     [0, 1,  0,  0],
                     [0, 0,  1,  0],
                     [0, 0,-1/K, 1]])

#-----------------------------------------------

class Entramado:
    """
    Crea el entramado de un modelo. Un modelo está formado por una rejilla de coorednadas de
    nodos 0 vertices y bordes 0 lados  
    """
    #-----------------------------------------------

    def __init__(self):
        """
        Crea listas de coordenadas de los vertices y tuplas de los lados o bordes
        """
        
        self.nodos = np.zeros((0, 4))       # Crea un vector de ceros como nodo vacio (nodos homogeneos = x,y,z,1)
        self.bordes = []                    # Crea un lista vacia de bordes (duplas inicio-fin)
    
    #-----------------------------------------------
    #    Crea objetos nodo de una coordenada obtenida de una lista y lo añade a la lista de objetos  
    #

    def anadeNodo(self, lista_nodos):
        """
        Añade a la lista las coordenadas homogeneizadas de vèrtices
        -    Primero crea una columna de de unos tantos como nodos haya en la lista
        -    Lo concatena al la lista para homogenizar la lista
        -    Lo ingresa a la lista de la clase 
        """
        
        columna_unos =  np.ones((len(lista_nodos), 1))          # Crea un vector columna de unos 
        unos_anadidos = np.hstack((lista_nodos, columna_unos))  # Convierte al vector de coordenadas en un vector homogeneo
        self.nodos =    np.vstack((self.nodos, unos_anadidos))  # Añade a la lista de vèr
        
    #-----------------------------------------------

    def anadeBorde(self, lista_bordes):
        """
        Crea objetos borde de tuplas obtenida de una lista 
        y lo añade a la lista de bordes  
        """
        self.bordes += lista_bordes      # Añade lista de bordes a la lista
                   
    #-----------------------------------------------

    def imprimeNodo(self):
        """
        Imprime por consola la lista de vèrtices (nodos)
        """
        print ("\n --- Vértices ------------------------------- ")
        for i, (x, y, z, _) in enumerate(self.nodos):
            print ("   %d: (%d, %d, %d)" % (i, x, y, z))
            
    #-----------------------------------------------

    def imprimeBorde(self):
        """
        Imprime por consola la lista de duplas bordes
        """
        
        print ("\n --- Lados ------------------------------- ")
        for i, (nodo1, nodo2) in enumerate(self.bordes):
            print ("   %d: %d -> %d" % (i, nodo1, nodo2))
    
    #-----------------------------------------------

    def transforma(self, matriz):
        """ 
        Aplica a la lista de nodos una tranformacion definida por la <matriz> dada
        """
            
        self.nodos = np.dot(self.nodos, matriz)
            
    #-----------------------------------------------

    def encuentraCentro(self):
        """ 
        Encuentra el centro del entramado del modelo.
        (el punto medio o centro de masa) 
        """
         
        num_nodos = len(self.nodos)
        mediaX = sum([nodo[0] for nodo in self.nodos]) / num_nodos
        mediaY = sum([nodo[1] for nodo in self.nodos]) / num_nodos
        mediaZ = sum([nodo[2] for nodo in self.nodos]) / num_nodos
        return (mediaX, mediaY, mediaZ) 
                
    #-----------------------------------------------

    def rotaX(self, eje, angulo):
        """ 
        Aplica a la lista de nodos una tranformacion definida por la <matriz> dada
        """
            
#         self.nodos = np.dot(self.nodos, matriz)
        pass
    #-----------------------------------------------

    def rotaY(self, eje, angulo):
        pass
    #-----------------------------------------------

    def rotaZ(self, eje, angulo):
        pass
    
#---------------------------------------------------------

if __name__ == "__main__":

    cubo = Entramado()
    nodos_dubo = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    
    cubo.anadeNodo(np.array(nodos_dubo))
    
    cubo.anadeBorde([(n, n + 4) for n in range(0, 4)])
    cubo.anadeBorde([(n, n + 1) for n in range(0, 8, 2)])
    cubo.anadeBorde([(n, n + 2) for n in (0, 1, 4, 5)])
    cubo.imprimeNodo()
    cubo.imprimeBorde()
    