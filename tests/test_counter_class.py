from libs.utils.class_utilities import CountEvent, EndMsg


def rutina():
    print('\n\t\tSe ejecutó rutina\n')

if __name__ == '__main__':

    contador  = CountEvent('mi_contador', callback= rutina)
#    contador  = CountEvent('mi_contador')

    contador.set_counter(5,False)
    for i in range(10):
        contador.step()
        print(f'{i+1} {contador.is_stopped()}', end= '\t\t')
        evento = contador.get_count_event_dict()
        print(evento)
        print(contador.stop)
