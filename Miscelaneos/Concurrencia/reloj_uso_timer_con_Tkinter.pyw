import tkinter as tk
import time

class AppClock():

    def __init__(self):
        self.root =     tk.Tk()                     #   crea la ventana raiz
        self.label =    tk.Label(text="")           #   crea una etiqueta vacìa
        self.label.pack()                           #   Ajustaa la ventana a la etiqueta

    def update_clock(self):
        now = time.strftime("%H:%M:%S")             #   crea string con formato <hora:minuto:segundo>
        self.label.configure(text=now)              #   y lo coloca en la etiqueta

        self.root.after(1000, self.update_clock)    #   LLama la función despues de cierto tiempo

    def run_clock(self):
        self.update_clock()  # Inicai temporizacion por primera vez
        self.root.mainloop()  # Lazo de tKinter

app= AppClock()  # Crea la aplicación
app.run_clock()