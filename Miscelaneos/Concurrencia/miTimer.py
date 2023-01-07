#-------------------------------------------------------------
#   timer propio
#-------------------------------------------------------------

from threading import Timer
import time

# ----------------------------------------------------------------

def intervalo():
	print("llega 5 seg")

# ----------------------------------------------------------------

if __name__ == '__main__':

	timer= Timer(5.0, intervalo)
	timer.start()

	print("entra")

	cuenta= True
	while cuenta:
		time.sleep(10)
		print("termino 10 seg")
#		timer.start()