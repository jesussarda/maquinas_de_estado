from math import *
#----------------------------------------------------------------
#	Parametros geomnetricos del problema

D= 			50
L=			10
Lambda = 	10
lados = 	12
vertices = 	8

#----------------------------------------------------------------
#	

def ImprimeMatriz(titulo,M):
    
    print (titulo)
    for i in range(len(M)):
        print ('[',end="")
        for j in range(len(M[i])):
            print ('{:>8.5s}'.format(str(M[i][j])),end="")
        print (']')


#----------------------------------------------------------------
#	

def matriz2str(matriz):
    cadena = ""
    for i in range(len(matriz)):
        cadena += "["
        for j in range(len(matriz[i])):
            cadena += "{:>8.5s}".format(str(matriz[i][j]))
        cadena += "]\n"
    return cadena

#----------------------------------------------------------------
#	

def creaMatriz(n,m):
    '''
    Esta funcion crea una matriz vacia con n filas y m columnas.

        param n : 	Numero de filas.
        param m : 	Numero de columnas
        type n: 	entero
        type m: 	entero
        return: 	devuelve una matriz n por m
        rtype: 		matriz (lista de listas)
    '''
    matriz = []
    for i in range(n):
        a = [0]*m
        matriz.append(a)
    return matriz

#----------------------------------------------------------------
#	

def creaMatrizDato(n,m, dato):
    '''
    Esta funcion crea una matriz con n filas y n columnas.
    Cada celda contiene el valor "dato"

        param n : 	Numero de filas.
        param m : 	Numero de columnas
        param dato: Un valor
        type n: 	entero
        type m: 	entero
        type dato: 	tipo simple
        return: 	devuelve una matriz n por m
        rtype: 		matriz (lista de listas)
    '''

    matriz = []
    for i in range(n):
        a = [dato]*m
        matriz.append(a)
    return matriz

#----------------------------------------------------------------
#	

def badmatrix(n,m):
    a = [0]*m
    matriz = [a]*n
    return matriz

#----------------------------------------------------------------
#	

def matrizCorrecta(M):
    '''
    Nos dice si una matriz es correcta.

        param M: 	una matriz
        type M: 	matriz
        return: 	True si es correcta, False en caso contrario
    '''

    filas = len(M)
    columnas = len(M[0])
    correcto = True
    i = 1
    while i < filas and correcto:
        correcto = (len(M[i]) == columnas)
        i += 1
    return correcto

#----------------------------------------------------------------
#	

def filas(M):
    '''
    Nos dice el número de filas de una matriz correcta.

        param M: 	una matriz
        type M: 	matriz
        return: 	numero de filas
    '''
    if matrizCorrecta(M):
        return len(M)

#----------------------------------------------------------------
#	

def columnas(M):
    '''
    Nos dice el número de columnas de una matriz correcta.

        param M: 	una matriz
        type M: 	matriz
        return: 	número de columnas
    '''
    if matrizCorrecta(M):
        return len(M[0])

#----------------------------------------------------------------
#	

def matrizIdentidad(n):
    '''
    Crea una matriz identidad de tamaÃ±o n

        param n : 	número de filas.
        type n : 	entero
        return: 	matriz identidad de tamaÃ±o n
    '''
    m = creaMatriz(n,n)
    for i in range(n):
        m[i][i] = 1
    return m

#----------------------------------------------------------------
#	

def copy(m):
    '''
    Realiza una copia independiente de la matriz
    '''

    result=[]
    for f in m:
        result.append(f[:])
    return result

#----------------------------------------------------------------
#	

def leeMatriz(n,m):
    '''
    Esta función lee por teclado una matríz con n filas y n columnas.

        param n : 	Número de filas.
        param m : 	Número de columnas
        type n: 	entero
        type m: 	entero
        return: 	devuelve una matriz n por m
    '''
    A = creaMatriz(n,m)
    for i in range(n):
        for j in range(m):
            A[i][j] = int(raw_input("Introduce la componente (%d,%d): "%(i,j)))
    return A

#----------------------------------------------------------------
#	

#def copy(m):
#	'''
#	Crea una copia de la matriz
#	'''
#	result=[]
#	for f in m:
#		result.append(f[:])
#	return result


#----------------------------------------------------------------
#	

def sumaMatriz(A,B):
    '''
    Suma dos matrices. Las dos matrices deben ser de la misma dimensión

        param A: 	una matriz nxm
        param B: 	una matriz nxm
        type A: 	Matriz
        type B: 	Matriz
        return: 	Matriz suma
    '''

    if filas(A) == filas(B) and columnas(A) == columnas(B):
        C = creaMatriz(filas(A), columnas(A))
        for i in range(filas(A)):
            for j in range(columnas(A)):
                C[i][j] = A[i][j] + B[i][j]
        return C

#----------------------------------------------------------------
#	

def multiplicaMatriz(A,B):

    '''
    Multiplica dos matrices. El número de columnas de
    la primera debe ser igual al número de filas de la segunda.

        param A: 	una matriz nxm
        param B:	una matriz mxk
        type A: 	Matriz
        type B: 	Matriz
        return: 	Matriz multiplicación nxk
    '''
    if columnas(A) == filas(B):
        C = creaMatriz(filas(A), columnas(B))
        for i in range(filas(C)):
            for j in range(columnas(C)):
                for k in range(columnas(A)):
                    C[i][j] += A[i][k] * B[k][j]
        return C

#----------------------------------------------------------------
#	

def traspuesta(M):
    '''
    Calcula la matriz traspuesta de M
    '''
    m = len(M) 					# filas
    n = len(M[0]) 				# columnas
    T = creaMatriz(n,m)			# crea una nueva matriz
    for i in range(n):
        for j in range(m):
            T[i][j] = M[j][i]	#	traspone los datos
    return T

#----------------------------------------------------------------
#	Convierte vector de puntos en una matriz homogenea

def	homogenea(lista):
    '''
    Convierte la matriz de coorednadas normales a homogenea
    '''
    for punto in lista:
        punto.append(1)
    return lista

#----------------------------------------------------------------
#	Convierte vector de puntos en una matriz homogenea

def	normaliza(M):
    '''
    Convierte la matriz de coorednadas homogenea a normales
    '''
    m = len(M) 					# filas
    n = len(M[0])-1 			# columnas (solo x, y, z)
    T = creaMatriz(m,n)			# crea una nueva matriz
    for i in range(m):
        for j in range(n):
            T[i][j]= M[i][j]/M[i][3]
    #for punto in M:
    #		T[i][j] = punto[0]/punto[3]	#	traspone los datos
    return T

#-------------------------------------------------------------
#   M A I N
#-------------------------------------------------------------

def main():

    #-----------------------------------------------------
    #	Matrices  de transformación
    #-----------------------------------------------------

    #-----------------------------------------------------
    # Traslacion, matriz homogenea

    Xo = 8		#	Translada distancia en el eje  X
    Yo = 5		#	Translada distancia en el eje  Y
    Zo = 0		#	Translada distancia en el eje  Z

    Tra =  [[1, 0, 0, Xo],
            [0, 1, 0, Yo],
            [0, 0, 1, Zo],
            [0, 0, 0,  1]]

    ImprimeMatriz("Traslacion",Tra)

    #-----------------------------------------------------
    # Escalado

    Sx = 100;
    Sy = 100;
    Sz = 100;

    Esc = [[Sx, 0,  0,  0],
           [0, Sy,  0,  0],
           [0,  0, Sz,  0],
           [0,  0,  0,  1]]

    ImprimeMatriz("Escalamiento",Esc)

    #-----------------------------------------------------
    # Rotacion un angulo  alrededor del eje Z

    theta = 45				#	Angulo de rotacion respecto al eje z
    theta = theta*pi/180

    Roz = [ [ cos(theta), sin(theta), 0,  0],
            [-sin(theta), cos(theta), 0,  0],
            [	0,          0,        1,  0],
            [	0,          0,        0,  1]]

    ImprimeMatriz("Rotacion respecto Z",Roz)

    #-----------------------------------------------------
    # Rotacion un angulo  alrededor del eje x

    alfa = 45				#	Angulo de rotacion respecto al eje x
    alfa = alfa*pi/180
    Rox = [ [1,     0,         0,      0],
            [0,  cos(alfa), sin(alfa), 0],
            [0, -sin(alfa), cos(alfa), 0],
            [0,     0,         0,      1]]

    ImprimeMatriz("Rotacion respecto X",Rox)

    #-----------------------------------------------------
    # Rotacion un angulo  alrededor del eje y

    beta = 45				#	Angulo de rotacion respecto al eje y
    beta = beta*pi/180
    Roy = [ [ cos(beta), 0, -sin(beta), 0],
            [    0,      1,      0,     0],
            [ sin(beta), 0,  cos(beta), 0],
            [    0,      0,      0,     1]]

    ImprimeMatriz("Rotacion respecto Y",Roy)

    #-----------------------------------------------------
    #	Transformacion en Perspectiva
    #	NOTA:
    #		- 	Para un punto de coordenada en el espacio
    #			(X,Y,Z) al transformar en homogenea se debe multiplicar
    #			por ubna constante K arbitraria:

    #			(	X, Y, Z, 1)*K = (KX, KY, KZ, K)

    #		- 	Después de hacer las transformaciones correspondientes
    #			el resultado es una coordenada homogenea. Para convertila
    #			a coordenada normal, se dividen las tres primeros elementos
    #			entra el cuarto, pero como es una proyección al plano xy
    #			la ccordenada z resultante no tiene significado, por lo que se
    #			descarta
    #				(xh,yh,zh, val) -> (xh,yh,zh)/val = (x,y,z) -> (x,y)

    # 	Lambda =

    K = 1;

    Per = [ [ 1,    0,     0,      0],
            [ 0,    1,     0,      0],
            [ 0,    0,     1,      0],
            [ 0,    0, -1/Lambda,  1]]

    ImprimeMatriz("Perspectiva",Per)

    #-----------------------------------------------------

    #-----------------------------------------------------
    #	Coordenadas del modelo
    #-----------------------------------------------------
    #	Coordenadas de los vértices de un cubo de lado 2L en el espacio
    #	a una distancia D del plano de proyección, usanso lente con distancia
    #	focal L

    p1= [-L, -L, D]
    p2= [-L,  L, D]
    p3= [ L, -L, D]
    p4= [ L,  L, D]
    p5= [-L, -L, D+L]
    p6= [-L,  L, D+L]
    p7= [ L, -L, D+L]
    p8= [ L,  L, D+L]

    Lista = [p1, p2, p3, p4, p5, p6, p7, p8]	# Lista de puntos  de vertices
    print("Lista de vertices  =         ", Lista)

    #-----------------------------------------------------
    #	Secuencia de pares de puntos para la generación de
    # lineas -lados del cubo-

    sec = [[1, 2], [1, 3], [3, 4], [2, 4], [5, 6], [5, 7], [7, 8], [6, 8], [1, 5], [2, 6], [3, 7], [4, 8]]
    print("Lista de lados   =           ", sec)

    #-----------------------------------------------------

    Ph= homogenea(Lista)
    print("Lista homogenea de vertices= ", Ph)

    Pn = normaliza(Ph)
    print("Lista normalizada de vertices=", Pn)

    Ph =  traspuesta(Ph)
    print("Lista traspuesta de vertices=", Ph)

    #ImprimeMatriz(m)
    #ImprimeMatriz(n)

    #A= [1, 2, 3]
    #B= [[1],[2],[3]]
    #C= traspuesta(B)
    #print(C)

    #s = matriz2str(n)
    #print(s)

    #G= multiplicaMatriz(C,n)
    #ImprimeMatriz(G)

    #ImprimeMatriz(B)
    #ImprimeMatriz(C)

    #-------------------------------------------------------------
    #   Ejecuta M A I N

if __name__ == "__main__":

    main()
