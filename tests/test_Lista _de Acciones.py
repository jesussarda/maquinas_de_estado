
#------------------------------------------------
#	Procedimientos y funciones

def Accion1():
    print("run: Accion1, idx: 0")

def Accion2():
    print("run: Accion2, idx:  1")

def Accion3():
    print("run: Accion3, idx:  2")

#------------------------------------------------
#	Librería de funciones
    
ListaAcc = {                #   Se crea la librería
    "cero": Accion1,
    "uno":  Accion2,
    "dos":  Accion3
    }

#------------------------------------------------
#	manejo de lalibreria

def indice(clave):
    i= 0
    Lista_claves = list(ListaAcc.keys())
    if clave in Lista_claves:
        i = Lista_claves.index(clave)
        funcion=  ListaAcc[clave]

#    i=0
#    for key in ListaAcc.keys():
#        if clave == key:
#            print("encontro")
#            break
#        else:
#            i +=1
    return i , funcion
	

#----------------------------------
#	EJECUTA 
#----------------------------------

if __name__ == '__main__':
    
    ind, funcion= indice("dos")
    print(f'indice {ind}')
    funcion()

