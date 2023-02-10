#-------------------------------------------------------------
#   timer propio
#-------------------------------------------------------------

from threading import Timer
import time

# ----------------------------------------------------------------

def funcion(dato):
	print("llega 5 seg dato",dato)
	return dato

# ----------------------------------------------------------------

def una_vez_timer(msg):
	timer= Timer(15.0, funcion,(msg,) )
	timer.start()


if __name__ == '__main__':

	#	timer= Timer(15.0, funcion,('prueba',) )
	#	timer.start()

	una_vez_timer('prueba')

	#	print("entra")

	cuenta= True
	while cuenta:
		time.sleep(10)
		print("sleep 10 seg")
#		timer.start()