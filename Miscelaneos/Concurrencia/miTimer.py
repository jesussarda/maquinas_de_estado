#-------------------------------------------------------------
#   timer propio
#-------------------------------------------------------------

from threading import Timer
import time

# ----------------------------------------------------------------

def funcion(dato):
	print("llega 5 seg dato",dato)

# ----------------------------------------------------------------

if __name__ == '__main__':

	timer= Timer(15.0, funcion,('prueba',) )
	timer.start()

	print("entra")

	cuenta= True
	while cuenta:
		time.sleep(10)
		print("termino 10 seg")
#		timer.start()